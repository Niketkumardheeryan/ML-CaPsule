"""Tests for the from-scratch logistic regression and the data pipeline.

These run offline on synthetic data — no download and no Kaggle credentials —
so they can verify the maths without depending on the network.

    python -m unittest discover -s tests -v
"""

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from banknote_data import standardize, summary, train_test_split  # noqa: E402
from model import LogisticRegression  # noqa: E402


def separable_data(n=200, seed=0):
    """Two clearly separated clouds, which logistic regression must solve."""
    rng = np.random.default_rng(seed)
    negative = rng.normal(-2.0, 0.6, size=(n // 2, 2))
    positive = rng.normal(2.0, 0.6, size=(n // 2, 2))
    X = np.vstack([negative, positive])
    y = np.concatenate([np.zeros(n // 2), np.ones(n // 2)])
    return X, y


class SigmoidTests(unittest.TestCase):
    def setUp(self):
        self.model = LogisticRegression()
        self.model.w = np.array([1.0, -1.0])
        self.model.b = 0.0

    def test_probabilities_stay_within_zero_and_one(self):
        X = np.array([[0.0, 0.0], [50.0, -50.0], [-50.0, 50.0]])
        probabilities = self.model.predict_proba(X)
        self.assertTrue(np.all(probabilities >= 0.0))
        self.assertTrue(np.all(probabilities <= 1.0))

    def test_zero_logit_gives_one_half(self):
        self.assertAlmostEqual(float(self.model.predict_proba(np.array([[0.0, 0.0]]))[0]), 0.5)

    def test_predict_applies_the_threshold(self):
        X = np.array([[5.0, -5.0], [-5.0, 5.0]])
        np.testing.assert_array_equal(self.model.predict(X), [1, 0])
        # A threshold of 1.0 can never be met, so everything becomes class 0.
        np.testing.assert_array_equal(self.model.predict(X, threshold=1.0), [0, 0])


class TrainingTests(unittest.TestCase):
    def test_separable_data_is_learned(self):
        X, y = separable_data()
        model = LogisticRegression()
        model.fit(X, y, epochs=300, gamma=0.5)
        accuracy = (model.predict(X) == y).mean()
        self.assertGreater(accuracy, 0.99)

    def test_loss_decreases(self):
        X, y = separable_data()
        model = LogisticRegression()
        model.fit(X, y, epochs=200, gamma=0.5)
        self.assertEqual(len(model.loss_history), 200)
        self.assertLess(model.loss_history[-1], model.loss_history[0])

    def test_loss_stays_finite_on_confident_predictions(self):
        # Without the guard, a saturated sigmoid would produce log(0) and the
        # loss would become -inf or nan.
        X, y = separable_data(seed=3)
        model = LogisticRegression()
        model.fit(X * 20, y, epochs=100, gamma=0.5)
        self.assertTrue(np.all(np.isfinite(model.loss_history)))

    def test_loss_is_never_negative(self):
        # Cross-entropy is bounded below by zero. Adding epsilon inside the log
        # instead of clipping used to push a saturated loss slightly below it.
        X, y = separable_data(seed=3)
        model = LogisticRegression()
        model.fit(X * 20, y, epochs=100, gamma=0.5)
        self.assertGreaterEqual(min(model.loss_history), 0.0)

    def test_gradient_matches_a_numerical_estimate(self):
        """The analytic gradient should agree with a finite-difference one."""
        rng = np.random.default_rng(5)
        X = rng.normal(size=(40, 3))
        y = (X[:, 0] + X[:, 1] > 0).astype(float)

        model = LogisticRegression()
        model.w = rng.normal(scale=0.1, size=3)
        model.b = 0.0

        def loss_for(weights, bias):
            logits = X @ weights + bias
            probabilities = 1 / (1 + np.exp(-logits))
            epsilon = 1e-15
            return -np.mean(
                y * np.log(probabilities + epsilon)
                + (1 - y) * np.log(1 - probabilities + epsilon)
            )

        predicted = model.predict_proba(X)
        analytic_w = -(X.T @ (y - predicted)) / X.shape[0]
        analytic_b = -np.mean(y - predicted)

        step = 1e-6
        numerical_w = np.zeros_like(analytic_w)
        for index in range(len(analytic_w)):
            up = model.w.copy()
            down = model.w.copy()
            up[index] += step
            down[index] -= step
            numerical_w[index] = (loss_for(up, model.b) - loss_for(down, model.b)) / (2 * step)
        numerical_b = (
            loss_for(model.w, model.b + step) - loss_for(model.w, model.b - step)
        ) / (2 * step)

        np.testing.assert_allclose(analytic_w, numerical_w, atol=1e-5)
        self.assertAlmostEqual(analytic_b, numerical_b, places=5)

    def test_a_column_vector_target_is_handled(self):
        X, y = separable_data(n=100)
        model = LogisticRegression()
        model.fit(X, y.reshape(-1, 1), epochs=100, gamma=0.5)
        self.assertEqual(model.predict(X).shape, (100,))


class SplitAndScaleTests(unittest.TestCase):
    def setUp(self):
        self.X, self.y = separable_data(n=200, seed=7)

    def test_split_sizes_and_no_overlap(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.25)
        self.assertEqual(len(X_train) + len(X_test), len(self.X))
        self.assertEqual(len(X_test), 50)
        train_rows = {tuple(row) for row in X_train}
        test_rows = {tuple(row) for row in X_test}
        self.assertEqual(train_rows & test_rows, set())

    def test_split_preserves_class_balance(self):
        _, _, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2)
        self.assertAlmostEqual(y_train.mean(), 0.5, places=6)
        self.assertAlmostEqual(y_test.mean(), 0.5, places=6)

    def test_split_is_reproducible_for_a_given_seed(self):
        first = train_test_split(self.X, self.y, seed=1)[1]
        second = train_test_split(self.X, self.y, seed=1)[1]
        np.testing.assert_array_equal(first, second)

    def test_standardize_uses_training_statistics_only(self):
        X_train, X_test, _, _ = train_test_split(self.X, self.y)
        scaled_train, scaled_test, (mean, std) = standardize(X_train, X_test)
        np.testing.assert_allclose(scaled_train.mean(axis=0), 0, atol=1e-9)
        np.testing.assert_allclose(scaled_train.std(axis=0), 1, atol=1e-9)
        # The test split is transformed with the training mean/std, not its own.
        np.testing.assert_allclose(scaled_test, (X_test - mean) / std)

    def test_constant_column_does_not_divide_by_zero(self):
        train = np.column_stack([np.ones(10), np.arange(10.0)])
        scaled_train, _, _ = standardize(train, train.copy())
        self.assertTrue(np.all(np.isfinite(scaled_train)))

    def test_summary_counts_both_classes(self):
        self.assertIn("100 genuine / 100 forged", summary(self.X, self.y))


if __name__ == "__main__":
    unittest.main(verbosity=2)

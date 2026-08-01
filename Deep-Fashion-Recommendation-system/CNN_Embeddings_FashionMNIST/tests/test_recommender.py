"""Unit tests for the retrieval and metric layer of the recommender.

These tests use synthetic embeddings, so they run in seconds and need **no
TensorFlow and no dataset download** — TensorFlow is only imported by the
model-building helpers, which are not exercised here.

    python -m unittest discover -s tests -v
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fashion_recommender import (  # noqa: E402
    CLASS_NAMES,
    FashionRecommender,
    class_distribution,
    l2_normalize,
    per_class_precision_at_k,
    precision_at_k,
)


def make_clustered_gallery(per_class: int = 20, dim: int = 8, noise: float = 0.05,
                           n_classes: int = 4, seed: int = 0):
    """Build embeddings where each class sits near its own axis in space."""
    rng = np.random.default_rng(seed)
    embeddings, labels = [], []
    for label in range(n_classes):
        centre = np.zeros(dim, dtype="float32")
        centre[label] = 1.0
        embeddings.append(centre + rng.normal(0, noise, size=(per_class, dim)))
        labels.extend([label] * per_class)
    return np.vstack(embeddings).astype("float32"), np.array(labels)


class NormalisationTests(unittest.TestCase):
    def test_rows_become_unit_length(self):
        normalised = l2_normalize(np.array([[3.0, 4.0], [1.0, 0.0]]))
        np.testing.assert_allclose(np.linalg.norm(normalised, axis=1), [1.0, 1.0], rtol=1e-6)

    def test_single_vector_is_promoted_to_a_row(self):
        self.assertEqual(l2_normalize(np.array([3.0, 4.0])).shape, (1, 2))

    def test_zero_vector_does_not_divide_by_zero(self):
        result = l2_normalize(np.zeros((1, 4)))
        self.assertTrue(np.isfinite(result).all())


class RecommenderTests(unittest.TestCase):
    def setUp(self):
        self.embeddings, self.labels = make_clustered_gallery()
        self.recommender = FashionRecommender(self.embeddings, self.labels).fit()

    def test_recommendations_come_from_the_query_class(self):
        # A query planted on class 2's axis must retrieve class 2 items.
        query = np.zeros(8, dtype="float32")
        query[2] = 1.0
        indices, similarities = self.recommender.recommend(query, k=5)
        self.assertEqual(indices.shape, (1, 5))
        self.assertTrue((self.labels[indices[0]] == 2).all())
        # Cosine similarity to a matching cluster should be close to 1.
        self.assertGreater(similarities[0][0], 0.9)

    def test_similarities_are_sorted_best_first(self):
        indices, similarities = self.recommender.recommend(self.embeddings[:3], k=5)
        for row in similarities:
            self.assertTrue(np.all(np.diff(row) <= 1e-6), f"not descending: {row}")

    def test_batch_queries_are_supported(self):
        indices, similarities = self.recommender.recommend(self.embeddings[:7], k=3)
        self.assertEqual(indices.shape, (7, 3))
        self.assertEqual(similarities.shape, (7, 3))

    def test_k_is_capped_at_the_gallery_size(self):
        small = FashionRecommender(self.embeddings[:4], self.labels[:4]).fit()
        indices, _ = small.recommend(self.embeddings[0], k=99)
        self.assertEqual(indices.shape[1], 4)

    def test_recommend_before_fit_is_an_error(self):
        recommender = FashionRecommender(self.embeddings, self.labels)
        with self.assertRaises(RuntimeError):
            recommender.recommend(self.embeddings[0])

    def test_mismatched_labels_are_rejected(self):
        with self.assertRaises(ValueError):
            FashionRecommender(self.embeddings, self.labels[:-1])

    def test_recommend_labels_returns_readable_names(self):
        names = self.recommender.recommend_labels(self.embeddings[0], k=3)
        self.assertEqual(len(names[0]), 3)
        for name in names[0]:
            self.assertIn(name, CLASS_NAMES)


class MetricTests(unittest.TestCase):
    def setUp(self):
        self.embeddings, self.labels = make_clustered_gallery()
        self.recommender = FashionRecommender(self.embeddings, self.labels).fit()

    def test_well_separated_clusters_score_perfectly(self):
        score = precision_at_k(self.recommender, self.embeddings, self.labels, k=5)
        self.assertAlmostEqual(score, 1.0, places=6)

    def test_random_embeddings_score_near_chance(self):
        # Four balanced classes -> chance precision is about 0.25.
        rng = np.random.default_rng(1)
        noise = rng.normal(size=self.embeddings.shape).astype("float32")
        recommender = FashionRecommender(noise, self.labels).fit()
        score = precision_at_k(recommender, noise, self.labels, k=5)
        self.assertLess(score, 0.6)

    def test_precision_is_bounded(self):
        score = precision_at_k(self.recommender, self.embeddings[:10], self.labels[:10], k=3)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

    def test_per_class_precision_covers_every_queried_class(self):
        scores = per_class_precision_at_k(self.recommender, self.embeddings, self.labels, k=5)
        self.assertEqual(len(scores), 4)
        for value in scores.values():
            self.assertAlmostEqual(value, 1.0, places=6)


class DatasetHelperTests(unittest.TestCase):
    def test_class_names_cover_the_ten_categories(self):
        self.assertEqual(len(CLASS_NAMES), 10)
        self.assertEqual(CLASS_NAMES[0], "T-shirt/top")
        self.assertEqual(CLASS_NAMES[9], "Ankle boot")

    def test_class_distribution_counts_by_readable_name(self):
        counts = class_distribution(np.array([0, 0, 1, 9]))
        self.assertEqual(counts, {"T-shirt/top": 2, "Trouser": 1, "Ankle boot": 1})


if __name__ == "__main__":
    unittest.main(verbosity=2)

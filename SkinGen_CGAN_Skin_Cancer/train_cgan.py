import time
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

import data as data_module
from augment import diff_augment
from models import Discriminator, Generator, LATENT_DIM, initialise_weights, pick_device

CHECKPOINT = Path(__file__).resolve().parent / "cache" / "cgan.pt"
DIFF_POLICY = "color,translation,cutout"


def train(images, labels, n_classes, epochs=300, batch_size=64, lr_g=2e-4, lr_d=1e-4,
          device=None, log_every=25, seed=42, image_size=32, g_steps=1, policy=DIFF_POLICY,
          warm_start=None, spectral=True, minibatch_std=True, ms_weight=0.3,
          diversity_every=10):
    """Train the conditional GAN.

    `ms_weight` controls mode-seeking regularisation (Mao et al., 2019). Two noise vectors are
    pushed through the generator with the same label, and the generator is rewarded for making
    them produce *different* images. This is the one anti-collapse mechanism that acts on the
    generator output directly: the minibatch-stddev layer inside the discriminator cannot do
    the job here, because `diff_augment` randomises every sample before the discriminator sees
    it and that randomness masks the collapse. Set to 0 to disable.

    The penalty is `1 / spread`, which has no target value and so pushes diversity up without
    bound. It has to be tuned against the diversity of real images rather than simply switched
    on: measured over 60 epochs, weight 1.0 settled at ~196% of the real figure and produced
    saturated colour artefacts, while 0.3 settled at ~143% and trending down, with clean
    backgrounds. Hence the default.
    """
    torch.manual_seed(seed)
    device = device or pick_device()

    generator = warm_start or Generator(n_classes, image_size=image_size).to(device)
    discriminator = Discriminator(n_classes, image_size=image_size, spectral=spectral,
                                  minibatch_std=minibatch_std).to(device)
    if warm_start is None:
        generator.apply(initialise_weights)
    discriminator.apply(initialise_weights)

    opt_g = torch.optim.Adam(generator.parameters(), lr=lr_g, betas=(0.5, 0.999))
    opt_d = torch.optim.Adam(discriminator.parameters(), lr=lr_d, betas=(0.5, 0.999))
    criterion = nn.BCEWithLogitsLoss()

    loader = DataLoader(
        TensorDataset(images, labels), batch_size=batch_size, shuffle=True, drop_last=True
    )

    history = []
    started = time.perf_counter()

    for epoch in range(1, epochs + 1):
        d_running, g_running, ms_running = 0.0, 0.0, 0.0

        for real, target in loader:
            real = real.to(device)
            target = target.to(device)
            current = real.size(0)

            noise = torch.randn(current, LATENT_DIM, device=device)
            fake_labels = torch.randint(0, n_classes, (current,), device=device)
            fake = generator(noise, fake_labels)

            opt_d.zero_grad()
            real_score = discriminator(diff_augment(real, policy), target)
            fake_score = discriminator(diff_augment(fake.detach(), policy), fake_labels)
            loss_d = (criterion(real_score, torch.ones_like(real_score) * 0.9)
                      + criterion(fake_score, torch.zeros_like(fake_score)))
            loss_d.backward()
            opt_d.step()

            for _ in range(g_steps):
                opt_g.zero_grad()
                labels_g = torch.randint(0, n_classes, (current,), device=device)
                noise_a = torch.randn(current, LATENT_DIM, device=device)
                fake_a = generator(noise_a, labels_g)

                if ms_weight:
                    # Same labels, different noise: the generator is scored on how far apart
                    # the two images end up relative to how far apart the noise vectors are.
                    noise_b = torch.randn(current, LATENT_DIM, device=device)
                    fake_b = generator(noise_b, labels_g)
                    both = diff_augment(torch.cat([fake_a, fake_b]), policy)
                    score = discriminator(both, torch.cat([labels_g, labels_g]))
                    spread = (torch.mean(torch.abs(fake_a - fake_b))
                              / (torch.mean(torch.abs(noise_a - noise_b)) + 1e-8))
                    penalty = ms_weight / (spread + 1e-5)
                else:
                    score = discriminator(diff_augment(fake_a, policy), labels_g)
                    penalty = torch.zeros((), device=device)

                adversarial = criterion(score, torch.ones_like(score))
                loss_g = adversarial + penalty
                loss_g.backward()
                opt_g.step()

            d_running += loss_d.item()
            g_running += adversarial.item()
            ms_running += float(penalty.detach())

        batches = len(loader)
        row = {"epoch": epoch, "d_loss": d_running / batches, "g_loss": g_running / batches,
               "ms_penalty": ms_running / batches}

        # Sampling flips the generator between train() and eval(), which is expensive enough
        # on some backends to dominate the epoch, so it is measured periodically rather than
        # every epoch.
        if epoch % diversity_every == 0 or epoch in (1, epochs):
            row["diversity"] = sample_diversity(generator, n_classes, device)
        history.append(row)

        if epoch % log_every == 0 or epoch == 1:
            measured = row.get("diversity")
            diversity_text = "" if measured is None else f"diversity {measured:.4f}  "
            print(f"epoch {epoch:>3}/{epochs}  d_loss {row['d_loss']:.3f}  "
                  f"g_loss {row['g_loss']:.3f}  {diversity_text}"
                  f"[{time.perf_counter() - started:.0f}s]", flush=True)

    return generator, history


@torch.no_grad()
def sample_diversity(generator, n_classes, device, per_class=6):
    """Mean per-pixel spread across several samples of the same class.

    This is the metric the first attempts at this project were missing. Generator and
    discriminator losses can sit in a perfectly healthy equilibrium while the generator
    quietly ignores its noise vector and emits one prototype per class - the losses cannot
    see that, but this can. Compare it against the same measurement on real images.
    """
    generator.eval()
    labels = torch.arange(n_classes, device=device).repeat_interleave(per_class)
    noise = torch.randn(len(labels), LATENT_DIM, device=device)
    images = generator(noise, labels)
    generator.train()

    spread = [images[labels == label].std(dim=0).mean() for label in range(n_classes)]
    return float(torch.stack(spread).mean())


@torch.no_grad()
def real_diversity(images, labels, n_classes, per_class=6, seed=0):
    """The same measurement on real images, as the reference the generator is judged against."""
    generator = torch.Generator().manual_seed(seed)
    spread = []
    for label in range(n_classes):
        pool = images[labels == label]
        picks = torch.randperm(len(pool), generator=generator)[:per_class]
        spread.append(pool[picks].std(dim=0).mean())
    return float(torch.stack(spread).mean())


@torch.no_grad()
def generate(generator, labels, device=None, batch_size=256):
    device = device or pick_device()
    generator.eval()
    outputs = []

    for start in range(0, len(labels), batch_size):
        chunk = labels[start:start + batch_size].to(device)
        noise = torch.randn(len(chunk), LATENT_DIM, device=device)
        outputs.append(generator(noise, chunk).cpu())

    generator.train()
    return torch.cat(outputs)


def main():
    payload = data_module.load_data()
    images = data_module.to_float(payload["images"], image_size=32)
    labels = payload["labels"]
    train_index, _ = data_module.stratified_split(labels)

    generator, history = train(
        images[train_index], labels[train_index], n_classes=len(payload["classes"])
    )

    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True, mode=0o755)
    torch.save({"generator": generator.state_dict(), "history": history}, CHECKPOINT)
    print(f"saved {CHECKPOINT}")


if __name__ == "__main__":
    main()

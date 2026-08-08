import math

import torch
import torch.nn as nn

LATENT_DIM = 100
EMBED_DIM = 50


class Generator(nn.Module):
    def __init__(self, n_classes, image_size=32, latent_dim=LATENT_DIM,
                 embed_dim=EMBED_DIM, features=64):
        super().__init__()
        self.latent_dim = latent_dim
        self.label_embedding = nn.Embedding(n_classes, embed_dim)

        blocks = int(round(math.log2(image_size))) - 2
        widths = [features * 2 ** i for i in range(blocks - 1, -1, -1)]

        layers = [
            nn.ConvTranspose2d(latent_dim + embed_dim, widths[0], 4, 1, 0, bias=False),
            nn.BatchNorm2d(widths[0]),
            nn.ReLU(True),
        ]
        for current, following in zip(widths, widths[1:]):
            layers += [
                nn.ConvTranspose2d(current, following, 4, 2, 1, bias=False),
                nn.BatchNorm2d(following),
                nn.ReLU(True),
            ]
        layers += [nn.ConvTranspose2d(widths[-1], 3, 4, 2, 1, bias=False), nn.Tanh()]

        self.net = nn.Sequential(*layers)

    def forward(self, noise, labels):
        conditioned = torch.cat([noise, self.label_embedding(labels)], dim=1)
        return self.net(conditioned.unsqueeze(-1).unsqueeze(-1))


class MinibatchStdDev(nn.Module):
    """Append the batch-wide standard deviation to the feature maps as one extra channel.

    A generator that has learned to ignore its noise vector emits a batch of near-identical
    images, and the standard deviation across that batch is close to zero. Handing the
    discriminator that one number makes the collapse trivially detectable, so the generator
    stops being able to get away with it. From Karras et al., 2018 (Progressive GAN).
    """

    def forward(self, x):
        deviation = x.std(dim=0, unbiased=False).mean()
        return torch.cat([x, deviation.expand(x.size(0), 1, x.size(2), x.size(3))], dim=1)


class Discriminator(nn.Module):
    """Conditional DCGAN discriminator.

    With `spectral=True` every convolution is spectrally normalised and the batch norms are
    dropped, which is the standard SN-GAN discriminator. On a few thousand images that
    Lipschitz constraint is what stops the discriminator from simply memorising the training
    set and starving the generator of gradient.
    """

    def __init__(self, n_classes, image_size=32, features=64, spectral=True,
                 minibatch_std=True):
        super().__init__()
        self.image_size = image_size
        self.label_embedding = nn.Embedding(n_classes, image_size * image_size)

        blocks = int(round(math.log2(image_size))) - 2
        widths = [features * 2 ** i for i in range(blocks)]
        normalise = nn.utils.spectral_norm if spectral else (lambda layer: layer)

        layers = [
            normalise(nn.Conv2d(4, widths[0], 4, 2, 1, bias=False)),
            nn.LeakyReLU(0.2, inplace=True),
        ]
        for current, following in zip(widths, widths[1:]):
            layers.append(normalise(nn.Conv2d(current, following, 4, 2, 1, bias=False)))
            if not spectral:
                layers.append(nn.BatchNorm2d(following))
            layers.append(nn.LeakyReLU(0.2, inplace=True))

        final = widths[-1]
        if minibatch_std:
            layers.append(MinibatchStdDev())
            final += 1
        layers.append(normalise(nn.Conv2d(final, 1, 4, 1, 0, bias=False)))

        self.net = nn.Sequential(*layers)
        self.spectral = spectral

    def forward(self, images, labels):
        maps = self.label_embedding(labels).view(-1, 1, self.image_size, self.image_size)
        return self.net(torch.cat([images, maps], dim=1)).view(-1)


class Classifier(nn.Module):
    def __init__(self, n_classes, features=32):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, features, 3, padding=1),
            nn.BatchNorm2d(features),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(features, features * 2, 3, padding=1),
            nn.BatchNorm2d(features * 2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(features * 2, features * 4, 3, padding=1),
            nn.BatchNorm2d(features * 4),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(features * 4, features * 4, 3, padding=1),
            nn.BatchNorm2d(features * 4),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d(1),
        )
        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.3),
            nn.Linear(features * 4, n_classes),
        )

    def forward(self, x):
        return self.head(self.features(x))


def initialise_weights(module):
    name = module.__class__.__name__
    if "Conv" in name:
        # A spectrally normalised layer keeps the learnable tensor as `weight_orig`;
        # `weight` is recomputed from it, so writing to `weight` would be discarded.
        weight = getattr(module, "weight_orig", getattr(module, "weight", None))
        if weight is not None:
            nn.init.normal_(weight.data, 0.0, 0.02)
    elif "BatchNorm" in name:
        nn.init.normal_(module.weight.data, 1.0, 0.02)
        nn.init.constant_(module.bias.data, 0)


def pick_device():
    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")

import torch
import torch.nn.functional as F


def rand_brightness(x):
    return x + (torch.rand(x.size(0), 1, 1, 1, device=x.device) - 0.5)


def rand_saturation(x):
    mean = x.mean(dim=1, keepdim=True)
    factor = torch.rand(x.size(0), 1, 1, 1, device=x.device) * 2
    return (x - mean) * factor + mean


def rand_contrast(x):
    mean = x.mean(dim=[1, 2, 3], keepdim=True)
    factor = torch.rand(x.size(0), 1, 1, 1, device=x.device) + 0.5
    return (x - mean) * factor + mean


def rand_translation(x, ratio=0.125):
    shift_x = int(x.size(2) * ratio + 0.5)
    shift_y = int(x.size(3) * ratio + 0.5)
    translation_x = torch.randint(-shift_x, shift_x + 1, (x.size(0), 1, 1), device=x.device)
    translation_y = torch.randint(-shift_y, shift_y + 1, (x.size(0), 1, 1), device=x.device)

    grid_batch, grid_x, grid_y = torch.meshgrid(
        torch.arange(x.size(0), device=x.device),
        torch.arange(x.size(2), device=x.device),
        torch.arange(x.size(3), device=x.device),
        indexing="ij",
    )
    grid_x = torch.clamp(grid_x + translation_x + 1, 0, x.size(2) + 1)
    grid_y = torch.clamp(grid_y + translation_y + 1, 0, x.size(3) + 1)

    padded = F.pad(x, [1, 1, 1, 1, 0, 0, 0, 0])
    return padded.permute(0, 2, 3, 1).contiguous()[grid_batch, grid_x, grid_y].permute(0, 3, 1, 2)


def rand_cutout(x, ratio=0.5):
    size = (int(x.size(2) * ratio + 0.5), int(x.size(3) * ratio + 0.5))
    offset_x = torch.randint(0, x.size(2) + (1 - size[0] % 2), (x.size(0), 1, 1), device=x.device)
    offset_y = torch.randint(0, x.size(3) + (1 - size[1] % 2), (x.size(0), 1, 1), device=x.device)

    grid_batch, grid_x, grid_y = torch.meshgrid(
        torch.arange(x.size(0), device=x.device),
        torch.arange(size[0], device=x.device),
        torch.arange(size[1], device=x.device),
        indexing="ij",
    )
    grid_x = torch.clamp(grid_x + offset_x - size[0] // 2, min=0, max=x.size(2) - 1)
    grid_y = torch.clamp(grid_y + offset_y - size[1] // 2, min=0, max=x.size(3) - 1)

    mask = torch.ones(x.size(0), x.size(2), x.size(3), dtype=x.dtype, device=x.device)
    mask[grid_batch, grid_x, grid_y] = 0
    return x * mask.unsqueeze(1)


POLICIES = {
    "color": [rand_brightness, rand_saturation, rand_contrast],
    "translation": [rand_translation],
    "cutout": [rand_cutout],
}


def diff_augment(x, policy="color,translation,cutout"):
    for name in policy.split(","):
        for function in POLICIES[name.strip()]:
            x = function(x)
    return x.contiguous()


def classical_augment(images, count, seed=0):
    generator = torch.Generator().manual_seed(seed)
    picks = torch.randint(0, len(images), (count,), generator=generator)
    batch = images[picks].clone()

    flips = torch.rand(count, generator=generator)
    batch[flips < 0.5] = torch.flip(batch[flips < 0.5], dims=[3])

    vertical = torch.rand(count, generator=generator)
    batch[vertical < 0.5] = torch.flip(batch[vertical < 0.5], dims=[2])

    turns = torch.randint(0, 4, (count,), generator=generator)
    for k in range(1, 4):
        selected = turns == k
        if selected.any():
            batch[selected] = torch.rot90(batch[selected], k, dims=[2, 3])

    brightness = (torch.rand(count, 1, 1, 1, generator=generator) - 0.5) * 0.3
    batch = (batch + brightness).clamp(-1, 1)

    return batch

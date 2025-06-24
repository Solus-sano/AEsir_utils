import torch
from PIL import Image
import numpy as np

__all__ = ["add_diffusion_noise"]


def add_diffusion_noise(image, noise_step, beta=0.01, max_steps=1000):
    """Add forward diffusion noise to an image.

    Parameters
    ----------
    image : ``torch.Tensor`` or :class:`~PIL.Image.Image`
        Input image to be noised.
    noise_step : int
        Current diffusion step. Must be within ``[0, max_steps]``.
    beta : float, optional
        Noise rate of each step. Default ``0.01``.
    max_steps : int, optional
        Maximum diffusion step. Default ``1000``.

    Returns
    -------
    ``torch.Tensor`` or :class:`~PIL.Image.Image`
        Noisy image with the same type as the input.
    """
    if noise_step < 0 or noise_step > max_steps:
        raise ValueError(f"noise_step should be between 0 and {max_steps}")

    alpha_bar = (1.0 - beta) ** noise_step

    if isinstance(image, Image.Image):
        img = np.array(image).astype(np.float32) / 255.0
        noise = np.random.randn(*img.shape).astype(np.float32)
        noisy = np.sqrt(alpha_bar) * img + np.sqrt(1 - alpha_bar) * noise
        noisy = np.clip(noisy, 0.0, 1.0)
        return Image.fromarray((noisy * 255).astype(np.uint8))

    if torch.is_tensor(image):
        noise = torch.randn_like(image)
        return (alpha_bar ** 0.5) * image + ((1 - alpha_bar) ** 0.5) * noise

    raise TypeError("image must be a torch.Tensor or PIL.Image.Image")

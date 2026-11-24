"""DFT-based utilities for image de-raining."""
import numpy as np
import cv2

def remove_rain_fallback(img):
    """Remove near-vertical rain frequencies and sharpen the result."""
    img_uint8 = np.uint8(np.clip(img * 255, 0, 255))
    yuv = cv2.cvtColor(img_uint8, cv2.COLOR_RGB2YUV)
    luminance = yuv[..., 0].astype(np.float32) / 255.0

    # A vertical streak produces energy mainly across the horizontal frequency
    # axis. Smoothly attenuate that directional high-frequency energy while
    # leaving the low-frequency scene structure and colour channels intact.
    height, width = luminance.shape
    fy = np.fft.fftshift(np.fft.fftfreq(height))[:, None]
    fx = np.fft.fftshift(np.fft.fftfreq(width))[None, :]
    radius = np.sqrt(fx * fx + fy * fy)
    directional_band = np.exp(-((fy / (0.035 + 0.35 * np.abs(fx))) ** 2))
    high_frequency = 1.0 - np.exp(-((radius / 0.03) ** 2))
    dft_filter = 1.0 - (0.96 * directional_band * high_frequency)

    spectrum = np.fft.fftshift(np.fft.fft2(luminance))
    clean_luminance = np.real(np.fft.ifft2(np.fft.ifftshift(spectrum * dft_filter)))
    clean_luminance = np.clip(clean_luminance, 0.0, 1.0)

    yuv[..., 0] = np.uint8(clean_luminance * 255.0)
    derained = cv2.cvtColor(yuv, cv2.COLOR_YUV2RGB)
    derained = cv2.bilateralFilter(derained, 7, 35, 35)

    # Strong unsharp mask restores edges softened by frequency attenuation.
    blurred = cv2.GaussianBlur(derained, (0, 0), 1.1)
    derained = cv2.addWeighted(derained, 1.65, blurred, -0.65, 0)
    return np.clip(derained / 255.0, 0, 1)


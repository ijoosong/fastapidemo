import random
from collections import namedtuple
from typing import Tuple
from colorsys import hls_to_rgb, hsv_to_rgb, rgb_to_hsv

Colour = namedtuple("Colour", "base circle")


def complementary(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """Returns RGB components of complementary color."""
    hsv = rgb_to_hsv(r, g, b)
    return hsv_to_rgb((hsv[0] + 0.5) % 1, hsv[1], hsv[2])


def make_color(hue: float, dark_variant: bool) -> Tuple[float, float, float]:
    """Make a nice hls color to use in a avatar."""
    saturation = 1
    lightness = random.uniform(.7, .85)

    # green and blue do not like high lightness, so we adjust this depending on how far from blue-green we are
    # hue_fix is the square of the distance between the hue and cyan (0.5 hue)
    hue_fix = (1 - abs(hue - 0.5)) ** 2
    # magic fudge factors
    lightness -= hue_fix * 0.15
    if dark_variant:
        lightness -= hue_fix * 0.25
    saturation -= hue_fix * 0.1

    return hue, lightness, saturation


def generate_griffify_colours() -> Colour:
    """Generate two beautiful colours for griff-ify avatar."""
    hue = random.random()
    dark_variant = random.choice([True, False])

    color = tuple(int(color * 256) for color in hls_to_rgb(*make_color(hue, dark_variant)))
    complement = tuple(map(int, complementary(*color)))
    return Colour(color, complement)

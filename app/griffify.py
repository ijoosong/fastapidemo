import random
from collections import namedtuple
from pathlib import Path
from typing import Optional, Tuple
from math import ceil
from PIL import Image, ImageChops, ImageDraw, ImageFont

from .colours import generate_griffify_colours
from .models import Colour

Color = Tuple[int, int, int]
Template = namedtuple("Template", "template base_colour circle circle_colour")

ASSETS_PATH = Path("app") / "assets"
SIZE = (512, 512)


class BubbleLetterArt:
    """Generates a random bubble letter art with the specified name or with the options passed in."""

    def __init__(self):
        self.output: Image.Image = Image.new("RGBA", SIZE, color=(0, 0, 0, 0))
        self.circles = {
            filename.stem: Image.open(filename) for filename in (ASSETS_PATH / "hand_drawn_circles").iterdir()
        }
        self.fonts = {
            filename.stem: filename for filename in (ASSETS_PATH / "fonts").iterdir()
        }

    def generate_template(self, base_colour: Color, circle_colour: Color) -> Template:
        """Generate a griff-ify avatar structure from given configuration."""
        circle = random.choice(list(self.circles))
        template = {
            "base": (
                Image.open(ASSETS_PATH / "grey base circle.png"),
                base_colour
            ),
            "circle": (
                Image.open(ASSETS_PATH / f"hand_drawn_circles/{circle}.png"),
                circle_colour
            )
        }

        return Template(template, base_colour, circle, circle_colour)

    def generate(self, letter: str, options: Optional[Colour] = None) -> Image.Image:
        """Generate a nice griffy-ify avatar."""
        if not options:
            colour = generate_griffify_colours()
        else:
            colour = options.dict()["base"], options.dict()["circle"]

        template = self.generate_template(*colour).template

        for item in template.values():
            self.apply_layer(*item)

        # Apply the letter
        font_fname = random.choice(list(self.fonts))
        font = ImageFont.truetype(
            f"app/assets/fonts/{font_fname}.ttf", 215, encoding="unic"
        )

        w_image, h_image = self.output.size
        draw = ImageDraw.Draw(self.output)
        w_text, h_text = draw.textsize(letter, font)
        xy = ceil((w_image-w_text)/2), ceil((h_image-h_text)/2)

        draw.text(xy, letter, colour.circle, font)

        return self.output

    def apply_layer(self, layer: Image.Image, recolor: Optional[Color] = None) -> None:
        """Add the given layer on top of the avatar. Can be recolored with the recolor argument."""
        if recolor:
            if isinstance(recolor, dict):
                recolor = tuple(recolor.values())
            layer = ImageChops.multiply(layer, Image.new("RGBA", SIZE, color=recolor))
        self.output.alpha_composite(layer)

import pygame
from pygame import base
from pygame import constants


class SpriteSheet:
    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert()
        except base.error as error:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(error) from error

    def image_at(self, rectangle, colorkey=None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, constants.RLEACCEL)
        return image

    def images_at(self, rects, colorkey=None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        """Load a whole strip of images, and return them as a list."""
        tups = [
            (rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
            for x in range(image_count)
        ]
        return self.images_at(tups, colorkey)

    def load_grid_images(
        self,
        num_rows,
        num_cols,
        x_margin=0,
        x_padding=0,
        y_margin=0,
        y_padding=0,
    ):
        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size

        x_sprite_size = (
            sheet_width - 2 * x_margin - (num_cols - 1) * x_padding
        ) / num_cols
        y_sprite_size = (
            sheet_height - 2 * y_margin - (num_rows - 1) * y_padding
        ) / num_rows

        rects = [
            (
                x_margin + col * (x_sprite_size + x_padding),
                y_margin + row * (y_sprite_size + y_padding),
                x_sprite_size,
                y_sprite_size,
            )
            for row in range(num_rows)
            for col in range(num_cols)
        ]

        return self.images_at(rects, colorkey=(255, 0, 255))

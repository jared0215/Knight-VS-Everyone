import pygame
import pytmx
from pytmx.util_pygame import load_pygame


class Level:
    def __init__(self, filename, tile_scale):
        self.tmx_data = load_pygame(filename)
        self.tile_scale = tile_scale

    def draw(self, screen):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        # Scale the tile
                        tile_scaled = pygame.transform.scale(tile, (int(self.tmx_data.tilewidth * self.tile_scale),
                                                                    int(self.tmx_data.tileheight * self.tile_scale)))
                        screen.blit(tile_scaled, (x * self.tmx_data.tilewidth * self.tile_scale,
                                                  y * self.tmx_data.tileheight * self.tile_scale))

    # Add more methods as needed, e.g., for handling collisions, events, etc.

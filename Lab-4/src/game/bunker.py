import pygame

class BunkerBlock:
    def __init__(self, x, y, size=6):
        self.x = x
        self.y = y
        self.size = size
        self.alive = True

    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

class Bunker:
    def __init__(self, start_x, start_y, block_size=6):
        self.start_x = start_x
        self.start_y = start_y
        self.block_size = block_size
        self.blocks = []
        self._build_shape()

    def _build_shape(self):
        pattern = [
            [0, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1]
        ]
        self.blocks = []
        for r_idx, row in enumerate(pattern):
            for c_idx, val in enumerate(row):
                if val == 1:
                    bx = self.start_x + c_idx * self.block_size
                    by = self.start_y + r_idx * self.block_size
                    self.blocks.append(BunkerBlock(bx, by, self.block_size))

    def reset(self):
        for block in self.blocks:
            block.alive = True

    def alive_blocks(self):
        return [b for b in self.blocks if b.alive]

    def collide_bullet(self, bullet):
        b_rect = bullet.rect()
        for block in self.blocks:
            if block.alive and block.rect().colliderect(b_rect):
                block.alive = False
                return True
        return False

    def render(self, screen):
        color = (0, 220, 110)
        for block in self.blocks:
            if block.alive:
                pygame.draw.rect(screen, color, block.rect())

import pygame

class Bullet:
    def __init__(self, x, y, width=4, height=12, speed=8, direction=-1, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.prev_y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.direction = direction
        self.color = color

    def move(self):
        self.prev_y = self.y
        self.y += self.speed * self.direction

    def off_screen(self, screen_height):
        return self.y < -self.height or self.y > screen_height + self.height

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def swept_rect(self):
        min_y = min(self.y, self.prev_y)
        total_h = abs(self.y - self.prev_y) + self.height
        return pygame.Rect(int(self.x), int(min_y), self.width, int(total_h))

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect())

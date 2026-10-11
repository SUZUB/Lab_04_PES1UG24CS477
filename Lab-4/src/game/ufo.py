import random
import pygame

class MysteryUFO:
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.width = 46
        self.height = 18
        self.y = 42
        self.x = -self.width
        self.speed = 3
        self.direction = 1
        self.active = False
        self.points = 100
        self.timer = random.randint(400, 700)

    def spawn(self):
        self.direction = 1 if random.random() < 0.5 else -1
        if self.direction == 1:
            self.x = -self.width
        else:
            self.x = self.screen_width
        self.points = random.choice([50, 100, 150, 300])
        self.active = True

    def update(self):
        if not self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.spawn()
                self.timer = random.randint(600, 1000)
            return

        self.x += self.speed * self.direction
        if self.direction == 1 and self.x > self.screen_width:
            self.active = False
        elif self.direction == -1 and self.x < -self.width:
            self.active = False

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def render(self, screen):
        if not self.active:
            return
        rx = int(self.x)
        ry = int(self.y)
        w = self.width
        h = self.height

        saucer_color = (255, 40, 40)
        dome_color = (255, 180, 50)
        window_color = (255, 255, 255)

        base_rect = pygame.Rect(rx + 4, ry + 6, w - 8, h - 8)
        pygame.draw.rect(screen, saucer_color, base_rect, border_radius=4)

        dome_rect = pygame.Rect(rx + 14, ry + 1, w - 28, 7)
        pygame.draw.rect(screen, dome_color, dome_rect, border_radius=3)

        for wx in [rx + 10, rx + 18, rx + 26, rx + 34]:
            pygame.draw.rect(screen, window_color, pygame.Rect(wx, ry + 9, 3, 3))

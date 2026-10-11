import pygame

class Player:
    def __init__(self, x, y, width=44, height=22):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 6
        self.lives = 3
        self.invulnerable_timer = 0

    def move(self, dx, screen_width):
        self.x += dx
        self.x = max(0, min(self.x, screen_width - self.width))

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def center_x(self):
        return int(self.x + self.width // 2)

    def hit(self):
        if self.invulnerable_timer <= 0:
            self.lives -= 1
            self.invulnerable_timer = 60
            return True
        return False

    def is_alive(self):
        return self.lives > 0

    def update(self):
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1

    def reset_position(self):
        self.x = self.start_x
        self.y = self.start_y
        self.invulnerable_timer = 45

    def reset_full(self):
        self.x = self.start_x
        self.y = self.start_y
        self.lives = 3
        self.invulnerable_timer = 0

    def render(self, screen):
        if self.invulnerable_timer > 0 and (self.invulnerable_timer // 6) % 2 == 1:
            return
        base_rect = pygame.Rect(int(self.x), int(self.y + 8), self.width, self.height - 8)
        pygame.draw.rect(screen, (0, 230, 80), base_rect, border_radius=3)
        mid_w = int(self.width * 0.55)
        mid_x = int(self.x + (self.width - mid_w) // 2)
        mid_rect = pygame.Rect(mid_x, int(self.y + 3), mid_w, 7)
        pygame.draw.rect(screen, (0, 255, 100), mid_rect, border_radius=2)
        cannon_w = 4
        cannon_h = 7
        cannon_x = int(self.center_x() - cannon_w // 2)
        cannon_rect = pygame.Rect(cannon_x, int(self.y - 2), cannon_w, cannon_h)
        pygame.draw.rect(screen, (200, 255, 200), cannon_rect)

import pygame

class Enemy:
    def __init__(self, x, y, row=0, width=38, height=24):
        self.x = x
        self.y = y
        self.row = row
        self.width = width
        self.height = height
        self.alive = True
        if self.row == 0:
            self.points = 30
            self.color = (240, 70, 160)
        elif self.row in (1, 2):
            self.points = 20
            self.color = (50, 215, 240)
        else:
            self.points = 10
            self.color = (240, 230, 60)

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def render(self, screen, anim):
        if not self.alive:
            return
        rx = int(self.x)
        ry = int(self.y)
        w = self.width
        h = self.height

        if self.row == 0:
            body = pygame.Rect(rx + 6, ry + 4, w - 12, h - 8)
            pygame.draw.rect(screen, self.color, body, border_radius=4)
            top = pygame.Rect(rx + 10, ry, w - 20, 5)
            pygame.draw.rect(screen, self.color, top)
            eye_y = ry + 7
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(rx + 10, eye_y, 4, 4))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(rx + w - 14, eye_y, 4, 4))
            if anim:
                pygame.draw.rect(screen, self.color, pygame.Rect(rx + 2, ry + h - 5, 5, 5))
                pygame.draw.rect(screen, self.color, pygame.Rect(rx + w - 7, ry + h - 5, 5, 5))
            else:
                pygame.draw.rect(screen, self.color, pygame.Rect(rx + 6, ry + h - 4, 5, 4))
                pygame.draw.rect(screen, self.color, pygame.Rect(rx + w - 11, ry + h - 4, 5, 4))

        elif self.row in (1, 2):
            body = pygame.Rect(rx + 4, ry + 5, w - 8, h - 10)
            pygame.draw.rect(screen, self.color, body, border_radius=3)
            pygame.draw.rect(screen, self.color, pygame.Rect(rx + 8, ry + 1, 4, 5))
            pygame.draw.rect(screen, self.color, pygame.Rect(rx + w - 12, ry + 1, 4, 5))
            eye_y = ry + 8
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(rx + 9, eye_y, 4, 4))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(rx + w - 13, eye_y, 4, 4))
            if anim:
                pygame.draw.rect(screen, self.color, pygame.Rect(rx, ry + 8, 4, 8))
                pygame.draw.rect(screen, self.color, pygame.Rect(rx + w - 4, ry + 8, 4, 8))
                pygame.draw.rect(screen, self.color, pygame.Rect(rx + 7, ry + h - 4, 5, 4))
                pygame.draw.rect(screen, self.color, pygame.Rect(rx + w - 12, ry + h - 4, 5, 4))
            else:
                pygame.draw.rect(screen, self.color, pygame.Rect(rx + 2, ry + 12, 4, 6))
                pygame.draw.rect(screen, self.color, pygame.Rect(rx + w - 6, ry + 12, 4, 6))
                pygame.draw.rect(screen, self.color, pygame.Rect(rx + 11, ry + h - 4, 5, 4))
                pygame.draw.rect(screen, self.color, pygame.Rect(rx + w - 16, ry + h - 4, 5, 4))

        else:
            body = pygame.Rect(rx + 5, ry + 3, w - 10, h - 8)
            pygame.draw.rect(screen, self.color, body, border_radius=5)
            eye_y = ry + 7
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(rx + 10, eye_y, 4, 4))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(rx + w - 14, eye_y, 4, 4))
            if anim:
                pygame.draw.rect(screen, self.color, pygame.Rect(rx + 4, ry + h - 5, 4, 5))
                pygame.draw.rect(screen, self.color, pygame.Rect(rx + 14, ry + h - 4, 4, 4))
                pygame.draw.rect(screen, self.color, pygame.Rect(rx + w - 18, ry + h - 4, 4, 4))
                pygame.draw.rect(screen, self.color, pygame.Rect(rx + w - 8, ry + h - 5, 4, 5))
            else:
                pygame.draw.rect(screen, self.color, pygame.Rect(rx + 7, ry + h - 5, 4, 5))
                pygame.draw.rect(screen, self.color, pygame.Rect(rx + 12, ry + h - 5, 4, 5))
                pygame.draw.rect(screen, self.color, pygame.Rect(rx + w - 16, ry + h - 5, 4, 5))
                pygame.draw.rect(screen, self.color, pygame.Rect(rx + w - 11, ry + h - 5, 4, 5))

class EnemyGrid:
    def __init__(self, screen_width, rows=4, cols=8, base_speed=1.5, drop_amount=20):
        self.screen_width = screen_width
        self.rows = rows
        self.cols = cols
        self.base_speed = base_speed
        self.speed = base_speed
        self.drop_amount = drop_amount
        self.direction = 1
        self.anim_toggle = False
        self.anim_counter = 0
        self.enemies = []
        self._build_grid()

    def _build_grid(self):
        self.enemies = []
        spacing_x = 54
        spacing_y = 42
        start_x = (self.screen_width - (self.cols * spacing_x)) // 2 + 10
        start_y = 75
        for row in range(self.rows):
            for col in range(self.cols):
                x = start_x + col * spacing_x
                y = start_y + row * spacing_y
                self.enemies.append(Enemy(x, y, row=row))

    def reset(self, base_speed=None, drop_amount=None):
        if base_speed is not None:
            self.base_speed = base_speed
        if drop_amount is not None:
            self.drop_amount = drop_amount
        self.speed = self.base_speed
        self.direction = 1
        self.anim_toggle = False
        self.anim_counter = 0
        self._build_grid()

    def alive_enemies(self):
        return [e for e in self.enemies if e.alive]

    def move(self):
        alive = self.alive_enemies()
        if not alive:
            return

        total = self.rows * self.cols
        alive_count = len(alive)
        speed_boost = 1.0 + (1.0 - alive_count / total) * 0.85
        current_speed = self.speed * speed_boost

        self.anim_counter += 1
        anim_threshold = max(10, int(30 * (alive_count / total)))
        if self.anim_counter >= anim_threshold:
            self.anim_toggle = not self.anim_toggle
            self.anim_counter = 0

        min_x = min(e.x for e in alive)
        max_x = max(e.x + e.width for e in alive)

        hit_edge = (self.direction == 1 and max_x + current_speed >= self.screen_width - 15) or \
                   (self.direction == -1 and min_x - current_speed <= 15)

        if hit_edge:
            self.direction *= -1
            for e in alive:
                e.y += self.drop_amount
        else:
            for e in alive:
                e.x += current_speed * self.direction

    def reached_bottom(self, limit_y):
        return any(e.y + e.height >= limit_y for e in self.alive_enemies())

    def render(self, screen):
        for e in self.enemies:
            e.render(screen, self.anim_toggle)

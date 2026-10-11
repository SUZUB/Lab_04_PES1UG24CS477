import random
import pygame
from .player import Player
from .enemy import EnemyGrid
from .bullet import Bullet
from .bunker import Bunker
from .ufo import MysteryUFO
from .sound import SoundManager

WHITE = (255, 255, 255)
GRAY = (140, 140, 140)
DARK_GRAY = (30, 30, 30)
GREEN = (0, 230, 80)
RED = (240, 60, 60)
YELLOW = (250, 220, 50)
CYAN = (60, 220, 255)

class GameEngine:
    DIFFICULTIES = {
        "1": {"name": "Easy", "speed": 1.0, "fire_chance": 0.005, "drop": 16},
        "2": {"name": "Medium", "speed": 1.5, "fire_chance": 0.010, "drop": 20},
        "3": {"name": "Hard", "speed": 2.2, "fire_chance": 0.020, "drop": 24}
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.sound = SoundManager()
        self.high_score = 0
        self.difficulty_key = "2"
        self.font_large = pygame.font.SysFont("Arial", 40, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 16)
        self.ufo = MysteryUFO(width)
        self.bunkers = []
        self._init_bunkers()
        self.start_new_game(self.difficulty_key)

    def _init_bunkers(self):
        self.bunkers = []
        positions = [70, 200, 330, 460]
        by = self.height - 140
        for bx in positions:
            self.bunkers.append(Bunker(bx, by, block_size=6))

    def start_new_game(self, diff_key="2"):
        if diff_key in self.DIFFICULTIES:
            self.difficulty_key = diff_key
        config = self.DIFFICULTIES[self.difficulty_key]
        self.difficulty_name = config["name"]
        self.enemy_fire_chance = config["fire_chance"]

        self.player = Player(self.width // 2 - 22, self.height - 50, 44, 22)
        self.enemy_grid = EnemyGrid(
            self.width,
            rows=4,
            cols=8,
            base_speed=config["speed"],
            drop_amount=config["drop"]
        )
        for bunker in self.bunkers:
            bunker.reset()
        self.ufo.active = False
        self.ufo.timer = random.randint(300, 600)

        self.player_bullets = []
        self.enemy_bullets = []
        self._shoot_cooldown = 0
        self.score = 0
        self.game_over = False
        self.state = "PLAYING"

    def handle_event(self, event):
        if self.state in ("GAME_OVER", "VICTORY"):
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_1, pygame.K_KP1, pygame.K_e):
                    self.start_new_game("1")
                elif event.key in (pygame.K_2, pygame.K_KP2, pygame.K_m):
                    self.start_new_game("2")
                elif event.key in (pygame.K_3, pygame.K_KP3, pygame.K_h):
                    self.start_new_game("3")
                elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    self.start_new_game(self.difficulty_key)
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self._shoot_cooldown <= 0:
                bullet_x = self.player.center_x() - 2
                self.player_bullets.append(
                    Bullet(bullet_x, self.player.y, direction=-1, color=(255, 255, 255))
                )
                self._shoot_cooldown = 14
                self.sound.play_laser()

    def handle_input(self):
        if self.state != "PLAYING":
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move(-self.player.speed, self.width)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move(self.player.speed, self.width)

    def update(self):
        if self.state != "PLAYING":
            return

        self.player.update()
        if self._shoot_cooldown > 0:
            self._shoot_cooldown -= 1

        self.enemy_grid.move()
        self.ufo.update()

        for enemy in self.enemy_grid.alive_enemies():
            if random.random() < self.enemy_fire_chance:
                bullet_x = enemy.x + enemy.width // 2
                self.enemy_bullets.append(
                    Bullet(bullet_x, enemy.y + enemy.height, direction=1, color=RED)
                )

        for bullet in self.player_bullets:
            bullet.move()
        for bullet in self.enemy_bullets:
            bullet.move()

        self.player_bullets = [b for b in self.player_bullets if not b.off_screen(self.height)]
        self.enemy_bullets = [b for b in self.enemy_bullets if not b.off_screen(self.height)]

        bullets_to_remove = set()
        for bullet in self.player_bullets:
            bullet_rect = bullet.swept_rect()
            for enemy in self.enemy_grid.alive_enemies():
                if bullet_rect.colliderect(enemy.rect()):
                    enemy.alive = False
                    bullets_to_remove.add(bullet)
                    self.score += enemy.points
                    self.sound.play_explosion()
                    break
        self.player_bullets = [b for b in self.player_bullets if b not in bullets_to_remove]

        if self.ufo.active:
            ufo_rect = self.ufo.rect()
            for bullet in list(self.player_bullets):
                if bullet.rect().colliderect(ufo_rect):
                    self.score += self.ufo.points
                    self.ufo.active = False
                    if bullet in self.player_bullets:
                        self.player_bullets.remove(bullet)
                    self.sound.play_explosion()
                    break

        for bunker in self.bunkers:
            for bullet in list(self.player_bullets):
                if bunker.collide_bullet(bullet):
                    if bullet in self.player_bullets:
                        self.player_bullets.remove(bullet)
            for bullet in list(self.enemy_bullets):
                if bunker.collide_bullet(bullet):
                    if bullet in self.enemy_bullets:
                        self.enemy_bullets.remove(bullet)

        for bullet in list(self.enemy_bullets):
            if bullet.rect().colliderect(self.player.rect()):
                self.enemy_bullets.remove(bullet)
                if self.player.hit():
                    self.sound.play_hit()
                    if not self.player.is_alive():
                        self.game_over = True
                        self.state = "GAME_OVER"
                        self.sound.play_game_over()
                    else:
                        self.player.reset_position()
                break

        if self.enemy_grid.reached_bottom(self.player.y):
            self.player.lives = 0
            self.game_over = True
            self.state = "GAME_OVER"
            self.sound.play_game_over()

        if not self.enemy_grid.alive_enemies():
            self.state = "VICTORY"
            self.score += 500
            self.sound.play_explosion()

        if self.score > self.high_score:
            self.high_score = self.score

    def render(self, screen):
        self._render_hud(screen)
        for bunker in self.bunkers:
            bunker.render(screen)
        self.ufo.render(screen)
        self.enemy_grid.render(screen)
        for bullet in self.player_bullets:
            bullet.render(screen)
        for bullet in self.enemy_bullets:
            bullet.render(screen)
        self.player.render(screen)

        if self.state in ("GAME_OVER", "VICTORY"):
            self._render_overlay(screen)

    def _render_hud(self, screen):
        score_surf = self.font_medium.render(f"SCORE: {self.score}", True, WHITE)
        screen.blit(score_surf, (15, 10))

        hi_surf = self.font_small.render(f"HIGH: {self.high_score}", True, YELLOW)
        screen.blit(hi_surf, (self.width // 2 - hi_surf.get_width() // 2, 14))

        diff_surf = self.font_small.render(f"[{self.difficulty_name.upper()}]", True, CYAN)
        screen.blit(diff_surf, (self.width // 2 - diff_surf.get_width() // 2, 34))

        lives_label = self.font_small.render("LIVES:", True, WHITE)
        lx = self.width - 15 - (self.player.lives * 22) - lives_label.get_width() - 8
        screen.blit(lives_label, (lx, 14))
        for i in range(max(0, self.player.lives)):
            rx = self.width - 15 - ((i + 1) * 22)
            pygame.draw.rect(screen, GREEN, pygame.Rect(rx, 15, 16, 8), border_radius=2)
            pygame.draw.rect(screen, (200, 255, 200), pygame.Rect(rx + 6, 12, 4, 4))

        pygame.draw.line(screen, DARK_GRAY, (0, 60), (self.width, 60), 1)

    def _render_overlay(self, screen):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 195))
        screen.blit(overlay, (0, 0))

        panel = pygame.Rect(self.width // 2 - 240, self.height // 2 - 190, 480, 380)
        pygame.draw.rect(screen, (15, 15, 25), panel, border_radius=12)
        border_color = GREEN if self.state == "VICTORY" else RED
        pygame.draw.rect(screen, border_color, panel, width=3, border_radius=12)

        title_text = "VICTORY! WAVE CLEARED" if self.state == "VICTORY" else "GAME OVER"
        title_color = GREEN if self.state == "VICTORY" else RED
        title_surf = self.font_large.render(title_text, True, title_color)
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, panel.y + 30))

        score_surf = self.font_medium.render(f"FINAL SCORE: {self.score}", True, WHITE)
        screen.blit(score_surf, (self.width // 2 - score_surf.get_width() // 2, panel.y + 95))

        hi_surf = self.font_medium.render(f"BEST SCORE: {self.high_score}", True, YELLOW)
        screen.blit(hi_surf, (self.width // 2 - hi_surf.get_width() // 2, panel.y + 130))

        div_y = panel.y + 175
        pygame.draw.line(screen, (60, 60, 80), (panel.x + 30, div_y), (panel.x + panel.w - 30, div_y), 1)

        opt_title = self.font_medium.render("SELECT DIFFICULTY TO REPLAY:", True, CYAN)
        screen.blit(opt_title, (self.width // 2 - opt_title.get_width() // 2, panel.y + 195))

        options = [
            ("[1] EASY", "Speed: 1.0  |  Fire: Low"),
            ("[2] MEDIUM", "Speed: 1.5  |  Fire: Normal"),
            ("[3] HARD", "Speed: 2.2  |  Fire: Intense")
        ]
        for idx, (label, desc) in enumerate(options):
            opt_y = panel.y + 235 + idx * 26
            opt_s = self.font_small.render(f"{label} - {desc}", True, WHITE)
            screen.blit(opt_s, (self.width // 2 - opt_s.get_width() // 2, opt_y))

        hint_s = self.font_small.render("PRESS [SPACE] QUICK RESTART   |   PRESS [Q] QUIT", True, GRAY)
        screen.blit(hint_s, (self.width // 2 - hint_s.get_width() // 2, panel.y + 325))

from projectiles import *
from resources import *

class Boss():
    def __init__(self, x, y):
        # Sprites
        self.sprites = []
        for i in range(1, 7):
            self.sprites.append(
                pygame.transform.scale(
                    pygame.image.load(f'assets/boss sprites/boss{i}.png'), (64, 64)
                )
            )
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.health = 5000
        self.max_health = 5000
        self.radius = 50

        # Movement properties
        self.vel = 2
        self.direction = 1
        self.moving = False

        self.patterns = {
            "phase1": {
                "pattern1": [
                    {"count": 8, "delay": 150, "repetition": 25, "current_repetition": 0, "last_shot_time": 0},
                    {"count": 30, "delay": 1000, "repetition": 4, "current_repetition": 0, "last_shot_time": 0}
                ],
                "pattern2": [
                    {"count": 30, "delay": 1000, "repetition": 5, "current_repetition": 0, "last_shot_time": 0},
                    {"count": 4, "delay": 100, "repetition": 25, "current_repetition": 0, "last_shot_time": 0}
                ]
            },
            "phase2": {
                "pattern1": [
                    {"count": 6, "delay": 100, "repetition": 35, "current_repetition": 0, "last_shot_time": 0},
                    {"count": 30, "delay": 700, "repetition": 6, "current_repetition": 0, "last_shot_time": 0}
                ],
                "pattern2": [
                    {"count": 5, "delay": 150, "repetition": 24, "current_repetition": 0, "last_shot_time": 0},
                    {"count": 15, "delay": 350, "repetition": 12, "current_repetition": 0, "last_shot_time": 0}
                ]
            },
            "phase3": {
                "pattern1": [
                    {"count": 4, "delay": 200, "repetition": 30, "current_repetition": 0, "last_shot_time": 0},
                    {"count": 40, "delay": 1100, "repetition": 5, "current_repetition": 0, "last_shot_time": 0}
                ],
                "pattern2": [
                    {"count": 4, "delay": 200, "repetition": 40, "current_repetition": 0, "last_shot_time": 0},
                    {"count": 40, "delay": 1100, "repetition": 5, "current_repetition": 0, "last_shot_time": 0}
                ]
            }
        }

        self.current_phase = "phase1"
        self.current_pattern_key = "pattern1"
        self.current_pattern_index = 0
        self.cooldown_start_time = 0
        self.cooldown_duration = 2500  # 3 seconds
        self.in_cooldown = False

    def shoot(self, bullets):
        # Check for phase transition
        if self.health <= self.max_health / 2 and self.current_phase == "phase1":
            self.current_phase = "phase2"
            self.current_pattern_key = "pattern1"
            self.current_pattern_index = 0
            self.in_cooldown = False
            self.reset_patterns("phase2")  # Reset phase2 patterns to ensure smooth transition

        if self.health <= 1000 and self.current_phase != "phase3":
            self.current_phase = "phase3"
            self.current_pattern_key = "pattern1"
            self.current_pattern_index = 0
            self.in_cooldown = False
            self.reset_patterns("phase3")

        if self.in_cooldown:
            current_time = pygame.time.get_ticks()
            if current_time - self.cooldown_start_time >= self.cooldown_duration:
                # Cooldown is over; switch to the next pattern
                self.in_cooldown = False
                self.switch_to_next_pattern()
            return

        # Get current pattern
        current_patterns = self.patterns[self.current_phase][self.current_pattern_key]

        # Spawn bullets for all sub-patterns in the current pattern
        all_done = True
        for pattern in current_patterns:
            self.spawn_bullets_in_circle(bullets, pattern)
            if pattern["current_repetition"] < pattern["repetition"]:
                all_done = False

        # If all repetitions are complete, start cooldown
        if all_done:
            self.in_cooldown = True
            self.cooldown_start_time = pygame.time.get_ticks()

    def reset_patterns(self, phase):
        """Resets the patterns of a given phase to their initial state."""
        for key in self.patterns[phase]:
            for pattern in self.patterns[phase][key]:
                pattern["current_repetition"] = 0
                pattern["last_shot_time"] = 0

    def spawn_bullets_in_circle(self, bullets, pattern):
        current_time = pygame.time.get_ticks()

        self.current_angle = (current_time // 10) % 360  # Rotate every 100 milliseconds
        step = 2 * math.pi / pattern["count"]

        if pattern["current_repetition"] < pattern["repetition"]:

            if current_time - pattern["last_shot_time"] >= pattern["delay"]:
                pattern["current_repetition"] += 1

                for i in range(pattern["count"]):
                    angle = step * i + math.radians(self.current_angle)

                    spawn_x = self.rect.centerx + self.radius * math.cos(angle)
                    spawn_y = self.rect.centery + self.radius * math.sin(angle)

                    bullets.append(Bullet(spawn_x, spawn_y, angle))

                pattern["last_shot_time"] = current_time

    def switch_to_next_pattern(self):
        # Move to the next pattern in the current phase
        phase_patterns = list(self.patterns[self.current_phase].keys())
        self.current_pattern_index = (self.current_pattern_index + 1) % len(phase_patterns)
        self.current_pattern_key = phase_patterns[self.current_pattern_index]

        # Reset all sub-patterns for the new pattern
        for pattern in self.patterns[self.current_phase][self.current_pattern_key]:
            pattern["current_repetition"] = 0
            pattern["last_shot_time"] = 0

    def move(self):
        if self.health <= 1000:
            self.moving = True

        if self.moving:
            self.rect.x += self.vel * self.direction

            if self.rect.right >= 400:
                self.rect.right = 400  # Snap to boundary
                self.direction = -1

            if self.rect.left <= 50:
                self.rect.left = 50  # Snap to boundary
                self.direction = 1  # Reverse direction

    def draw_health_bar(self):

        """Draw the boss's health bar above it."""
        bar_width = 200  # Width of the health bar
        bar_height = 6  # Height of the health bar
        bar_x = 120  # X position of the health bar
        bar_y = 130  # Y position of the health bar (above the boss)

        health_bar = pygame.image.load('assets/boss sprites/health bar.png')

        # Background bar (full health)
        base_surface.blit(health_bar, (bar_x, bar_y))

        # Foreground bar (current health)
        current_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(base_surface, health_bar_color, (bar_x + 1, bar_y + 1, current_width - 2, bar_height))

    def draw(self):
        self.current_sprite += 0.2

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]
        base_surface.blit(self.image, self.rect)
        self.draw_health_bar()
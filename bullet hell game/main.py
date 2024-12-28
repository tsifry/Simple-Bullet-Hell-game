import pygame
import math

from resources import *
from boss import *
from projectiles import *

class Player():
    def __init__(self, x, y):
        # Sprites
        self.player_image = pygame.transform.scale(pygame.image.load('assets/player_idle.png').convert_alpha(),(16, 16))
        self.player_left = pygame.transform.scale(pygame.image.load('assets/player_left.png').convert_alpha(), (16, 16))
        self.player_right = pygame.transform.scale(pygame.image.load('assets/player_right.png').convert_alpha(),(16, 16))
        self.player_top = pygame.transform.scale(pygame.image.load('assets/player_top.png').convert_alpha(), (16, 16))
        self.player_bot = pygame.transform.scale(pygame.image.load('assets/player_bot.png').convert_alpha(), (16, 16))
        self.is_moving = False

        self.image = self.player_image
        self.width = 16
        self.height = 16
        self.health = 6
        self.max_health = 6
        self.vel = 4

        self.x = x
        self.y = y

        # shooting
        self.shoot_cooldown = 200  # Time in milliseconds between shots
        self.last_shot_time = pygame.time.get_ticks()

        # Collision
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.flip = False

    def move(self):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if keys[pygame.K_a]:  # left
            if self.rect.left - self.vel > 0:
                dx -= self.vel
                self.image = self.player_left
            else:
                self.rect.left = 0  # Snap to the boundary

        if keys[pygame.K_d]:  # right
            if self.rect.right + self.vel < SCREEN_WIDTH:
                dx += self.vel
                self.image = self.player_right
            else:
                self.rect.right = SCREEN_WIDTH  # Snap to the boundary

        if keys[pygame.K_w]:  # up
            if self.rect.top - self.vel > 0:
                dy -= self.vel
                self.image = self.player_top
            else:
                self.rect.top = 0  # Snap to the boundary

        if keys[pygame.K_s]:  # down
            if self.rect.bottom + self.vel < SCREEN_HEIGHT:
                dy += self.vel
                self.image = self.player_bot
            else:
                self.rect.bottom = SCREEN_HEIGHT  # Snap to the boundary

        if not (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]):
            self.image = self.player_image

        # Normalize vector
        length = math.sqrt(dx ** 2 + dy ** 2)
        if length > 0:
            dx /= length
            dy /= length

        # Apply movement
        self.rect.x += dx * player.vel
        self.rect.y += dy * player.vel

    def draw(self):
        # Draw the current frame
        base_surface.blit(self.image, (self.rect.centerx - self.width // 2, self.rect.centery - self.height // 2))

        # Draw health bar
        full_heart = pygame.image.load('assets/full_heart.png').convert_alpha()
        broken_heart = pygame.image.load('assets/broken_heart..png').convert_alpha()

        for heart in range(self.health):
            base_surface.blit(full_heart, (heart * 20, 45))

        for heart in range(self.max_health):
            if heart < self.health:
                base_surface.blit(full_heart, (heart * 20, 45))
            else:
                base_surface.blit(broken_heart, (heart * 20, 45))

    def get_center(self):
        return self.rect.x + self.width / 2, self.rect.y + self.height / 2

    def shoot(self):

        # Timing bullets
        current_time = pygame.time.get_ticks()

        # Get mouse pos
        mouse_pos = pygame.mouse.get_pos()

        # Cursor stuff
        pygame.mouse.set_visible(False)
        cursor_image = get_cursor_image(3, 3)
        base_surface.blit(cursor_image, (mouse_pos[0] - tile, mouse_pos[1] - tile))

        # Shooting
        if pygame.mouse.get_pressed()[0] and current_time - self.last_shot_time >= self.shoot_cooldown:
            self.last_shot_time = current_time

            # Get the mouse position and calculate direction
            mouse_pos = pygame.mouse.get_pos()
            direction = pygame.Vector2(mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery)
            direction.normalize()

            # Create a new player projectile
            projectiles.append(PlayerProjectile(self.rect.centerx, self.rect.centery, direction))

            # sfx
            player_shooting = pygame.mixer.Sound("assets/player_shooting.wav")
            player_shooting.play()

    def damage(self):
        # sfx
        player_hit = pygame.mixer.Sound("assets/player_hit.mp3")
        player_hit.set_volume(0.4)

        if self.health > 0:
            self.health -= 1
            player_hit.play()

player = Player(SCREEN_WIDTH // 2, 450)
boss = Boss(SCREEN_WIDTH // 2, 200)
bullets = []
projectiles = []

# Rendering stuff
def redraw_window():
    base_surface.fill((0, 0, 0))

    player.draw()
    boss.draw()

    # Draw bullets
    for bullet in bullets:
        bullet.draw()

    for proj in projectiles:
        proj.draw()

    player.shoot()

    scaled_screen.blit(pygame.transform.scale(base_surface, (SCALED_WIDTH, SCALED_HEIGHT)), (0, 0))
    pygame.draw.rect(base_surface, (255, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 2)
    pygame.display.flip()

# Main game
def play():
    global player, boss, bullets, projectiles
    run = True

    mixer.music.stop()
    mixer.music.load("assets/music.mp3")
    mixer.music.play(-1)
    mixer.music.set_volume(0.3)

    player = Player(SCREEN_WIDTH // 2, 450)
    boss = Boss(SCREEN_WIDTH // 2, 200)
    bullets = []  # List to store BOSS projectiles
    projectiles = []  # List to store PLAYER projectiles

    while run:

        base_surface.fill((0, 0, 0))
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #Player and boss actions
        player.move()
        player.shoot()
        boss.move()
        boss.shoot(bullets)

        for i in bullets:
            i.update()
            if i.col(player):
                bullets.remove(i)

            if i.x < 0 or i.x > SCREEN_WIDTH or i.y < 0 or i.y > SCREEN_HEIGHT:
                bullets.remove(i)

        for j in projectiles:
            j.update()
            if j.col(boss):
                projectiles.remove(j)

            if j.x < 0 or j.x > SCREEN_WIDTH or j.y < 0 or j.y > SCREEN_HEIGHT:
                projectiles.remove(j)

        if player.health <= 0:
            run = False
            mixer.music.stop()
            lose()

        if boss.health <= 0:
            win()
            run = False

        # Update the entire display after drawing
        redraw_window()

    pygame.quit()


# Menus
def draw_text(text, font, text_col, x, y):
    textobj = font.render(text, True, text_col)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    scaled_screen.blit(textobj, (x, y))

def menu():
    run = True
    click = False
    while run:

        base_surface.fill((0, 0, 0))

        draw_text("Play", MAIN_FONT, FONT_COLOR, 395, 250)
        draw_text("Exit", MAIN_FONT, FONT_COLOR, 395, 390)
        draw_text("W-A-S-D / Move", MAIN_FONT, FONT_COLOR, 325, 600)
        draw_text("Mouse1 / Shoot", MAIN_FONT, FONT_COLOR, 325, 630)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(240, 220, 390, 90)
        button_2 = pygame.Rect(240, 360, 390, 90)

        if button_1.collidepoint((mx, my)) and click:
            play()
            return

        if button_2.collidepoint((mx, my)) and click:
            pygame.quit()
            exit()

        pygame.draw.rect(scaled_screen, white, button_1, width=1)
        pygame.draw.rect(scaled_screen, white, button_2, width=1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()# Exit the loop when QUIT event occurs
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def lose():
    run = True
    click = False
    while run:
        scaled_screen.fill((0, 0, 0))

        # Draw buttons and text
        draw_text("You lost!", MAIN_FONT, FONT_COLOR, 370, 600)
        draw_text("Retry", MAIN_FONT, FONT_COLOR, 400, 250)
        draw_text("Exit", MAIN_FONT, FONT_COLOR, 400, 390)

        button_1 = pygame.Rect(240, 220, 390, 90)
        button_2 = pygame.Rect(240, 360, 390, 90)

        mx, my = pygame.mouse.get_pos()
        pygame.mouse.set_visible(True)

        if button_1.collidepoint((mx, my)) and click:
            play()
            return

        if button_2.collidepoint((mx, my)) and click:
            pygame.quit()
            exit()

        pygame.draw.rect(scaled_screen, white, button_1, width=1)
        pygame.draw.rect(scaled_screen, white, button_2, width=1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()#
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def win():
    run = True
    click = False
    while run:
        scaled_screen.fill((0, 0, 0))

        # Draw buttons and text
        draw_text("You Win!", MAIN_FONT, FONT_COLOR, 370, 600)
        draw_text("Replay", MAIN_FONT, FONT_COLOR, 400, 250)
        draw_text("Exit", MAIN_FONT, FONT_COLOR, 400, 390)

        button_1 = pygame.Rect(240, 220, 390, 90)
        button_2 = pygame.Rect(240, 360, 390, 90)

        mx, my = pygame.mouse.get_pos()
        pygame.mouse.set_visible(True)

        if button_1.collidepoint((mx, my)) and click:
            play()
            return

        if button_2.collidepoint((mx, my)) and click:
            pygame.quit()
            exit()

        pygame.draw.rect(scaled_screen, white, button_1, width=1)
        pygame.draw.rect(scaled_screen, white, button_2, width=1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  #
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


menu()
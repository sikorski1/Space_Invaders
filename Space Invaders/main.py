import pygame
from sys import exit
from player import Player
import obstacles
from aliens import Alien
import random
from laser import Laser
from aliens import Extra


class Game:
    def __init__(self):
        # Player
        player_sprite = Player((screen_width / 2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        # Lives and score
        self.lives = 3
        self.lives_surf = pygame.image.load("graphics/player.png").convert_alpha()
        self.lives_start_x_pos = screen_width - (self.lives_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font("font/Pixeled.ttf", 20)
        # Obstacle
        self.shape = obstacles.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(self.obstacle_x_positions, x_start=screen_width / 14, y_start=480)
        # Alien
        self.aliens = pygame.sprite.Group()
        self.alien_setup(rows=6, cols=8)
        self.alien_direction = 1
        self.alien_laser = pygame.sprite.Group()
        # Extra
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_timer = random.randint(400, 800)



    def create_obstacle(self, offset_x, x_start, y_start, ):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == "x":
                    x = x_start + self.block_size * col_index + offset_x
                    y = y_start + self.block_size * row_index
                    block = obstacles.Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, offset, x_start, y_start, ):
        for offset_x in offset:
            self.create_obstacle(offset_x, x_start, y_start, )

    def alien_setup(self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                if row_index <= 0:
                    alien_sprite = Alien("yellow", x, y)

                elif 0 < row_index <= 2:
                    alien_sprite = Alien("green", x, y)

                elif 2 < row_index <= rows:
                    alien_sprite = Alien("red", x, y)
                self.aliens.add(alien_sprite)

    def alien_postion_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(1)
            if alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(1)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = random.choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, -5, screen_height)
            self.alien_laser.add(laser_sprite)

    def extra_alien_timer(self):
        self.extra_spawn_timer -= 1
        if self.extra_spawn_timer <= 0:
            self.extra.add(Extra(random.choice(["right", "left"]), screen_width))
            self.extra_spawn_timer = random.randint(400, 800)

    def collision_check(self):
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # obstacle
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                # alien
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                # extra
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 500
                    laser.kill()
        if self.alien_laser:
            for laser in self.alien_laser.sprites():
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        exit()

        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)
                if pygame.sprite.spritecollide(alien, self.player, True):
                    pygame.quit()
                    exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.lives_start_x_pos + (live * (self.lives_surf.get_size()[0] + 10))
            screen.blit(self.lives_surf, (x, 8))

    def display_score(self):
        surf = self.font.render("score:  " + str(self.score), True, "white")
        rect = surf.get_rect(topleft=(10, -10))
        screen.blit(surf, rect)

    def run(self):
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_postion_checker()
        self.alien_laser.update()
        self.collision_check()
        self.extra.update()
        self.extra_alien_timer()
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_laser.draw(screen)
        self.extra.draw(screen)
        self.display_lives()
        self.display_score()


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Space Invaders")
    game = Game()
    ALINELASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALINELASER, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == ALINELASER:
                game.alien_shoot()
        screen.fill((30, 30, 30))
        game.run()

        clock.tick(120)
        pygame.display.update()

import pygame, sys
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser


class Game:
    def __init__(self):
        # player setup
        player_sprite = Player((screen_width/2,screen_height),screen_width,5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # health and score setup
        self.lives = 3
        self.live_surf = pygame.image.load('SpaceInvaders/graphics/player.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20) # screen width minus x parameter of live surf
        self.score = 0
        self.font = pygame.font.Font('SpaceInvaders/font/Pixeled.ttf', 20)

        # obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(self.obstacle_x_positions , x_start = screen_width / 15, y_start = 480)

        # alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_list = [
            'yggrrr',
            'yggrrr',
            'yggrrr',
            'yggrrr',
            'yggrrr',
            'yggrrr',
            'yggrrr',
            'yggrrr',
        ]
        self.alien_setup(100, 100, 60, 48)
        self.alien_direction = 1
        self.alien_lasers = pygame.sprite.Group()
        
        # extra setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(40, 80)

        # audio setup
        music = pygame.mixer.Sound('SpaceInvaders/audio/music.wav')
        music.set_volume(0.2)
        music.play(-1)
        self.laser_sound = pygame.mixer.Sound('SpaceInvaders/audio/laser.wav')
        self.laser_sound.set_volume(0.2)
        self.explosion_sound = pygame.mixer.Sound('SpaceInvaders/audio/explosion.wav')
        self.explosion_sound.set_volume(0.3)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape): # The enumerate() method adds a counter to an iterable and returns it (the enumerate object).
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size,(241,79,80),x,y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_setup(self, x_start, y_start, x_offset, y_offset):
        for row_index, row in enumerate(self.alien_list):
            for col_index, col in enumerate(row):
                x = x_start + row_index * x_offset
                y = y_start + col_index * y_offset
                if col == 'r':
                    alien_sprite = Alien('red', x, y)
                elif col == 'g':
                    alien_sprite = Alien('green', x, y)
                elif col == 'y':
                    alien_sprite = Alien('yellow', x, y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)

            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens: # in case player kills all the aliens
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites(): # only run if player hasen't won yet
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 5, self.player.sprite.rect.bottom)
            self.alien_lasers.add(laser_sprite) # have to make a new group for alien lasers, otherwise, each player laser will hit player when we add collision
            self.laser_sound.play()

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right', 'left']), screen_width))
            self.extra_spawn_time = randint(400, 800)

    def game_over(self):
        print('game over')

    def get_hit(self):
        if self.lives != 1:
            self.lives -= 1
        else:
            self.lives -= 1
            print('game over man')
            pygame.quit()
            sys.exit()

    def collision_checks(self):

        # player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                # alien collisions
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens , True)
                if aliens_hit:
                    laser.kill()
                    self.explosion_sound.play()
                    for alien in aliens_hit:
                        self.score += alien.value
                # extra collisions
                if pygame.sprite.spritecollide(laser, self.extra , True):
                    laser.kill()
                    self.score += 500
                    self.explosion_sound.play()

        # alien lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                # player collisions
                if pygame.sprite.spritecollide(laser, self.player , False):
                    laser.kill()
                    self.get_hit()

        # alien block player collision
        if self.aliens:
            for alien in self.aliens:
                # obstacle
                pygame.sprite.spritecollide(alien, self.blocks, True)
                # player
                if pygame.sprite.spritecollide(alien, self.player, False):
                    print('game over man')
                    pygame.quit()
                    sys.exit()
                
    def display_lives(self):
        for live in range(self.lives - 1): # display only 2, 1 and 0 lives
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        self.score_surf = self.font.render(f'Score: {self.score}', False, (64,64,64))
        self.score_rect = self.score_surf.get_rect(topleft = [10, -10])
        screen.blit(self.score_surf, self.score_rect)

    def victory_message(self):
        if not self.aliens.sprites():
            victory_surf = self.font.render('You won!', False, 'white')
            victory_rect = victory_surf.get_rect(center = (screen_width / 2, screen_height / 2))
            screen.blit(victory_surf, victory_rect)

    def run(self):
        self.extra_alien_timer()
        self.alien_position_checker()
        self.collision_checks()
        self.display_lives()
        self.display_score()

        self.extra.update()
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_lasers.update()
        
        
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)
        crt.draw()

        self.victory_message()

class CRT: # adds old tv styling to screen
    def __init__(self):
        self.tv = pygame.image.load('SpaceInvaders/graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (screen_width, screen_height)) # incase we increase scale of screen

    def draw(self): # draw all crt stylings
        self.tv.set_alpha(randint(75, 90))
        self.create_crt_lines()
        screen.blit(self.tv, (0,0))

    def create_crt_lines(self): # adds lines to screen, to emulate crt tv
        line_height = 3
        line_amount = int(screen_height / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos), (screen_width, y_pos), 1)

if __name__ == '__main__': # we are going to work with different files, so we need different names
    pygame.init()
    screen_width = 600
    screen_height = 600
    num_blocks = 3
    screen = pygame.display.set_mode((screen_width, screen_height)) # create display
    clock = pygame.time.Clock() # call later to limit frame rate
    game = Game()
    crt = CRT()

    ALIENLASER = pygame.USEREVENT +1
    pygame.time.set_timer(ALIENLASER, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # check quit button
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()
        
        screen.fill((30,30,30)) # background color
        game.run()
            
        pygame.display.flip()
        clock.tick(60)
        

import pygame
import sys
from player import Soldier
from bullet import Bullet

class Game():
    def __init__(self):
        # player
        player_sprite = Soldier(300, 300, 2, 'player', 50)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        # enemy
        enemy_sprite = Soldier(400, 300, 2, 'enemy', 50)
        self.enemy_group = pygame.sprite.Group()
        self.enemy_group.add(enemy_sprite)
        # bullet
        self.bullet_group = pygame.sprite.Group()

    def run(self):
        # update
        self.player.update()
        self.bullet_group.update()
        self.enemy_group.update()
        # draw
        self.player.draw(screen)
        self.bullet_group.draw(screen)
        self.enemy_group.draw(screen)

if __name__ == '__main__':
    pygame.init()
    direction = True
    # screen
    screen_width = 800
    screen_height = int(screen_width * 0.8)
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Shooter')
    # game and clock objects
    game = Game()
    clock = pygame.time.Clock()
    game = Game()
    bullet_path = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.QUIT
                    sys.exit()
                if event.key == pygame.K_d:
                    game.player.sprite.facing_right = True
                    bullet_path = 0.8
                elif event.key == pygame.K_a:
                    game.player.sprite.facing_right = False
                    bullet_path = -0.1
                if event.key == pygame.K_SPACE:
                    game.bullet_group.add(Bullet(game.player.sprite.rect.x + (game.player.sprite.rect.size[0] * 2.8 * bullet_path), 
                    game.player.sprite.rect.y + (game.player.sprite.rect.size[1]), game.player.sprite.facing_right, screen_width))

        screen.fill('black')
        game.run()
        pygame.display.flip()
        clock.tick(60)

        

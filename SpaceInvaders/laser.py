import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        self.image = pygame.Surface((4,20))
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.y_constraint = screen_height
    
    def laser_move(self): # moves laser
        self.rect.y += self.speed

    def destroy(self): # deletes instance of laser if goes too far off screen
        if self.rect.bottom <= -50 or self.rect.top >= self.y_constraint + 50:
            self.kill()

    def update(self):
        self.laser_move()
        self.destroy()
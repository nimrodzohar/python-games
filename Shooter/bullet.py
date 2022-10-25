import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_right, constraint):
        super().__init__()
        self.constraint = constraint
        self.speed = 10
        self.facing_right = facing_right
        self.image = pygame.image.load('Shooter/img/icons/bullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def shoot(self):
        if self.facing_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    def destroy(self):
        if self.rect.right < 0 or self.rect.left > self.constraint:
            self.kill()
    
    def update(self):
        self.shoot()
        self.destroy()



    


import pygame

class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, character, ammo):
        super().__init__()
        self.character = character
        self.facing_right = True
        self.y = y
        self.x = x
        self.ammo = ammo
        self.start_ammo = ammo
        self.load_frames()
        # init player rect
        self.rect = self.idle_frames_left[0].get_rect()
        self.rect.center = (self.x, self.y)
        self.current_frame = 0 # index for frame lists
        self.last_updated = 0 # animation timer
        self.state = 'idle' # animation state
        self.image = self.idle_frames_right[0] # starting image
        self.velocity = 0
        self.scale = scale
        self.grav = 20

    def load_frames(self): # all frames are naturally turned right in x axis
        # idle frames
        self.idle_frames_right = [pygame.image.load(f'Shooter/img/{self.character}/idle/0.png').convert_alpha(), pygame.image.load(f'Shooter/img/{self.character}/idle/1.png').
        convert_alpha(), pygame.image.load(f'Shooter/img/{self.character}/idle/2.png').convert_alpha(), pygame.image.load(f'Shooter/img/{self.character}/idle/3.png').convert_alpha(),
        pygame.image.load(f'Shooter/img/{self.character}/idle/4.png').convert_alpha()]
        # create left facing idle frame list, using pygame.transform.flip function inside a for loop
        self.idle_frames_left = []
        for frame in self.idle_frames_right:
            self.idle_frames_left.append(pygame.transform.flip(frame, True, False)) # image, x axis flip? , y axis flip?
        # running frames
        self.run_frames_right = [pygame.image.load(f'Shooter/img/{self.character}/Run/0.png').convert_alpha(), pygame.image.load(f'Shooter/img/{self.character}/Run/1.png').convert_alpha(),
        pygame.image.load(f'Shooter/img/{self.character}/Run/2.png').convert_alpha(), pygame.image.load(f'Shooter/img/{self.character}/Run/3.png').convert_alpha(),
        pygame.image.load(f'Shooter/img/{self.character}/Run/4.png').convert_alpha(), pygame.image.load(f'Shooter/img/{self.character}/Run/5.png').convert_alpha()]
        self.run_frames_left = []
        for frame in self.run_frames_right:
            self.run_frames_left.append(pygame.transform.flip(frame, True, False))
        # jump frame
        self.jump_frame_right = pygame.image.load(f'Shooter/img/{self.character}/Jump/0.png').convert_alpha()
        self.jump_frame_left = pygame.transform.flip(self.jump_frame_right, True, False)

    def get_input(self):
        keys = pygame.key.get_pressed()
        self.velocity = 0

        if keys[pygame.K_d]:
            self.velocity = 3
        elif keys[pygame.K_a]:
            self.velocity = -3
        if keys[pygame.K_w]:
            if self.rect.y == self.y:
                self.grav = -15
        self.rect.x += self.velocity

    def apply_grav(self):
        self.grav += 1
        self.rect.y += self.grav
        if self.rect.y > self.y:
            self.rect.y = self.y

    def set_state(self):
        self.state = 'idle'
        if self.velocity > 0:
            if self.rect.y < self.y: # jumping while running
                self.state = 'jump'
            else:
                self.state = 'run right'
        elif self.velocity < 0:
            if self.rect.y < self.y:
                self.state = 'jump'
            else:
                self.state = 'run left'
        elif self.rect.y < self.y: # jumping while idle
            self.state = 'jump'

    def animate(self):
        # get current time
        now = pygame.time.get_ticks()
        # animate idle frames
        if self.state == 'idle':
            if now - self.last_updated > 100: # flip through frames every 200 ms
                # after 200 ms, now will be bigger than last_updated by 200 ms, thus repeating the cycle and switching to next frame
                self.last_updated = now
                # current_frame will be the index in our current animation list
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames_left) 
                # using key input from player in main file, we determine which direction player is facing
                if self.facing_right == True:
                    self.image = pygame.transform.scale(self.idle_frames_right[self.current_frame], (self.run_frames_right[self.current_frame].get_width() * self.scale, self.run_frames_right[self.current_frame].get_height() * self.scale))
                elif self.facing_right == False:
                    self.image = pygame.transform.scale(self.idle_frames_left[self.current_frame], (self.idle_frames_left[self.current_frame].get_width() * self.scale, self.idle_frames_left[self.current_frame].get_height() * self.scale))
        # animate running frames
        elif self.state == 'run right' or self.state == 'run left':
            if now - self.last_updated > 100: # check every 100 ms for running frame
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.run_frames_left)
                if self.state == 'run right':
                    self.image = pygame.transform.scale(self.run_frames_right[self.current_frame], (self.run_frames_right[self.current_frame].get_width() * self.scale, self.run_frames_right[self.current_frame].get_height() * self.scale))
                elif self.state == 'run left':
                    self.image = pygame.transform.scale(self.run_frames_left[self.current_frame], (self.run_frames_left[self.current_frame].get_width() * self.scale, self.run_frames_left[self.current_frame].get_height() * self.scale))
        # animate jump frame
        elif self.state == 'jump':
            if self.facing_right:
                self.image = pygame.transform.scale(self.jump_frame_right, (self.jump_frame_right.get_width() * self.scale, self.jump_frame_right.get_height() * self.scale))
            if self.facing_right == False:
                self.image = pygame.transform.scale(self.jump_frame_left, (self.jump_frame_left.get_width() * self.scale, self.jump_frame_left.get_height() * self.scale))

    def update(self):
        if self.character == 'player':
            self.get_input()
        self.set_state()
        self.animate()
        self.apply_grav()
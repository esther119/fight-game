import pygame 
import time

class Fighter(): 
    def __init__(self, x, y, fighter_data, sheet, columns):
        self.size = fighter_data[0]
        self.scale = fighter_data[1]
        self.offset = fighter_data[2]
        self.rect = pygame.Rect((x,y,50,100))
        self.velocity_y = 0
        self.jump = False
        self.attack_type = 0
        self.attacking = False 
        self.health = 100
        self.flip = False
        # self.animation_list = self.load_images(sheet, columns)
        self.action = 0 #0: idle 1: run 2: jump 3: attack1 4: attack2 5: hit 6: death
        self.frame_index = 0
        # self.image = self.animation_list[self.action][self.frame_index]
    

    def update_flip(self, target):
        """Update the flip attribute based on the relative position of the target."""
        # print('flipping position', self.rect.centerx, target.rect.centerx)
        if target.rect.centerx < self.rect.centerx:
            self.flip = True
        else:
            self.flip = False

        print('flipping', self.flip)

    def move(self, screen_width, screen_height, surface, target):
        # print('rct left and right', self.rect.left, self.rect.right)
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        # ensure player face each other 
        
        self.update_flip(target)
        # update player position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        # flip left or right]
        print('flip', self.flip)
        # self.image = pygame.transform.flip(self.image, self.flip, False) # surface, flip_x, flip_y
        pygame.draw.rect(surface, (255,0,0), self.rect)
        # surface.blit(self.image, (self.rect.x -self.offset[0], self.rect.y - -self.offset[1])) #source, dest
    
    
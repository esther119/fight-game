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
        self.animation_list = self.load_images(sheet, columns)
        self.action = 0 #0: idle 1: run 2: jump 3: attack1 4: attack2 5: hit 6: death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
    
    def load_images(self, sheet, columns):
        animation_list = []
        for y, col in enumerate(columns):
            row_images = []
            for x in range(0, col):
                # print('x', x, 'y', y, 'col', col )
                img = sheet.subsurface(x*self.size, y*self.size, self.size, self.size) #Surface(162x162x32)  #32 is the color depth
                # scale the image
                img = pygame.transform.scale(img, (self.size * self.scale, self.size * self.scale))
                row_images.append(img)
            animation_list.append(row_images)
        return animation_list



    def move(self, screen_width, screen_height, surface, target):
        # print('rct left and right', self.rect.left, self.rect.right)
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        key = pygame.key.get_pressed()

        if self.attacking == False: 
            if key[pygame.K_LEFT]:
                dx = -SPEED
            if key[pygame.K_RIGHT]:
                dx = SPEED
            #jump
            if key[pygame.K_SPACE] and not self.jump:
                self.velocity_y = -15
                self.jump = True
            elif not key[pygame.K_SPACE]:
                self.jump = False
            self.velocity_y += GRAVITY
            dy+= self.velocity_y
            # attack
            if key[pygame.K_z] or key[pygame.K_m]:
                print('attack')
                self.attack(surface, target)
                if key[pygame.K_z]:
                    self.attack_type = 1
                elif key[pygame.K_m]:
                    self.attack_type = 2


            

        # check for boundaries
        if self.rect.left + dx < 0:
            # print('left boundary', -self.rect.left)
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            # print('right boundary', -self.rect.right)
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            dy = screen_height - 110 - self.rect.bottom
        # check not over the top
        if self.rect.top + dy < 0:
            print('top boundary', -self.rect.top)
            dy = 0

        # ensure player face each other 
        if target.rect.x < self.rect.x:
            self.flip = True
        else:
            self.flip = False
        # update player position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        # flip left or right]
        print('flip', self.flip)
        self.image = pygame.transform.flip(self.image, self.flip, False) # surface, flip_x, flip_y
        pygame.draw.rect(surface, (255,0,0), self.rect)
        surface.blit(self.image, (self.rect.x -self.offset[0], self.rect.y - -self.offset[1])) #source, dest
    
    def attack(self, surface, target):
        self.attacking = True
        attacking_rect = pygame.Rect((self.rect.centerx - (2* self.rect.width * self.flip), self.rect.y, 2*self.rect.width, self.rect.height))
        if attacking_rect.colliderect(target.rect):
            print('hit')
            target.health -= 10
        # wait for a second 
        time.sleep(1)
        self.attacking = False
        

        pygame.draw.rect(surface, (0,255,0), attacking_rect)

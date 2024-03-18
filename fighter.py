import pygame 
import time

class Fighter(): 
    def __init__(self, player, x, y, fighter_data, flip, sheet, columns):
        self.player = player
        self.size = fighter_data[0]
        self.scale = fighter_data[1]
        self.offset = fighter_data[2]
        self.rect = pygame.Rect((x,y,50,100))
        self.velocity_y = 0
        self.running = False
        self.jump = False
        self.attack_type = 0
        self.attacking = False 
        self.attack_cooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True 
        self.flip = flip
        self.animation_list = self.load_images(sheet, columns)
        self.action = 0 #0: idle 1: run 2: jump 3: attack1 4: attack2 5: hit 6: death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
    
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

    def player_movement(self, dx, dy, surface, target):
        key = pygame.key.get_pressed()
        SPEED = 10
        GRAVITY = 2

        if self.player == 2: 
            if self.attacking == False: 
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                #jump
                if key[pygame.K_SPACE] and not self.jump:
                    self.velocity_y = -15
                    self.jump = True
                elif not key[pygame.K_SPACE]:
                    self.jump = False
                self.velocity_y += GRAVITY
                dy+= self.velocity_y
                # attack
                if key[pygame.K_n] or key[pygame.K_m]:
                    self.attack(surface, target)
                    if key[pygame.K_n]:
                        self.attack_type = 1
                    elif key[pygame.K_m]:
                        self.attack_type = 2  
        else:         
            if self.attacking == False: 
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                #jump
                if key[pygame.K_w] and not self.jump:
                    self.velocity_y = -15
                    self.jump = True
                elif not key[pygame.K_w]:
                    self.jump = False
                self.velocity_y += GRAVITY
                dy+= self.velocity_y
                # attack
                if key[pygame.K_c] or key[pygame.K_v]:
                    self.attack(surface, target)
                    if key[pygame.K_c]:
                        self.attack_type = 1
                    elif key[pygame.K_v]:
                        self.attack_type = 2
        return dx, dy


    def move(self, screen_width, screen_height, surface, target):
        # print('rct left and right', self.rect.left, self.rect.right)

        dx = 0
        dy = 0
        
        self.running = False
        dx, dy = self.player_movement(dx, dy, surface, target)
            

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
            dy = 0

        # ensure player face each other 
        if target.rect.x < self.rect.x:
            self.flip = True
        else:
            self.flip = False

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        # update player position
        self.rect.x += dx
        self.rect.y += dy
    


    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False) # surface, flip_x, flip_y
        surface.blit(img, (self.rect.x-self.offset[0], self.rect.y- self.offset[1])) #source, dest
    
    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect((self.rect.centerx - (2* self.rect.width * self.flip), self.rect.y, 2*self.rect.width, self.rect.height))
            
            if attacking_rect.colliderect(target.rect):
                # print('hit')
                target.health -= 10
                target.hit = True
                pygame.draw.rect(surface, (0,255,0), attacking_rect)
                

    def update_action(self, new_action =0):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            # print('new action', new_action)
    #handle animation update
    def update_animation(self):
        if self.running: 
            self.update_action(1)
        elif self.jump:
            self.update_action(2)
        elif self.attacking:
            if self.attack_type == 1:
                # print('attack1 update action')
                self.update_action(3)
            elif self.attack_type == 2:
                # print('attack2 update action')
                self.update_action(4)
        elif self.hit: 
            self.update_action(5)
        elif self.health <= 0:
            self.alive = False
            self.update_action(6)
        else:
            self.update_action(0)
        
        ANIMATION_COOLDOWN = 50
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            # print('heath', self.health)
            # if self.health <= 0:
            if not self.alive:  #TO DO: fix the death animation
                self.frame_index = len(self.animation_list[self.action]) - 1
                # print('death happens')
            else: 
                self.frame_index = 0
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                elif self.action == 5:
                    self.hit = False
                    # TO DO: if the player is in the middle of attack 

             
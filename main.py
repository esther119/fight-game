import pygame 
from fighter import Fighter

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fighter")

#set frame rate
clock = pygame.time.Clock()
FPS = 60

# colors 
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# define fighter variable 
WARRIOR_SIZE = 162
WARRIOR_SCALE = 2
WARRIOR_OFFSET = [130,100]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WARRIOR_SCALE = 1.65
WARRIOR_OFFSET = [160, 188]
WIZARD_DATA = [WIZARD_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]


# load background image 
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# define number of columns in each animation
WARRIOR_ANIMATION_COL = [10,8,1,7,7,3,7]
WIZARD_ANIMATION_COL = [8,8,1,8,8,3,7]
# function to draw background image
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)) 
    screen.blit(scaled_bg, (0, 0))

def health_bars(surface, fighter1, fighter2):
    # draw health bars
    pygame.draw.rect(surface, RED, (fighter1.rect.x, fighter1.rect.y - 20, 100, 10))
    pygame.draw.rect(surface, RED, (fighter2.rect.x, fighter2.rect.y - 20, 100, 10))
    pygame.draw.rect(surface, YELLOW, (fighter1.rect.x, fighter1.rect.y - 20, fighter1.health, 10))
    pygame.draw.rect(surface, YELLOW, (fighter2.rect.x, fighter2.rect.y - 20, fighter2.health, 10))

#create fighers
fighter1 = Fighter(200, 400, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_COL)
fighter2 = Fighter(600, 400, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_COL)

# game loop
run = True
while run:
    clock.tick(10)
    draw_bg()
    fighter1.draw(screen)
    fighter2.draw(screen)
    health_bars(screen, fighter1, fighter2)

    fighter1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter2)
    # fighter2.move()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # update display window
    pygame.display.update()
pygame.quit()
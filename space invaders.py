import pygame
import random
import math

# -- Global Constants

# -- Colors defined
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)
RED = (255,0,0)


## -- Define the class invader which is a sprite 
class invader(pygame.sprite.Sprite):
    # Define  the constructor for invader    
    def __init__(self, color, width, height, speed):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        # Define the starting value for each sprite
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,600)
        self.rect.y = random.randrange(0,50) - 50
        # Set speed of the sprite
        self.speed = speed

    # Class update function - moves the invader down on each loop
    def update(self):
        if self.rect.y > 480:
            self.rect.y = random.randrange(0,50) - 50
        else:
            self.rect.y = self.rect.y + self.speed

## -- Define the class player which is a sprite 
class player(pygame.sprite.Sprite):

    # Define  the constructor for player    
    def __init__(self, color, width, height):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        # Set the position of the player attributes
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 470
        # Set speed of the player initially stationary.
        self.speed = 0

    # Method which returns the value of the player's x co-ordinate
    def get_x(self):
        return self.rect.x
    
    # Method to update the speed of the player
    def player_speed_update(self, speed):
        self.speed = speed
        
    # Class update function - runs for each pass through the game loop       
    def update(self):
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > 630:
            self.rect.x = 630
        else:
            self.rect.x = self.rect.x + self.speed

## -- Define the class bullet which is a sprite 
class bullet(pygame.sprite.Sprite):
    # Define  the constructor for bullet including initial position    
    def __init__(self, color, width, height, x_val, y_val):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        # Set the attributes of the bullet
        self.rect = self.image.get_rect()
        self.rect.x = x_val
        self.rect.y = y_val
        # Set speed of the bullet
        self.speed = 2

    # Define the bullet update function - runs for each pass through the game loop       
    def update(self):
        self.rect.y = self.rect.y - self.speed
        
# -- Initialise pygame and clock
pygame.init()

# -- Blank Screen
size = (640,480)
screen = pygame.display.set_mode(size)

# -- Title of new window/screen
pygame.display.set_caption("Space Invaders")
# -- Fonts
font = pygame.font.SysFont('Calibri',20,True, False)

# -- Initialise variables for the game
done = False
lives = 5
bullet_count = 0
score = 0
number_of_invaders = 10

# Create a list of all sprites
all_sprites_list = pygame.sprite.Group()

# Create a list of inavders 
invader_list = pygame.sprite.Group()

# Create a bullet list
bullet_list = pygame.sprite.Group()

# Create the invaders and add them to the invader list
for x in range(number_of_invaders):
    my_invader = invader(BLUE, 10, 10, 1)
    invader_list.add(my_invader)
    all_sprites_list.add(my_invader)

# Create a player
player = player(YELLOW,10,10)
all_sprites_list.add(player)

# -- Manages how fast screen refreshes
clock = pygame.time.Clock()

### -- Game Loop
while not done:
    # -- User inputs here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                    player.player_speed_update(-3)
            elif event.key == pygame.K_RIGHT:
                player.player_speed_update(3)
            elif event.key == pygame.K_UP:
                if bullet_count > 49:
                    pass
                else:
                    # Create a red bullet and add it to the bullet list
                    mybullet = bullet(RED,5,5, player.get_x(), 490)
                    all_sprites_list.add(mybullet)
                    bullet_list.add(mybullet)
                    bullet_count += 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.player_speed_update(0)

    # Game logic goes in here
    # -- Check for collisions
    player_hit_list = pygame.sprite.spritecollide(player, invader_list, True)
    bullet_hit_list = pygame.sprite.groupcollide(invader_list, bullet_list, True, False)

    # For each time a player is hit by invader take one off the lives total
    for foo in player_hit_list:
        lives = lives - 1
    # For each time a bullet hits an invaders 
    for me in bullet_hit_list:
       score = score + 5

    # Run the update function for all sprites    
    all_sprites_list.update()

    #Screen background is BLACK
    screen.fill (BLACK)

    text = font.render("Lives: " + str(lives),True,WHITE)
    screen.blit(text,[30,30])
    text = font.render("Score: " + str(score),True,WHITE)
    screen.blit(text,[30,60])
    text = font.render("Bullets: " + str(50 - bullet_count),True,WHITE)
    screen.blit(text,[30,90])

    # -- Draw here
    all_sprites_list.draw(screen)
    
    # -- flip display to reveal new position of objects
    pygame.display.flip()
    clock.tick(60)

### -- End of game loop
pygame.quit()


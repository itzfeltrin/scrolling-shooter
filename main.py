import pygame

# initialize pygame project
pygame.init()

# define game constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300

# create pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# set window title
pygame.display.set_caption("Scrolling Shooter")

# run game loop while 'run' is True
run = True
while run:
    # paint the background a purple color
    screen.fill((120, 80, 235))

    # loop through events on every cycle of the loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update the screen with changes
    pygame.display.update()

# actually quit the game when exit the loop
pygame.quit()

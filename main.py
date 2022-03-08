import pygame

# initialize pygame project
pygame.init()

# define game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

# create pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# set window title
pygame.display.set_caption("Scrolling Shooter")

# define framerate
clock = pygame.time.Clock()
fps = 60

# define player action variables
moving_left = False
moving_right = False

# define colors
BG = (144, 201, 120)


def draw_bg():
    screen.fill(BG)


# define soldier class
class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        # -1 = left, 1 = right
        self.direction = 1
        self.flip = False
        img = pygame.image.load(f'assets/img/{self.char_type}/Idle/0.png')
        self.img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        # delta y and delta x (how much to move in both axes)
        dx = 0
        dy = 0

        # assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect)


player = Soldier('player', 200, 200, 3, 5)
enemy = Soldier('enemy', 400, 200, 3, 5)

# run game loop while 'run' is True
run = True
while run:
    # set framerate
    clock.tick(60)

    # redraw background on every cycle of the loop
    draw_bg()
    # move and draw player on screen
    player.move(moving_left, moving_right)
    player.draw()
    enemy.draw()

    # loop through events on every cycle of the loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            # quit game on press escape
            if event.key == pygame.K_ESCAPE:
                run = False
            # move player on press ASD keys
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    # update the screen with changes
    pygame.display.update()

# actually quit the game when exit the loop
pygame.quit()

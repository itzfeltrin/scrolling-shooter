import os

import pygame

# initialize pygame project
pygame.init()

# define game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
GRAVITY = 0.75

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
shoot = False

# load images
bullet_img = pygame.image.load('assets/img/icons/bullet.png').convert_alpha()

# define colors
BG = (144, 201, 120)
RED = (255, 0, 0)


def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))


# define soldier class
class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
        # -1 = left, 1 = right
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        # frame_index is where the animation is at
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # load all images
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            temp_list = []
            folder_path = f'assets/img/{self.char_type}/{animation}'
            num_of_frames = len(os.listdir(folder_path))
            for i in range(num_of_frames):
                img = pygame.image.load(os.path.join(folder_path, f'{i}.png')).convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        self.check_alive()
        # update shoot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

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

        # jump
        if self.jump and self.in_air is False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y >= 10:
            self.vel_y = 10
        dy += self.vel_y

        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery,
                            self.direction)
            bullet_group.add(bullet)
            # reduce ammo
            self.ammo -= 1

    def update_animation(self):
        cooldown = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            # if animation has run out reset frame_index
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 3:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # reset frame_index
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # move bullet
        self.rect.x += self.speed * self.direction
        # check if bullet has gone out of screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        # check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False) and player.alive:
            player.health -= 5
            self.kill()
        if pygame.sprite.spritecollide(enemy, bullet_group, False) and enemy.alive:
            enemy.health -= 25
            print(enemy.health)
            self.kill()


# create sprite groups
bullet_group = pygame.sprite.Group()

player = Soldier('player', 200, 200, 3, 5, 20)
enemy = Soldier('enemy', 400, 200, 3, 5, 20)

# run game loop while 'run' is True
run = True
while run:
    # set framerate
    clock.tick(60)

    # redraw background on every cycle of the loop
    draw_bg()

    enemy.update()
    enemy.draw()

    player.update()
    player.draw()

    # update and draw groups
    bullet_group.update()
    bullet_group.draw(screen)

    if player.alive:
        if shoot:
            player.shoot()
        # update player actions
        if player.in_air:
            player.update_action(2)
        elif moving_left or moving_right:
            player.update_action(1)
        else:
            player.update_action(0)

    # move and draw player on screen
    player.move(moving_left, moving_right)

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
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_SPACE:
                shoot = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False

    # update the screen with changes
    pygame.display.update()

# actually quit the game when exit the loop
pygame.quit()

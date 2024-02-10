import pygame 
from pygame import mixer
import os
import random
import csv
import button 

mixer.init()
pygame.init()

# Get the full path of the current file
file_path = os.path.realpath(__file__)

# Extract the directory path
directory_path = os.path.dirname(file_path)

file_path = directory_path + '/'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Special Forces Adventure')

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.75
SCROLL_THRESH = 200 
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 22
MAX_LEVELS = 3
screen_scroll = 0 
bg_scroll = 0
level = 1
score = 0
start_game = False
start_intro = False

#define player action variables 
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False
boss = None

#load music/sounds
pygame.mixer.music.load(file_path + 'audio/music2.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound(file_path + 'audio/jump.wav')
jump_fx.set_volume(0.5)
shot_fx = pygame.mixer.Sound(file_path + 'audio/shot.wav')
shot_fx.set_volume(0.5)
grenade_fx = pygame.mixer.Sound(file_path + 'audio/grenade.wav')
grenade_fx.set_volume(0.5)


#load images 
#button images
start_img = pygame.image.load(file_path + 'img/start_btn.png').convert_alpha()
exit_img = pygame.image.load(file_path + 'img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load(file_path + 'img/restart_btn.png').convert_alpha()
#background
pine1_img = pygame.image.load(file_path + 'img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load(file_path + 'img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load(file_path + 'img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load(file_path + 'img/Background/sky_cloud.png').convert_alpha()
#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(file_path + f'img/Tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
#bullet
bullet_img = pygame.image.load(file_path + 'img/icons/bullet.png').convert_alpha()
#grenade
grenade_img = pygame.image.load(file_path + 'img/icons/grenade.png').convert_alpha()
#pickup boxes 
health_box_img = pygame.image.load(file_path + 'img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load(file_path + 'img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load(file_path + 'img/icons/grenade_box.png').convert_alpha()
item_boxes = {
    'Health'  : health_box_img, 
    'Ammo'    : ammo_box_img,
    'Grenade' : grenade_box_img
}

#define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)

#define font
font = pygame.font.SysFont('Futura', 30)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_bg():
    screen.fill(BG)
    width = sky_img.get_width()
    for x in range(5):     
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - bg_scroll *0.8, SCREEN_HEIGHT - pine2_img.get_height()))


#function to reset level
def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    #create empty tile list 
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data


class PLAYER(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed 
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0  
        self.grenades = grenades 
        self.health = 100
        self.max_health = self.health     
        self.direction = 1
        self.vel_y = 0 
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0 
        self.action = 0 
        self.update_time = pygame.time.get_ticks()
        #AI specific variables 
        self.move_counter = 0 
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0 
        
        #load all images for players 
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            #reset temp list of images
            temp_list = []
            #count number of files in the folder
            num_of_frames = len(os.listdir(file_path + f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(file_path + f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)            
            self.animation_list.append(temp_list) 

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        #reset movement variables 
        screen_scroll = 0
        dx = 0 
        dy = 0 

        #assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1 

        #jump 
        if self.jump == True and self.in_air == False:
            self.vel_y = -15
            self.jump = False
            self.in_air = True

        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #check for collision 
        for tile in world.obstacle_list:
            #check collisions in the x direction
            if tile [1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0 
                #if the AI has hit a wall then make it turn around
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0 

            #check for collision in the y direction
            if tile [1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground, i.e jumping
                if self.vel_y < 0:
                    self.vel_y = 0 
                    dy = tile[1].bottom - self.rect.top
                #check if above the groun, i.e falling 
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom


        #check for collision with water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0 

        #check for collision with exit 
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True 

        #check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0 


        #check if going off the edges of the screen
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0 
        
        #update rectangle position 
        self.rect.x += dx
        self.rect.y += dy

        #update scroll based on player postion 
        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH) or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx 

        return screen_scroll, level_complete

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            #reduce ammo
            self.ammo -= 1
            shot_fx.play()


    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0) #0: idle
                self.idling = True
                self.idling_counter = 50
            #check if the AI is near the player
            if self.vision.colliderect(player.rect):
                #stop running and face the player 
                self.update_action(0) #0: idle
                #shoot
                self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1) #1: run 
                    self.move_counter += 1
                    #update AI vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1 
                        self.move_counter *= -1
                else: 
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        #scroll 
        self.rect.x += screen_scroll

    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passsed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out then reset back to start 
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the aniamtion settings
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

# Enemy Class
class Enemy(PLAYER):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
        super().__init__(char_type, x, y, scale, speed, ammo, grenades) 
        self.health = 50 # Enemy Health
        self.max_health = 50  # Enemy Max Health
        self.alive = True

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False


    def update(self):
        super().update() 
        # Check the health of enemy lower than 0, alive fail
        if self.health <= 0:
            self.alive = False

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)  # 0: idle
                self.idling = True
                self.idling_counter = 50
            # check if the AI is near the player
            if self.vision.colliderect(player.rect):
                # stop running and face the player
                self.update_action(0)  # 0: idle
                # shoot
                self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)  # 1: run
                    self.move_counter += 1
                    # update AI vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        # scroll
        self.rect.x += screen_scroll

class Boss(PLAYER):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
        super().__init__(char_type, x, y, scale * 3, speed, ammo, grenades * 5) 
        self.health = 200  # Enemy Boss Health
        self.max_health = 200  # Enemy Boss Max Health
        self.alive = True

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False


    def update(self):
        super().update()  
        # Check the health of boss lower than 0, alive fail
        if self.health <= 0:
            self.alive = False

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)  # 0: idle
                self.idling = True
                self.idling_counter = 50
            # check if the AI is near the player
            if self.vision.colliderect(player.rect):
                # stop running and face the player
                self.update_action(0)  # 0: idle
                # shoot
                self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)  # 1: run
                    self.move_counter += 1
                    # update AI vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        # scroll
        self.rect.x += screen_scroll

class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        #iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15: #create player 
                        player = PLAYER('player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5, 20, 5)
                        health_bar = HealthBar(10, 10, player.health, player.health)
                    elif tile == 16: #create enemies
                        enemy = Enemy('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20, 0)
                        enemy_group.add(enemy)
                    elif tile == 17: #create ammo box 
                        item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 18: #create grenade box 
                        item_box = ItemBox('Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19: #create health box 
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20: # create exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
                    elif tile == 21:  # create the Boss
                            global boss
                            boss = Boss('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20, 5)
                            enemy_group.add(boss)

        return player, health_bar


    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self):
	        self.rect.x += screen_scroll

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        #scroll
        self.rect.x += screen_scroll
        #check if the player has picked up the box
        if pygame.sprite.collide_rect(self, player):
            #check what kind of box it was 
            if self.item_type == 'Health':              
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health               
            elif self.item_type =='Ammo':
                player.ammo += 15
            elif self.item_type == 'Grenade':
                player.grenades += 3 
            #delete the itembox
            self.kill()


class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y 
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        #update with new health
        self.health = health
        #calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10 
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction 

    def update(self):
        #move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        #check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        #check for collisons with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        #check collisions with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25               
                    self.kill()


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -15
        self.speed = 7 
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction 

    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y 

        #check for collision with level
        for tile in world.obstacle_list:
            #check collision with walls
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            #check for collision in the y direction
            if tile [1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0 
                #check if below the ground, i.e thrown up
                if self.vel_y < 0:
                    self.vel_y = 0 
                    dy = tile[1].bottom - self.rect.top
                #check if above the groun, i.e falling 
                elif self.vel_y >= 0:
                    self.vel_y = 0                  
                    dy = tile[1].top - self.rect.bottom       

        #update grenade position 
        self.rect.x += dx + screen_scroll
        self.rect.y += dy 

        #countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            grenade_fx.play()
            explosion = Explosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
            #do damage to anyone that is nearby
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 50
                    
                    

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(file_path + f'img/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale))) 
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]         
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0 


    def update(self):
        #scroll       
        self.rect.x += screen_scroll

        EXPLOSION_SPEED = 4
        #update explosion animation 
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0 
            self.frame_index += 1
            #if the animation is complete then delete the explosion
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]




class ScreenFade():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0 



    def fade(self):
        fade_complete = False 
        self.fade_counter += self.speed
        if self.direction == 1: #whole screen fade
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.colour, (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.direction == 2: #vertical screen down
            pygame.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True

        return fade_complete

def display_score():
    # Calculate the width and height of the text
    text_surf = font.render(f'Your Score: {score+50+player.health}', True, WHITE)
    text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Draw a rectangle on the background
    background_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 10, text_rect.width + 20, text_rect.height + 20)
    pygame.draw.rect(screen, BLACK, background_rect)

    # Draw the score in the center of the screen
    screen.blit(text_surf, text_rect)
    pygame.display.update()  # Update the screen to show what you draw

def reset_game():
    global score, level, start_game, boss, world, player, health_bar, shoot
    score = 0
    level = 1
    start_game = True
    boss = None
    shoot = False
    # Reset the sprite group
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    # Reload the data from the first level
    world_data = []
    for row in range(ROWS):
        r = [-1] * COLS
        world_data.append(r)
    with open(file_path + f'level{level}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)
    world = World()
    player, health_bar = world.process_data(world_data)
    # Reset background scrolling
    bg_scroll = 0
    # 重新开始游戏
    main_game_loop()
def game_over_screen():
    screen.fill(BG)
    # The score is displayed first
    display_score()

    # Restart button
    restart_button = button.Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 70, restart_img, 1)

    # The game loops and waits for the player to respond
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # If the window closes, exit the program completely
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse clicked the restart button
                if restart_button.isOver(pygame.mouse.get_pos()):
                    waiting = False  # End the wait and start a new game

        # Draw buttons
        if restart_button.draw(screen):
            reset_game()  # Reset the game and start over
            waiting = False  # If you click the button, start a new game

        pygame.display.update()


#create screen fades
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)


#create buttons
start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)


#create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()


#crate empty tile list 
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
#load in level data and create world
with open(file_path + f'level{level}_data.csv', newline= '') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)        
world = World()
player, health_bar = world.process_data(world_data)


run = True
def main_game_loop():
    global run, start_game
while run:

    clock.tick(FPS)

    if start_game == False:
        #draw menu
        screen.fill(BG) 
        #add buttons
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            run = False
    else:
        #update background
        draw_bg()
        #draw world map 
        world.draw()
        #show player health
        health_bar.draw(player.health)
        #show ammo
        draw_text('AMMO: ', font, WHITE, 10, 35)
        for x in range(player.ammo):
            screen.blit(bullet_img, (90 + (x * 10), 40))
        #show grenade
        draw_text('GRENADE: ', font, WHITE, 10, 60)
        for x in range(player.grenades):
            screen.blit(grenade_img, (135 + (x * 15), 60))


        player.update()
        player.draw()

        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()

        #update and draw groups
        bullet_group.update()
        grenade_group.update()
        explosion_group.update()
        item_box_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()
        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)

        #show intro 
        if start_intro == True:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        #update player actions 
        if player.alive:
            #shoot bullets
            if shoot:
                player.shoot()   
            #throw grenades
            elif grenade and grenade_thrown == False and player.grenades > 0:
                grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction), player.rect.top, player.direction)
                grenade_group.add(grenade)
                #reduce grenades
                player.grenades -= 1
                grenade_thrown = True                             
            if player.in_air:
                player.update_action(2) #2: jump 
            elif moving_left or moving_right:
                player.update_action(1) #1: run 
            else:
                player.update_action(0) #0: idle
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll
            #check if player has completed the level
            if level_complete:
                start_intro = True
                level += 1
                bg_scroll = 0 
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    #load in level data and create world
                    with open(file_path + f'level{level}_data.csv', newline= '') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)       
                    world = World()
                    player, health_bar = world.process_data(world_data)
        else:
            screen_scroll = 0 
            if death_fade.fade():
                if restart_button.draw(screen):
                    death_fade.fade_counter = 0 
                    start_intro = True
                    bg_scroll = 0 
                    world_data = reset_level()
                    #load in level data and create world
                    with open(file_path + f'level{level}_data.csv', newline= '') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)       
                    world = World()
                    player, health_bar = world.process_data(world_data)


    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
            if event.key == pygame.K_UP and player.alive:
                player.jump = True
                jump_fx.play()
            if event.key == pygame.K_ESCAPE:
                run = False



        #keyboard button release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False
    for enemy in enemy_group:
        if not enemy.alive:
            score += 5
            enemy_group.remove(enemy)
    for item in item_box_group:
        if pygame.sprite.collide_rect(player, item):
            score += 10  # Increase your score
            item.kill()
    # SCREEN_WIDTH
    text = f'Score: {score}'
    text_width, text_height = font.size(text)  # Get the text dimensions
    x = SCREEN_WIDTH - text_width - 10  # Start drawing text from the right edge of the screen 10 pixels to the left
    y = 10  # 10 pixels from the top of the screen

    draw_text(text, font, WHITE, x, y)
    # Check if the boss is defeated at the appropriate place in the game's main loop

    if boss is not None and not boss.alive:
        game_over_screen()  # Displays the game over screen and score
        start_game = True  # Reset the game start flag

    pygame.display.update()

pygame.quit()
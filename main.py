import pygame
import math
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('./img/music.mp3')
pygame.mixer.music.play(loops=0)
# F = 1/2*m*v^2
clock = pygame.time.Clock()
enemy_scroll = 0
FPS = 60
x = 100
y = 300
BLACK = (0,0,0)
jumping = False
direction = 'right'
#create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 432
Y_GRAVITY = 1
JUMP_HEIGHT = 15
shoot = False
standing = pygame.image.load('img/flame1.png')
jumpingly = pygame.image.load('img/flame1.png')
Y_VELOCITY = JUMP_HEIGHT
flame_rect = standing.get_rect(center=(x,y))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fire Man")
fireball_shoot = 0
#define game variables
scroll = 0
fire_image = pygame.image.load('img/Fireball1.png')

class Player(pygame.sprite.Sprite):
  def __init__(self,x,y,direction):
    self.direction = 'right'
    self.x = x
    self.y = y
    self.image = standing
    self.animation_loop = 0
    self.bleh = 0
    self.rect = self.image.get_rect()
    self.cooldown = 0
    self.enemy_count = 0
    
    
  def animation(self):
    self.left_animation = [
      pygame.image.load('img/flame6.png'),
      pygame.image.load('img/flame5.png'),
    ]
    self.right_animation = [
      pygame.image.load('img/flame3.png'),
      pygame.image.load('img/flame4.png'),
    ]
    self.center_animation = [
      pygame.image.load('img/flame1.png'),
      pygame.image.load('img/flame2.png')
    ]
    

  def update(self):
    self.animation()


    if shoot and self.cooldown <= 0:
      self.cooldown = 40
      bullet = Attack(player.rect.centerx, player.rect.centery, player.direction)
      bullet_group.add(bullet)
    if self.cooldown <= 0 and self.enemy_count <=5:
      self.enemy_count+=1
      enemytemp = Enemy(500+self.enemy_count*400, player.y)
      enemy_group.add(enemytemp)
    

    

    if self.direction == 'left':
      self.bleh +=1
      if self.bleh % 10 == 0:
        self.image = self.left_animation[self.animation_loop]
        self.animation_loop += 1
    if self.direction == 'right': 
      self.bleh +=1
      if self.bleh % 10 == 0:
        self.image = self.right_animation[self.animation_loop]
        self.animation_loop += 1
    if self.direction == 'center':
      self.bleh +=1
      if self.bleh % 10 == 0:
        self.image = self.center_animation[self.animation_loop]
        self.animation_loop += 1
    if self.animation_loop >= 2:
          self.animation_loop = 0
    screen.blit(self.image,(self.x,self.y))

class Attack(pygame.sprite.Sprite):
  def __init__(self, x, y,direction):
    pygame.sprite.Sprite.__init__(self)
    self.image = fire_image
    self.image = pygame.transform.scale(self.image, (100,100))
    self.fireball_shoot = 0
    self.vel = 8 
    self.rect = self.image.get_rect()
    self.rect.center = (player.x+60,player.y+25)
    self.direction = direction
    self.update()
  def update(self):
    self.rect.x += (self.vel)

    if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH - 85:
      self.kill()


  def collide(self):
      #hits = pygame.sprite.spritecollide(self, player, True)
      pass


  def animate(self):
      direction = player.direction

      right_animations = [
      pygame.image.load('img/Fireball1.png'),
      pygame.image.load('img/Fireball2.png'),]

      if direction == 'right':
        self.image = right_animations[math.floor(self.animation_loop)]
class Enemy(pygame.sprite.Sprite):
  def __init__(self,x,y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load('img/trap.png')
    self.image = pygame.transform.scale(self.image, (200,200))
    self.x = x
    self.y = player.y
    self.rect = self.image.get_rect()
    self.rect.center = (self.x,self.y)
    self.update()
  def update(self):
    self.rect.x -= enemy_scroll
    
  




  
ground_image = pygame.image.load("img/grass1.png").convert_alpha()
ground_image = pygame.transform.scale(ground_image, (320,64))
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

house_images = []
for i in range(1,4):
  house_image = pygame.image.load(f"img/house{i}.png").convert_alpha()
  house_image = pygame.transform.scale(house_image, (200,200))
  house_images.append(house_image)
house_width = house_images[0].get_width()
house_height = house_image.get_height()

bg_images = []
for i in range(1, 4):
  bg_image = pygame.image.load(f"img/sky1.png").convert_alpha()
  bg_image = pygame.transform.scale(bg_image, (768,432))
  bg_images.append(bg_image)
bg_width = bg_images[0].get_width()

def draw_bg():
  for x in range(10):
    speed = 1
    for i in bg_images:
      screen.blit(i, ((x * bg_width) - scroll * speed, 0))
      speed += 0.2
def draw_house():
  for x in range(20):
    speed = 1
    for i in house_images:
      screen.blit(i, (((x*2) * house_width) - scroll * speed, 237))
      speed += 0.2

def draw_ground():
  for x in range(30):
    screen.blit(ground_image, ((x * ground_width) - scroll * 2.5, SCREEN_HEIGHT - ground_height))
player=Player(x,y,direction)
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
fireballs = [] # This goes right above the while loop
#game loop
run = True
while run:
  enemy_scroll =5
  player.cooldown-=1
  scroll +=1
  if scroll <=0:
    scroll = 0

  clock.tick(FPS)

  #draw world
  draw_bg()
  draw_ground()
  draw_house()
  player.update()
  bullet_group.update()
  bullet_group.draw(screen)
  enemy_group.update()
  enemy_group.draw(screen)
  

  #get keypresses
  key = pygame.key.get_pressed()
  if key[pygame.K_LEFT] and scroll > 0:
    scroll -= 5
    player.direction = 'left'
  if key[pygame.K_RIGHT] and scroll < 3000:
    scroll += 5
    player.direction = 'right'
  if key[pygame.K_UP]:
    jumping = True
  if key[pygame.K_SPACE]:
    shoot = True

  
  

  if jumping:
    player.y -= Y_VELOCITY
    Y_VELOCITY -= Y_GRAVITY
    if Y_VELOCITY <- JUMP_HEIGHT:
      jumping = False
      Y_VELOCITY = JUMP_HEIGHT
    flame_rect = jumpingly.get_rect(center=(x,y))
  else:
    flame_rect = standing.get_rect(center=(x,y))


    
  if scroll >=3000:
    scroll -=2500


  #event handlers
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_SPACE:
        shoot = False

  pygame.display.update()


pygame.quit()
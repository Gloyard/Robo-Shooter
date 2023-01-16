import pygame
from random import choice

class Mob(object):
    def __init__(self):
        self.image = pygame.image.load("hirvio.png")
        self.rect = self.image.get_rect()
        self.x = choice(range(50, 590))
        self.y = -50
# another idea for hibox before trying the collidepoint function
#        self.hitbox = (self.x, self.y, self.image.get_width(), self.image.get_height())

    def collide_check(self, x, y):
        self.collide = self.rect.collidepoint(x, y)
        if self.collide:
            return True

    def create(self):
        screen.blit(self.image, (self.x, self.y))
        self.move()
    
    def move(self):
        self.y += 3
    
    def hit(self):
        score.add()

class Bullet(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), 3)
        self.move()
    
    def move(self):
        self.y -= 5

    def call(self):
        return (self.x, self.y)
            
class Player:
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("robo.png")
        self.rect = self.image.get_rect()
        self.x = 320
        self.y = 860

        self.left = False
        self.right = False
        self.up = False
        self.down = False

    def fire(self):
        bullets.append(Bullet((self.x + self.image.get_width()/2), self.y))

class Score(object):
    def __init__(self):
        self.score = 3
        self.font = pygame.font.SysFont("Arial", 24)
        self.score_text = self.font.render(str(self.score), True, (255, 0, 0))

    def update(self):
        self.score_text = self.font.render(str(self.score), True, (255, 0, 0))

    def draw(self):
        screen.blit(self.score_text, (590, 50))

    def add(self):
        self.score += 1

def main():
    pygame.init()
    global screen
    screen = pygame.display.set_mode((640, 960))
    pygame.display.set_caption("Robo Shooter")

    screen.fill((0, 0, 0))

    global player
    player = Player()

    global bullets
    bullets = []

    global mobs
    mobs = []

    global score
    score = Score()

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        check_events()
        flip_display(screen)

def check_events():    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.left = True
            if event.key == pygame.K_RIGHT:
                player.right = True
            if event.key == pygame.K_UP:
                player.up = True
            if event.key == pygame.K_DOWN:
                player.down = True
            if event.key == pygame.K_SPACE:
                player.fire()
            if event.key == pygame.K_q:
                mobs.append(Mob())
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.left = False
            if event.key == pygame.K_RIGHT:
                player.right = False
            if event.key == pygame.K_UP:
                player.up = False
            if event.key == pygame.K_DOWN:
                player.down = False
    if player.left:
        if player.x > 0:
            player.x -= 4
    if player.right:
        if player.x < 640 - player.image.get_width():
            player.x += 4
    if player.up:
        if player.y > 0:
            player.y -= 4
    if player.down:
        if player.y < 960 - player.image.get_height():
            player.y += 4

    for bullet in bullets:
        for mob in mobs:
#            collide = mob.rect.collidepoint(bullet.x, bullet.y)
            if mob.collide_check(bullet.x, bullet.y):
                bullets.pop(bullets.index(bullet))
                score.add()
# another idea for hitbox
#        if bullet.y < mob.hitbox[1] + mob.hitbox[3] and bullet.y > mob.hitbox[1]:
#            if bullet.x > mob.hitbox[0] and bullet.x < mob.hitbox[0] + mob.hitbox[2]:
        if bullet.y < 0:
            bullets.pop(bullets.index(bullet))
    
    for mob in mobs:
        if mob.y > 1000:
            mobs.pop(mobs.index(mob))

    score.update()

def flip_display(screen):
    screen.fill((10, 10, 10))
    screen.blit(player.image, (player.x, player.y))
    for bullet in bullets:
        bullet.draw(screen)
    for mob in mobs:
        mob.create()
    score.draw()
    pygame.display.flip()

if __name__ == "__main__":
    main()

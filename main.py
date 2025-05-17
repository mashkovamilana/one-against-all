from pygame import *
from random import *

window = display.set_mode((1600, 900))
display.set_caption('One against all')
background = transform.scale(image.load('images/background.png'), (1600, 900))
start = transform.scale(image.load('images/start.png'), (800, 450))
lose = transform.scale(image.load('images/lose.png'), (800, 450))
win = transform.scale(image.load('images/win.png'), (800, 450))

game = True
FPS = 60
state = 'start'
# start
# game
# win
# lose
clock = time.Clock()
state_timer = 0
win_timer = 0


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, speed, x, y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (50, 50))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def colliding_with(self, other):
        collide = sprite.collide_rect(self, other)
        return collide


class Player(GameSprite):
    def __init__(self, player_image, speed, x, y):
        super().__init__(player_image, speed, x, y)
        self.fire_timer = 0

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 1450:
            self.rect.x += self.speed
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_SPACE] and self.fire_timer >= 20:
            self.fire_timer = 0
            bullets.append(Bullet('images/gem.png', 6, self.rect.x + 13, self.rect.y))
        self.fire_timer += 1


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 900:
            spawn = randint(0, 1600)
            self.speed = randint(3, 7)
            self.rect.x = spawn
            self.rect.y = -100

    def collision(self):
        self.rect.y = -100
        self.rect.x = randint(0, 1600)
        self.speed = randint(3, 7)


class Bullet(sprite.Sprite):
    def __init__(self, player_image, speed, x, y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (25, 25))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -25:
            bullets.remove(self)

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


player = Player('images/player.PNG', 10, 730, 700)

bullets = []
enemies = []
hearts = []

enemies.append(Enemy('images/sprite1.png', randint(3, 7), 800, -100))
enemies.append(Enemy('images/sprite1.png', randint(3, 7), 500, -100))
enemies.append(Enemy('images/sprite1.png', randint(3, 7), 200, -100))
enemies.append(Enemy('images/sprite1.png', randint(3, 7), 1000, -100))
enemies.append(Enemy('images/sprite1.png', randint(3, 7), 50, -100))
hearts.append(GameSprite('images/heart.png', 0, 1550, 0))
hearts.append(GameSprite('images/heart.png', 0, 1490, 0))
hearts.append(GameSprite('images/heart.png', 0, 1430, 0))

lives = 3
count = 0
while game:
    window.blit(background, (0, 0))
    if state == 'start':
        window.blit(start, (400, 250))
        state_timer += 1
        if state_timer == 120:
            state = 'game'
            state_timer = 0
    if state == 'game':
        player.update()
        player.reset()
        for enemy in enemies:
            if enemy.colliding_with(player):
                lives -= 1
                enemy.collision()
                hearts.pop(len(hearts) - 1)
                if lives == 0:
                    state = 'lose'
                    lives = 3
                    hearts.append(GameSprite('images/heart.png', 0, 1550, 0))
                    hearts.append(GameSprite('images/heart.png', 0, 1490, 0))
                    hearts.append(GameSprite('images/heart.png', 0, 1430, 0))
            for bullet in bullets:
                if enemy.colliding_with(bullet):
                    bullets.remove(bullet)
                    enemy.collision()
                    count += 1
        for enemy in enemies:
            enemy.update()
            enemy.reset()
        for bullet in bullets:
            bullet.update()
            bullet.reset()
        for heart in hearts:
            heart.update()
            heart.reset()
        win_timer += 1
        if win_timer >= 3600:
            state = 'win'
            win_timer = 0
    if state == 'lose':
        window.blit(lose, (400, 250))
        state_timer += 1
        if state_timer >= 120:
            state = 'game'
            state_timer = 0
    if state == 'win':
        window.blit(win, (400, 250))
        state_timer += 1
        if state_timer >= 120:
            state = 'game'
            state_timer = 0
    for e in event.get():
        if e.type == QUIT:
            game = False
    display.update()
    clock.tick(FPS)

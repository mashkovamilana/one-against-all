from pygame import *
from random import *
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

font.init()
mixer.init()

window = display.set_mode((1600, 900))
display.set_caption('One against all')
background = transform.scale(image.load(resource_path('images/background.png')), (1600, 900))
start = transform.scale(image.load(resource_path('images/start.png')), (800, 450))
lose = transform.scale(image.load(resource_path('images/lose.png')), (800, 450))
win = transform.scale(image.load(resource_path('images/win.png')), (800, 450))
mixer.music.load(resource_path('audio/battleThemeA.mp3'))
mixer.music.play(-1)
chicken_sound = mixer.Sound(resource_path('audio/Chicken.ogg'))
game_over = mixer.Sound(resource_path('audio/GAMEOVER.wav'))
player_win = mixer.Sound(resource_path('audio/win.wav'))
hit = mixer.Sound(resource_path('audio/hit01.mp3.flac'))
player_hit = mixer.Sound(resource_path('audio/qubodupRatAttack.flac'))

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
lives = 3
count = 0
time_left = 60
time_left_timer = 0


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, speed, x, y):
        super().__init__()
        self.image = transform.scale(image.load(resource_path(player_image)), (50, 50))
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
            hit.play()
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
        self.image = transform.scale(image.load(resource_path(player_image)), (25, 25))
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


class TextArea(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = None
        self.font = font.Font(resource_path('Tiny5-Regular.ttf'), 36)
        self.x = x
        self.y = y

    def set_text(self, text):
        self.image = self.font.render(text, False, (0, 0, 0))

    def reset(self):
        if self.image is not None:
            window.blit(self.image, (self.x, self.y))


player = Player('images/player.PNG', 10, 730, 700)
score_label = TextArea(20, 20)
score_label.set_text('Score:' + str(count))
counter = TextArea(20, 60)
counter.set_text('Time left:' + str(time_left))

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

while game:
    window.blit(background, (0, 0))
    if state == 'start':
        window.blit(start, (400, 250))
        state_timer += 1
        if state_timer == 120:
            state = 'game'
            state_timer = 0
    if state == 'game':
        score_label.reset()
        counter.reset()
        player.update()
        player.reset()
        if time_left_timer == 60:
            time_left -= 1
            counter.set_text('Time left:' + str(time_left))
            time_left_timer = 0
        for enemy in enemies:
            if enemy.colliding_with(player):
                lives -= 1
                enemy.collision()
                hearts.pop(len(hearts) - 1)
                player_hit.play()
                if lives == 0:
                    state = 'lose'
                    game_over.play()
                    mixer.music.set_volume(0)
            for bullet in bullets:
                if enemy.colliding_with(bullet):
                    chicken_sound.play()
                    bullets.remove(bullet)
                    enemy.collision()
                    count += 1
                    score_label.set_text('Score:' + str(count))

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
        time_left_timer += 1
        if win_timer >= 3600:
            state = 'win'
            win_timer = 0
            player_win.play()
            mixer.music.set_volume(0)
    if state == 'lose':
        window.blit(lose, (400, 250))
        state_timer += 1
        if state_timer >= 120:
            state = 'game'
            mixer.music.set_volume(100)
            state_timer = 0
            win_timer = 0
            count = 0
            time_left = 60
            hearts.clear()
            lives = 3
            hearts.append(GameSprite('images/heart.png', 0, 1550, 0))
            hearts.append(GameSprite('images/heart.png', 0, 1490, 0))
            hearts.append(GameSprite('images/heart.png', 0, 1430, 0))
            score_label.set_text('Score:' + str(count))
            counter.set_text('Time left:' + str(time_left))

    if state == 'win':
        window.blit(win, (400, 250))
        player_win.play()
        state_timer += 1
        mixer.music.set_volume(0)
        if state_timer >= 120:
            state = 'game'
            mixer.music.set_volume(100)
            state_timer = 0
            win_timer = 0
            count = 0
            time_left = 60
            hearts.clear()
            lives = 3
            hearts.append(GameSprite('images/heart.png', 0, 1550, 0))
            hearts.append(GameSprite('images/heart.png', 0, 1490, 0))
            hearts.append(GameSprite('images/heart.png', 0, 1430, 0))
            score_label.set_text('Score:' + str(count))
            counter.set_text('Time left:' + str(time_left))
    for e in event.get():
        if e.type == QUIT:
            game = False
    display.update()
    clock.tick(FPS)

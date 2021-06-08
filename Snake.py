#!/usr/bin/env python

import pygame
import sys
import random
import pygame_menu
pygame.init()

surface = pygame.display.set_mode((600, 400))
bg_image = pygame.image.load('snake.jpg')
HIGH_SCORES = 'highscore.txt'
SIZE_BLOCK = 20
FRAME_COLOR = (0, 255, 204)
RED = (224, 0, 0)
WHITE = (255, 255, 255)
BLUE = (204, 255, 255)
HEADER_COLOR = (0, 204, 153)
SNAKE_COLOR = (0, 102, 0)
COUNT_BLOCKS = 20
HEADER_MARGIN = 70
MARGIN = 1
health = 3
DIFFICULTY = ['EASY']
size = (SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * SIZE_BLOCK + HEADER_MARGIN)
print(size)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snake')
timer = pygame.time.Clock()
courier = pygame.font.SysFont('courier', 28)
health_img = pygame.image.load('heart.jpg')
health_img = pygame.transform.scale(health_img, (30, 30))
    

RULES = ['In the Snake game, the player uses the','arrow keys to move the snake around',
 'the board. When the snake finds food,', 'it eats it and thus is large in size.',
 'The game ends when the snake either', 'leaves the screen or enters itself.',
 'You have 3 lives. The goal is to make the', 'snake as big as possible and earn points',
'before doing it.']
rules = pygame_menu.Menu(
        height = size[1] * 0.83,
        theme = pygame_menu.themes.THEME_GREEN,
        title = 'Rules',
        width = size[0]  * 0.95)
for m in RULES:
    rules.add.label(m ,align = pygame_menu.locals.ALIGN_LEFT, font_size = 20)
    rules.add.vertical_margin(5)

ABOUT_AUTHOR = ['My name is Viktoriia.','I am a 1st year student of WUST.',
 'I created a Snake because I remembered', 'how I loved to play if as a child.',
 'I am very glad that you are playing my game.']
about_author = pygame_menu.Menu(
        height = size[1] * 0.7,
        theme = pygame_menu.themes.THEME_GREEN,
        title = 'About author',
        width = size[0]  * 0.95)
for m in ABOUT_AUTHOR:
    about_author.add.label(m ,align = pygame_menu.locals.ALIGN_LEFT, font_size = 20)
    about_author.add.vertical_margin(5)
    
high = pygame_menu.Menu(
        height = size[1] * 0.7,
        theme = pygame_menu.themes.THEME_GREEN,
        title = 'High score',
        width = size[0]  * 0.95)
open_txt = open(HIGH_SCORES, 'r')
text = 'High score : ' + open_txt.read()
high.add.label(text, align = pygame_menu.locals.ALIGN_CENTER, font_size = 40)
high.add.image('high.jpg', angle = 0, scale = (0.15, 0.15))
open_txt.close()
    
class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.mixer.init()
        
    def inside(self):
        return 0 <= self.x < SIZE_BLOCK and 0 <= self.y < SIZE_BLOCK
    
    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y
    
    
def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1), 
                                             HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1), 
                                             SIZE_BLOCK, SIZE_BLOCK])
def highs(x):
    total1 = int(x)
    f = open(HIGH_SCORES, 'r+')
    s = f.read()
    n = int(s)
    if total1 > n:
        f = open(HIGH_SCORES, 'w+')
        f.write(str(total1))
    else:
        pass
    f.close()

def show_health():
    global health
    show = 0
    k = 330
    while show != health:
        screen.blit(health_img, (k , 20))
        k += 40
        show += 1
        
def check_health():
    global health
    health -= 1
    if health == 0:
        pygame.mixer.Sound.play()
        return False
    else:
        crash = pygame.mixer.Sound('crash.mp3')
        pygame.mixer.Sound.play(crash)
        return True

def set_difficulty(value: tuple[any, int], difficulty: str):
    selected, index = value
    print('Selected difficulty: "{0}" ({1}) at index {2}'
          ''.format(selected, difficulty, index))
    DIFFICULTY[0] = difficulty
    
def start_the_game(difficulty: list) : 
    assert isinstance(difficulty, list)
    difficulty = difficulty[0]
    assert isinstance(difficulty, str)
    
    def random_block():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_block:
            empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
            empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return empty_block

    snake_block = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
    apple = random_block()
    d_row = buf_row = 0
    d_col = buf_col = 1
    total = 0
    speed = 1

    while True:
        pygame.mixer.music.pause()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('exit')
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    buf_row = 1
                    buf_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_col = 1
                
        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0,0, size[0], HEADER_MARGIN])
    
        text_total = courier.render(f"Total: {total}", 0, WHITE)
        text_speed = courier.render(f"Speed: {speed}", 0, WHITE)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK + 160, SIZE_BLOCK))
    
        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (row + column) % 2 == 0:
                    color = BLUE
                else:
                    color = WHITE
            
                draw_block(color, row, column)
    
        head = snake_block[-1]
        
        if not head.inside():
            highs(total)
            crash = pygame.mixer.Sound('crash.mp3')
            pygame.mixer.Sound.play(crash)
            break
            
                
        
        draw_block(RED, apple.x, apple.y)
        
        for block in snake_block:
            draw_block(SNAKE_COLOR, block.x, block.y)
            
        
        pygame.display.flip()
        
        if apple == head:
            sound = pygame.mixer.Sound('sound.mp3')
            pygame.mixer.Sound.play(sound)
            total += 1
            speed = total//5 + 1
            snake_block.append(apple)
            apple = random_block()
        
        d_row = buf_row
        d_col = buf_col
      
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)
    
        if new_head in snake_block:
            highs(total)
            crash = pygame.mixer.Sound('crash.mp3')
            pygame.mixer.Sound.play(crash)
            break
            
        
        snake_block.append(new_head)
        snake_block.pop(0)
    
        if difficulty == 'EASY':
            timer.tick(3 + speed)
        elif difficulty == 'HARD':
            timer.tick(5 + speed)
        
theme = pygame_menu.themes.THEME_GREEN
theme.set_background_color_opacity(0.87)
menu = pygame_menu.Menu('Welcome', 430, 400,theme = theme)

menu.add.text_input('Name : ', default = 'Player 1')
menu.add.button('Play', start_the_game, DIFFICULTY)
menu.add.selector('Difficulty :', [('Speed low', 'EASY'), ('Speed high', 'HARD')], onchange = set_difficulty)
menu.add.button('Rules', rules)
menu.add.button('High score', high)
menu.add.button('About author', about_author)
menu.add.button('Exit', pygame_menu.events.EXIT)
pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play()

while True:

    screen.blit(bg_image, (0,0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()
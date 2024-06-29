import pygame 
from pygame.locals import *
from random import choice 

pygame.init()

# Set up the colors
GREEN = (0, 107, 56)
BLACK = (16,24,32)

# Set up the fonts
pygame.font.init()
font = pygame.font.SysFont('Roboto', 40)

# Set up the window
WIN_WIDTH, WIN_HEIGHT = 800, 600
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Language Learning using OCR")
win.fill(BLACK)

# Get the words from txt database
with open('google-10000-english-usa-no-swears-short.txt') as f:
    global words 
    words = f.readlines()

# Function to get a random word
def get_word():
    return choice(words).strip()

# Function to write text on screen 
def write_text(text, x, y, color, highlight_word):
    text = text.split()
    for i, word in enumerate(text):
        if word == highlight_word:
            text[i] = font.render(word, True, BLACK, GREEN)
        else:
            text[i] = font.render(word, True, color)
    x -= sum([t.get_width() for t in text])//2
    for t in text:
        win.blit(t, (x, y))
        x += t.get_width() + 5

# Function to draw the bounding box for the writing area
bounding_box = pygame.Rect(50, 100, 700, 400)
def draw_rect():
    pygame.draw.rect(win, GREEN, bounding_box, 3)

# Function to clear the screen
def clear_screen():
    win.fill(BLACK)
    draw_rect()

# Main loop 
running = True
word = get_word()
write_text("Write the word " + word, WIN_WIDTH//2, 15, GREEN, word)
draw_rect()
pygame.display.update()
while running:
    for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    word = get_word()
                    clear_screen()
                    write_text("Write the word " + word, WIN_WIDTH//2, 15, GREEN, word)
                    pygame.display.update()
        
    # Draw within the bounding box 
    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()
        if bounding_box.collidepoint(x, y):
            pygame.draw.circle(win, GREEN, (x, y), 5)
            pygame.display.update()
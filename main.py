import pygame 
from pygame.locals import *
from random import choice 
import easyocr
from PIL import Image

pygame.init()

# Set up the OCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Set up the colors
GREEN = (0, 107, 56)
BLACK = (16,24,32)

# Set up the fonts
pygame.font.init()
font = pygame.font.SysFont('Roboto', 40)

# Set up sound effect to play if guess is correct
pygame.mixer.init()
correct_sound = pygame.mixer.Sound('sound.mp3')
correct_sound.set_volume(0.5)

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

# Function to write text on screen, simplified to ensure text always appears
def write_text(text, x, y, color, highlight_word=None):
    words = text.split()
    total_width = sum([font.size(word)[0] for word in words]) + (len(words) - 1) * 5
    start_x = x - total_width // 2
    for word in words:
        if word == highlight_word:
            rendered_word = font.render(word, True, BLACK, GREEN)
        else:
            rendered_word = font.render(word, True, color)
        win.blit(rendered_word, (start_x, y))
        start_x += rendered_word.get_width() + 5
    pygame.display.update()  # Ensure the display is updated after drawing the text

# Function to draw the bounding box for the writing area
bounding_box = pygame.Rect(50, 100, 700, 400)
def draw_rect():
    pygame.draw.rect(win, GREEN, bounding_box, 3)

# Function to clear the screen
def clear_screen():
    win.fill(BLACK)
    draw_rect()

# Function to crop and save the image of the text user has drawn from the screen 
def save_text_image():
    pygame.image.save(win.subsurface(bounding_box), 'text_image.png')
    # change image to greyscale 
    img = Image.open('text_image.png').convert('L')
    img.save('text_image.png')

# Function to convert guess to lowercase and remove special characters and whitespace
def clean_guess(guess):
    guess = guess.lower()
    guess = ''.join(e for e in guess if e.isalnum())
    return guess

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
                elif event.key == K_1:
                    clear_screen()
                    write_text("Write the word " + word, WIN_WIDTH//2, 15, GREEN, word)
                    pygame.display.update()
                elif event.key == K_2: 
                    save_text_image()
                    print("Image saved")
                    text = reader.readtext('text_image.png')
                    print(text)
                    if text:
                        guess = clean_guess(text[0][1])
                    else:
                        guess="?"
                    print("Guess:", guess)
                    write_text("Guess: "+guess, WIN_WIDTH//2, 525, GREEN, guess)
                    if guess == word:
                        correct_sound.play()
        
    # Draw within the bounding box 
    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()
        if bounding_box.collidepoint(x, y):
            pygame.draw.circle(win, GREEN, (x, y), 3)
            pygame.display.update()
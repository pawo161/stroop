import random
import sys
import time
import pygame
import subprocess

YELLOW = (255,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
bg = [YELLOW,BLUE,RED]
color = random.choice(bg)
step = 0

pygame.init()
 # Our clock object
clock = pygame.time.Clock()
clock2 = pygame.time.Clock()

fps = 60
size = [800, 650]
screen = pygame.display.set_mode(size, 0, 32)

button = pygame.Rect(295, 295, 220, 60)
font = pygame.font.SysFont("arial", 33)    
font2 = pygame.font.SysFont("arial", 36) 

def time():
    time_passed = clock.tick(60)
    time_passed_seconds = time_passed / 1000.0
    
    print(time_passed_seconds)
    return time_passed_seconds
    
    

time_zgodne = []
time_niezgodne = []
time_wszystkie = []

def odswiezanie(czas):
    # print('button was pressed at {0}'.format(mouse_pos))
    print(czas)
    
    text2 = font.render("Średni czas to {avg} s".format(avg=avg), True, pygame.color.Color('black'))
    bg = [YELLOW,BLUE,RED]
    color = random.choice(bg)
    screen.fill(random.choice(bg))
    
    pygame.draw.rect(screen, color, button) 
    # text = font.render("Hello, World", True, color)
    # pygame.display.update()
    bg = [YELLOW,RED,BLUE]
    color = random.choice(bg)
    text_rand = ["ŻÓŁTY", "CZERWONY", "NIEBIESKI"]
    text_one = random.choice(text_rand)

    text = font2.render(text_one, True, color)
    screen.blit(text,
    (300, 300))
    if step > 1:
        if czas > 4:
            text3 = font.render("Postaraj się bardziej, ({czas} s to jakiś żart).".format(czas=czas), True, pygame.color.Color('black'))
            screen.blit(text3, (80, 100))
            pygame.display.update()
        else:
            text1 = font.render("Poprzedni czas to {czas} sekund.".format(czas=czas), True, pygame.color.Color('black'))
            screen.blit(text1, (220, 100))
            pygame.display.update()
    screen.blit(text2, (220, 150))
    pygame.display.flip()


time_passed = 0

run = True
while run:
    if step < 2:
            screen.fill(pygame.color.Color('white'))
            text0 = font.render("Instrukcja:", True, pygame.color.Color('black'))
            text5 = font.render("Prosimy o jak najszybsze mrugnięcie kiedy ", True, pygame.color.Color('black'))
            text6 = font.render("nazwa koloru i kolor tła będą zgodne. ", True, pygame.color.Color('black'))
            text7 = font.render("Mrugnij by rozpocząć. ", True, pygame.color.Color('black'))
            screen.blit(text0, (220, 150))
            screen.blit(text5, (100, 200))
            screen.blit(text6, (100, 250))
            screen.blit(text7, (100, 300))
            pygame.display.flip()
            time_passed=0
            
                
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # gets mouse position

            # checks if mouse position is over the button
            if button.collidepoint(mouse_pos):
                czas = ""
                avg = 0
                if step > 1:
                    time_passed = round(time_passed, 3)
                    czas = time_passed
                    
                    time_wszystkie.append(czas)
                
                    avg = sum(time_wszystkie)/len(time_wszystkie)
                    avg = round(avg, 3)        
                print(czas)
                # czas = float(czas)
                odswiezanie(czas)
                time_passed=0
                step += 1
                
              
    
    time_passed2 = clock2.tick(60)
    time_passed_seconds2 = time_passed2 / 1000.0
    time_passed += time_passed_seconds2
    # print(time_passed)
    if time_passed > 5:
        czas = 0
        avg = ""
        if len(time_wszystkie) > 0:
            avg = sum(time_wszystkie)/len(time_wszystkie)
            avg = round(avg, 3)   
        
        
        odswiezanie(czas)
        pygame.mixer.music.load('fail.mp3')
        pygame.mixer.music.play(0)
        time_passed=0
        step+=1
    # print(time_passed_seconds2) 
    # pygame.display.flip()
   

        
    
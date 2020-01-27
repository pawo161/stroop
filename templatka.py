# -*- coding: utf-8 -*-

from psychopy import visual, event, core
import multiprocessing as mp
import pygame as pg
import pandas as pd
import filterlib as flt
import blink as blk
#from pyOpenBCI import OpenBCIGanglion


def blinks_detector(quit_program, blink_det, blinks_num, blink,):
    def detect_blinks(sample):
        if SYMULACJA_SYGNALU:
            smp_flted = sample
        else:
            smp = sample.channels_data[0]
            smp_flted = frt.filterIIR(smp, 0)
        #print(smp_flted)

        brt.blink_detect(smp_flted, -38000)
        if brt.new_blink:
            if brt.blinks_num == 1:
                #connected.set()
                print('CONNECTED. Speller starts detecting blinks.')
            else:
                blink_det.put(brt.blinks_num)
                blinks_num.value = brt.blinks_num
                blink.value = 1

        if quit_program.is_set():
            if not SYMULACJA_SYGNALU:
                print('Disconnect signal sent...')
                board.stop_stream()
                
                
####################################################
    SYMULACJA_SYGNALU = True
####################################################
    mac_adress = 'd2:b4:11:81:48:ad'
####################################################

    clock = pg.time.Clock()
    frt = flt.FltRealTime()
    brt = blk.BlinkRealTime()

    if SYMULACJA_SYGNALU:
        df = pd.read_csv('dane_do_symulacji/data.csv')
        for sample in df['signal']:
            if quit_program.is_set():
                break
            detect_blinks(sample)
            clock.tick(200)
        print('KONIEC SYGNAŁU')
        quit_program.set()
    else:
        board = OpenBCIGanglion(mac=mac_adress)
        board.start_stream(detect_blinks)

if __name__ == "__main__":


    blink_det = mp.Queue()
    blink = mp.Value('i', 0)
    blinks_num = mp.Value('i', 0)
    #connected = mp.Event()
    quit_program = mp.Event()

    proc_blink_det = mp.Process(
        name='proc_',
        target=blinks_detector,
        args=(quit_program, blink_det, blinks_num, blink,)
        )

    # rozpoczęcie podprocesu
    proc_blink_det.start()
    print('subprocess started')

    ############################################
    # Poniżej należy dodać rozwinięcie programu
    ############################################

    core.wait(2.0)
    cnt_blinks=0
    
    import random
    import sys
    import time
    import pygame
    

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
    pygame.display.set_caption('Stroop experiment')
    fps = 60
    size = [800, 650]
    screen = pygame.display.set_mode(size, 0, 32)

    button = pygame.Rect(295, 295, 220, 60)
    font = pygame.font.SysFont("arial", 33)    
    font2 = pygame.font.SysFont("arial", 36) 

    def time():
        time_passed = clock.tick(60)
        time_passed_seconds = time_passed / 1000.0
        # print(time_passed_seconds)
        return time_passed_seconds

    time_zgodne = []
    time_niezgodne = []
    time_wszystkie = []

    def odswiezanie(czas):
        # print('button was pressed at {0}'.format(mouse_pos))
        print(czas)
        
        text2 = font.render("Średni czas to {avg} sekundy.".format(avg=avg), True, pygame.color.Color('black'))
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

        text = font2.render(text_one, True, pygame.color.Color('black'))
        screen.blit(text,
        (300, 300))
        if step > 1:
            if czas > 4:
                text3 = font.render("Postaraj się bardziej, ({czas} s to jakiś  żart).".format(czas=czas), True, pygame.color.Color('black'))
                screen.blit(text3, (80, 60))
                pygame.display.update()
            else:
                text1 = font.render("Poprzedni czas to {czas} sekundy.".format(czas=czas), True, pygame.color.Color('black'))
                screen.blit(text1, (220, 60))
                pygame.display.update()
        screen.blit(text2, (220, 110))
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

        
        if blink.value == 1:

            print('BLINK!')
            blink.value = 0
            cnt_blinks += 1
            
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
   
    
# Zakończenie podprocesów
    proc_blink_det.join()

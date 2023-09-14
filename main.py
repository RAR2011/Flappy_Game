import pygame
import random
import sys      # This will use this to exit the game
from pygame.locals import *

FPS = 32 # frame per second
SCREENWIDTH = 289
SCREENHEIGHT = 511

SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8 # %80 OF THE PICS WILL BE CONSIDERED

GAME_SPRITES = {}
GAME_SOUNDS = {}

PLAYER = 'gallery/sprites/bird.png'
Background = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'


def welcomeScreen():

    playerX = int(SCREENWIDTH / 5)
    playerY = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)

    messageX = int((SCREENHEIGHT - GAME_SPRITES['message'].get_width()) /2)
    messageY = int(SCREENHEIGHT * 0.13)
    baseX = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0,0))
                SCREEN.blit(GAME_SPRITES['player'], (playerX, playerY))
                SCREEN.blit(GAME_SPRITES['message'], (messageX, messageY))
                SCREEN.blit(GAME_SPRITES['base'], (baseX, GROUNDY))

                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score=0
    playerX = int (SCREENWIDTH / 5)
    playerY = int (SCREENWIDTH / 2)
    baseX = 0
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]


    lowerPipes = [
        {'x' : SCREENWIDTH + 200, 'y' : newPipe1[1]},
        {'x' : SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y' : newPipe2 [1] ['y'] },
    ]

    pipeVelX = -4

    pipeVelY= -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerFlappyAccv = -8      #velocity at the time of flapping
    playerFlapped = False # this is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.type == K_UP):
                if playerY > 0:
                    playerVelY = playerFlappyAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing.wav'].play()

            crashTest = isCollide(playerX, playerY, upperPipes, lowerPipes) # this function will return true if player is crashed

            if crashTest:
                return

            # check score
            playerMidPos = playerX + GAME_SPRITES['player'].get_width() /2
            for pipe in upperPipes:
                pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() /2
                if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                    score +=1
                    print (f"your score is {score}")
                    GAME_SOUNDS['point'].play()

            if playerVelY < playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY

            if playerFlapped:
                playerFlapped = False
            playerHeight = GAME_SPRITES['player'].get_height()
            playerY = playerY + min(playerVelY, GROUNDY - playerY-playerHeight)

            for upperPipes, lowerPipes in zip(upperPipes, lowerPipes):
                upperPipes['x'] += pipeVelX
                lowerPipes ['x'] += pipeVelX
            # adding a new pipe when the first pipe mis about to cross the leftmost corner of the screen
            if 0 < upperPipes[0]['x'] < 5:
                newpipe = getRandomPipe()
                upperPipes.append(newpipe[0])
                lowerPipes.append(newpipe[1])

            if upperPipes[0]['x'] <- GAME_SPRITES['pipe'][0].get_height():
                upperPipes.pop(0)
                lowerPipes.pop(0)

            SCREEN.blit(GAME_SPRITES['background'],(0,0))
            for upperPipes, lowerPipes in zip(upperPipes, lowerPipes):
                SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipes['x'], upperPipes['y']))
                SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipes['x'], lowerPipes['y']))

                SCREEN.blit(GAME_SPRITES ['base'], (baseX, GROUNDY))
                SCREEN.blit(GAME_SPRITES['base'], (playerX, playerY))
                myDigits = [int (x) for x in list(str(score))]
                width = 0
                for digit in myDigits:
                    width += GAME_SPRITES['numbers'] [digit].get_width()
                    Xoffsett = (SCREENWIDTH - width) / 2

                    for digit in myDigits:
                        SCREEN.blit(GAME_SPRITES['numbers'] [digit], (Xoffsett, SCREENHEIGHT * 0.12))
                        width += GAME_SPRITES['numbers'][digit].get_width()

                    pygame.display.update()
                    FPSCLOCK.tick(FPS)

def isCollide(playerX, playerY, upperPipes, lowerPipes):
    if playerY > GROUNDY - 25 or playerY < 0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if playerY < pipeHeight + pipe ['y'] and abs(playerX - pipe ['x'])<GAME_SPRITES['pipe'][0].get_height():
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:

        if (playerY + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerX-pipe['x']) < \
                GAME_SPRITES['pipe'] [0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False


def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_width()
    offset = SCREENHEIGHT / 3
    y2 = offset.random.randrange(0,int(SCREENHEIGHT - GAME_SPRITES['base'].get_height - 1.2 * offset))
    pipeX = SCREENHEIGHT + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x' : pipeX, 'y' : -y1},
        {'x': pipeX, 'y': y2}
    ]
    return pipe

    if __name__ == '__main__':
        pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Rohan Rijhwani')
    GAME_SPRITES['number'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.jpg').convert_alpha(),
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha(),
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
                            pygame.image.load(PIPE).convert_alpha()
                            )

    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(Background).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()
        mainGame()
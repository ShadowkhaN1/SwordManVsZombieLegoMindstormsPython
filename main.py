#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from random import randint



# image name
nameAnimationSlashLeft = "slashLEFT"
nameAnimationSlashRight = "slashRIGHT"

state = 0
countAnimation = [1, 20, 20]
isLose = False
points = 0

# screen dimensions
screenWidth = 178
screenHeight = 128

# Player parameters
playerWidth = 126
playerHeight = 100
centerXPlayer = 30
centerYPlayer = 33
playerPositionX = round((screenWidth / 2) - (playerWidth / 2))
playerPositionY = screenHeight - playerHeight + 3

#Zombie parameters
zombieWidth = 60
zombieHeight = 66

# Zombie left parameters
zombieLeftPositionX = 0 - zombieWidth
zombieLeftPositionY = screenHeight - zombieHeight

# Zombie right parameter
zombieRightPositionX = screenWidth + zombieWidth
zombieRightPositionY = screenHeight - zombieHeight

# Write your program here
brick.sound.file('zombie.wav')

touch1 = TouchSensor(Port.S1)
touch2 = TouchSensor(Port.S4)

 
def loadImages():
     counter = 0
     nameAnimation = ""
     while counter < 20:
        nameAnimation = nameAnimationSlashLeft + str(counter) + '.png'
        brick.display.image(nameAnimation, (180, 140), clear=False)
        nameAnimation = nameAnimationSlashRight + str(counter) + '.png'
        brick.display.image(nameAnimation, (180, 140), clear=False)
        brick.display.image('begin.png', clear=False)
        counter += 1


loadImages()


def showZombieRight():
    global zombieRightPositionX
    brick.display.image('zombieRight.png', (zombieRightPositionX, zombieRightPositionY), clear=False)
    
   
def showZombieLeft():
    global zombieLeftPositionX
    brick.display.image('zombieLeft.png', (zombieLeftPositionX, zombieLeftPositionY), clear=False)

def changePositionXYZombie():
    global zombieLeftPositionX
    global zombieRightPositionX
    zombieLeftPositionX += randint(1, 3)
    zombieRightPositionX -= randint(1, 3)


def isZombieLeftDead():
    global points
    global zombieLeftPositionX
    global playerPositionX
    if (zombieLeftPositionX + zombieWidth) >= (playerPositionX + 50) and (zombieLeftPositionX + zombieWidth) <= (playerPositionX + 60) and state == 1:
        zombieLeftPositionX = 0 - randint(zombieWidth, (2 * zombieWidth))
        points += 1

def isZombieLeftKill():  
    global isLose 
    if (zombieLeftPositionX + zombieWidth) >= (playerPositionX + 70):
        if state == 0:
            isLose = True 
        if state == 2:
            isLose = True 
        if state == 3:
            isLose = True    


def isZombieRightDead():
    global points
    global zombieRightPositionX
    global playerPositionX
    if zombieRightPositionX >= (playerPositionX + playerWidth - 60) and zombieRightPositionX <= (playerPositionX + playerWidth - 50) and state == 3:
        zombieRightPositionX = randint(screenWidth, (2 * screenWidth))
        points += 1


def isZombieRightKill():
    global isLose
    if zombieRightPositionX <= (playerPositionX + playerWidth - 70):
        if state == 0:
            isLose = True
        if state == 1:
            isLose = True
        if state == 2:
            isLose = True

def showPlayerAnimation(stateDef):
    counter = 0
    global state
    nameAnimation = ""

    if stateDef == 0:
        brick.display.clear()
        brick.display.image('state0.png', (playerPositionX, playerPositionY), clear=False)
        brick.display.text("Score: " + str(points), (playerPositionX, playerPositionY))
        showZombieLeft()
        showZombieRight()
        changePositionXYZombie()
        wait(60)

    if stateDef == 1:
        brick.sound.beep()
        while counter < 20:
            brick.display.clear()
            isZombieLeftDead()
            brick.display.text("Score: " + str(points), (playerPositionX, playerPositionY))
            nameAnimation = nameAnimationSlashLeft + str(counter) + '.png'
            brick.display.image(nameAnimation, (playerPositionX, playerPositionY), clear=False)
            showZombieLeft()
            showZombieRight()
            changePositionXYZombie()
            counter += 1
            wait(60)
        brick.display.clear()    
        state = 0

    if stateDef == 2:
        brick.display.clear()
        brick.display.image('state2.png', (playerPositionX, playerPositionY), clear=False)
        brick.display.text("Score: " + str(points), (playerPositionX, playerPositionY))
        showZombieLeft()
        showZombieRight()
        changePositionXYZombie()
        wait(60)

    if stateDef == 3:
        brick.sound.beep()
        while counter < 20:
            brick.display.clear()
            isZombieRightDead()
            brick.display.text("Score: " + str(points), (playerPositionX, playerPositionY))
            nameAnimation = nameAnimationSlashRight + str(counter) + '.png'
            brick.display.image(nameAnimation, (playerPositionX, playerPositionY), clear=False)
            showZombieLeft()
            showZombieRight()
            changePositionXYZombie()
            counter += 1
            wait(60) 
        brick.display.clear()         
        state = 2
    
while True:
    
    if touch1.pressed():
        state = 1

    if touch2.pressed():
        state = 3


    showPlayerAnimation(state)
    isZombieLeftKill()
    isZombieRightKill()
    brick.display.text("Score: " + str(points), (30, 30))


    if isLose == True:
        break


brick.sound.file('zombie.wav')
brick.display.image('gameOver.png')
wait(3000)








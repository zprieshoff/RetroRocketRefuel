#(lab) slide and catch
#Zechariah Prieshoff
#June 4th, 2024
#A simple, space themed slide and catch game.

import pygame
import simpleGE
import random


class SpeedBoost(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("speedBoost.png")
        self.setSize(40, 30)
        self.speed = 15
        self.reset()

    def reset(self):
        self.x = 10
        self.y = random.randint(0, self.screen.get_height())
        self.dx = self.speed

    def checkBounds(self):
        if self.right > self.screen.get_width():
            self.reset()


class Asteroid(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("asteroid.png")
        self.setSize(40, 30)
        self.minSpeed = 5
        self.maxSpeed = 9
        self.reset()

    def reset(self):
        self.x = self.screen.get_width()
        self.y = random.randint(0, self.screen.get_height())
        self.dx = -random.randint(self.minSpeed, self.maxSpeed)

    def checkBounds(self):
        if self.left < 0:
            self.reset()


class Fuel(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("fuel.png")
        self.setSize(30, 30)
        self.minSpeed = 3
        self.maxSpeed = 8
        self.reset()

    def reset(self):
        self.x = 10
        self.y = random.randint(0, self.screen.get_height())
        self.dx = random.randint(self.minSpeed, self.maxSpeed)

    def checkBounds(self):
        if self.right > self.screen.get_width():
            self.reset()


class Ship(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("spaceshipv2.png")
        self.setSize(50, 40)
        self.position = (320, 240)
        self.movespeed = 7

    def process(self):
        if self.isKeyPressed(pygame.K_UP):
            self.y -= self.movespeed
        if self.isKeyPressed(pygame.K_DOWN):
            self.y += self.movespeed


class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time left: 10"
        self.center = (500, 30)


class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100, 30)


class Game(simpleGE.Scene):
    def __init__(self, numFuels = 5, numAsteroids = 4, numSpeedBoosts = 1):
        super().__init__()
        self.setImage("arcadespace.jpg")

        self.soundFuel = simpleGE.Sound("powerup.wav")

        self.numFuels = numFuels
        self.numAsteroids = numAsteroids
        self.numSpeedBoosts = numSpeedBoosts

        self.score = 0
        self.lblScore = LblScore()
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 5
        self.lblTime = LblTime()

        self.ship = Ship(self)
        self.fuels = []
        self.asteroids = []
        self.speedBoosts = []

        for i in range(self.numFuels):
            self.fuels.append(Fuel(self))
        for i in range(self.numAsteroids):
            self.asteroids.append(Asteroid(self))
        for i in range(self.numSpeedBoosts):
            self.speedBoosts.append(SpeedBoost(self))
        self.sprites = [self.ship, self.fuels, self.asteroids, self.speedBoosts, self.lblScore, self.lblTime]

    def process(self):
        for fuel in self.fuels:
            if fuel.collidesWith(self.ship):
                fuel.reset()
                self.soundFuel.play()
                self.score += 1
                self.timer.totalTime += 0.8
                self.lblScore.text = f"Score: {self.score}"

        for asteroid in self.asteroids:
            if asteroid.collidesWith(self.ship):
                print("Hit by an asteroid!")
                self.stop()

        for speedBoost in self.speedBoosts:
            if speedBoost.collidesWith(self.ship):
                speedBoost.reset()
                self.ship.movespeed += .5

        self.lblTime.text = f"Fuel left: {self.timer.getTimeLeft():.2f}"
        if self.timer.getTimeLeft() < 0:
            print("Lost in space!")
            print(f"Score: {self.score}")
            self.stop()


class HowToPlay(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("arcadespace.jpg")

        self.howToPlay = simpleGE.Label()
        self.howToPlay.text = "How To Play"
        self.howToPlay.size = (200, 35)
        self.howToPlay.center = (320, 90)
        self.howToPlay.fgColor = (0xFF, 0xEF, 0xD5)
        self.howToPlay.bgColor = (0x1F, 0x1F, 0x1F)

        self.instructions = simpleGE.MultiLabel()
        self.instructions.fgColor = (0xFF, 0xEF, 0xD5)
        self.instructions.bgColor = (0x1F, 0x1F, 0x1F)

        self.instructions.textLines = ["To move the ship, use your up and down arrows!", "In the intro screen, press" 
                                       " Space to play", "Q to quit, D to enter game difficulties",
                                       "and H to enter how to play",
                                       "In the game difficulty screen and how to play screen", "press B to go back",
                                       "All buttons can also be clicked with your mouse!"]
        self.instructions.center = (320, 200)
        self.instructions.size = (550, 350)

        self.btnBack = simpleGE.Button()
        self.btnBack.text = "Back"
        self.btnBack.center = (320, 400)
        self.btnBack.size = (150, 30)
        self.btnBack.fgColor = (0xFF, 0xEF, 0xD5)
        self.btnBack.bgColor = (0x1F, 0x1F, 0x1F)

        self.sprites = [self.howToPlay, self.instructions, self.btnBack]

    def process(self):
        if self.btnBack.clicked or self.isKeyPressed(pygame.K_b):
            self.response = "Back"
            print("Loading title screen...")
            self.stop()


class Difficulty(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("arcadespace.jpg")

        self.difficultyTitle = simpleGE.Label()
        self.difficultyTitle.font = pygame.font.Font("Retronoid-BZX3.ttf", 20)
        self.difficultyTitle.size = (200, 35)
        self.difficultyTitle.center = (320, 100)
        self.difficultyTitle.fgColor = (0xFF, 0xEF, 0xD5)
        self.difficultyTitle.bgColor = (0x1F, 0x1F, 0x1F)
        self.difficultyTitle.text = "Game Difficulty"

        self.btnBack = simpleGE.Button()
        self.btnBack.text = "Back"
        self.btnBack.center = (320, 400)
        self.btnBack.size = (150, 30)
        self.btnBack.fgColor = (0xFF, 0xEF, 0xD5)
        self.btnBack.bgColor = (0x1F, 0x1F, 0x1F)

        self.btnEasy = simpleGE.Button()
        self.btnEasy.text = "Easy mode"
        self.btnEasy.center = (320, 200)
        self.btnEasy.size = (150, 30)
        self.btnEasy.fgColor = (0xFF, 0xEF, 0xD5)
        self.btnEasy.bgColor = (0x1F, 0x1F, 0x1F)

        self.btnNormal = simpleGE.Button()
        self.btnNormal.text = "Normal mode"
        self.btnNormal.center = (320, 250)
        self.btnNormal.size = (150, 30)
        self.btnNormal.fgColor = (0xFF, 0xEF, 0xD5)
        self.btnNormal.bgColor = (0x1F, 0x1F, 0x1F)

        self.btnHard = simpleGE.Button()
        self.btnHard.text = "Hard mode"
        self.btnHard.center = (320, 300)
        self.btnHard.size = (150, 30)
        self.btnHard.fgColor = (0xFF, 0xEF, 0xD5)
        self.btnHard.bgColor = (0x1F, 0x1F, 0x1F)

        self.difficulties = {"Easy": (8, 3, 2), "Normal": (5, 4, 1), "Hard": (4, 6, 0)}
        self.response = None

        self.sprites = [self.difficultyTitle, self.btnBack, self.btnEasy, self.btnNormal, self.btnHard]

    def process(self):
        if self.btnBack.clicked or self.isKeyPressed(pygame.K_b):
            self.response = "Back"
            print("Loading title screen...")
            self.stop()
        if self.btnEasy.clicked:
            self.response = "Easy"
            self.stop()
        if self.btnNormal.clicked:
            self.response = "Normal"
            self.stop()
        if self.btnHard.clicked:
            self.response = "Hard"
            self.stop()
        if self.response in self.difficulties:
            print(f"Loading game on {self.response} mode...")
            numFuels, numAsteroids, numSpeedBoosts = self.difficulties[self.response]
            game = Game(numFuels, numAsteroids, numSpeedBoosts)
            game.start()


class StartScreen(simpleGE.Scene):
    def __init__(self, prevScore):
        super().__init__()

        self.prevScore = prevScore

        self.setImage("arcadespace.jpg")
        self.response = "Quit"

        self.directions = simpleGE.MultiLabel()
        self.directions.fgColor = (0xFF, 0xEF, 0xD5)
        self.directions.bgColor = (0x1F, 0x1F, 0x1F)
        self.directions.font = pygame.font.Font("Retronoid-BZX3.ttf", 20)

        self.directions.textLines = ["Welcome to Retro Rocket Refuel!", "Dodge the asteroids ",
                                     "and catch fuel to continue your journey!",
                                     "Good luck Space Ranger!"]
        self.directions.center = (320, 170)
        self.directions.size = (550, 250)

        self.btnHowTo = simpleGE.Button()
        self.btnHowTo.fgColor = (0xFF, 0xEF, 0xD5)
        self.btnHowTo.bgColor = (0x1F, 0x1F, 0x1F)
        self.btnHowTo.text = "How to play"
        self.btnHowTo.center = (100, 350)
        self.btnHowTo.size = (150, 30)

        self.btnPlay = simpleGE.Button()
        self.btnPlay.fgColor = (0xFF, 0xEF, 0xD5)
        self.btnPlay.bgColor = (0x1F, 0x1F, 0x1F)
        self.btnPlay.text = "Play"
        self.btnPlay.center = (100, 400)
        self.btnPlay.size = (150, 30)

        self.btnQuit = simpleGE.Button()
        self.btnQuit.fgColor = (0xFF, 0xEF, 0xD5)
        self.btnQuit.bgColor = (0x1F, 0x1F, 0x1F)
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (540, 400)
        self.btnQuit.size = (150, 30)

        self.lblScore = simpleGE.Label()
        self.lblScore.fgColor = (0xFF, 0xEF, 0xD5)
        self.lblScore.bgColor = (0x1F, 0x1F, 0x1F)
        self.lblScore.text = "Last Score: 0"
        self.lblScore.center = (320, 400)
        self.btnQuit.size = (150, 30)
        self.lblScore.text = f"Last Score: {self.prevScore}"

        self.btnDifficulty = simpleGE.Button()
        self.btnDifficulty.fgColor = (0xFF, 0xEF, 0xD5)
        self.btnDifficulty.bgColor = (0x1F, 0x1F, 0x1F)
        self.btnDifficulty.text = "Difficulty"
        self.btnDifficulty.center = (320, 350)
        self.btnDifficulty.size = (150, 30)

        self.sprites = [self.directions, self.btnHowTo, self.btnPlay, self.btnDifficulty, self.btnQuit, self.lblScore]

    def process(self):
        if self.btnPlay.clicked or self.isKeyPressed(pygame.K_SPACE):
            self.response = "Play"
            self.stop()
        elif self.btnDifficulty.clicked or self.isKeyPressed(pygame.K_d):
            self.response = "Difficulty"
            self.stop()
        elif self.btnQuit.clicked or self.isKeyPressed(pygame.K_q):
            self.response = "Quit"
            self.stop()
        elif self.btnHowTo.clicked or self.isKeyPressed(pygame.K_h):
            self.response = "How"
            self.stop()


def main():
    keepGoing = True
    lastScore = 0

    while keepGoing:
        startScreen = StartScreen(lastScore)
        startScreen.start()

        if startScreen.response == "Difficulty":
            print("Opening Game Difficulties...")
            difficulty = Difficulty()
            difficulty.start()

        if startScreen.response == "How":
            print("Opening How To Play...")
            howToPlay = HowToPlay()
            howToPlay.start()

        if startScreen.response == "Play":
            print("Starting game...")
            game = Game()
            game.start()
            lastScore = game.score

        elif startScreen.response == "Quit":
            print("Stopping game...")
            keepGoing = False


if __name__ == "__main__":
    main()

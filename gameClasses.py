import tkinter as tk
import animations 
from collisions import collisionDetectionPlayer, projectileCollision

class Player():
    def __init__(self, canvas):
        """
        When defined, a list of variables are initalised to keep track of the players status. 
        playerObject is inialised to create animations. Its image is constantly updated between states to give the animation effect
        hitBox keeps track of the players position in regard with other objects to detect collisions. The canvas is stored as a variable.
        """
        self.canvas = canvas
        self.playerObject = self.canvas.create_image(100, 490, anchor=tk.NW)
        self.area = self.canvas.create_rectangle(165, 520, 190, 620, outline="")
        self.direction = "None"
        self.previousDirection = ""
        self.orientation = "right"
        self.runSpeed = 0
        self.score = 0
        self.coins = 0

        self.inFrame = 1
        self.jumpTime = 0
        self.jump = False
        self.jumpRight = False
        self.jumpLeft = False
        self.collision = False
        self.player = True
        self.dead = False

        self.frames = 1
        self.time = 0
        self.speed = 0
        self.image = None
        self.moveObjects = False

    def move(self, background, obstacles, keys, images):
        """
        Moves player and animates the movement, also checks for collisions
        """
        self.updateDirections(keys)
        self.checkFallState(keys)
        self.collisionDetection(obstacles)

        if self.direction == "right":
            self.orientation = "right"
            self.image = animations.runAnimation(self.canvas, self, obstacles, images, background.backgrounds)
        elif self.direction == "left":
            self.orientation = "left"
            self.image = animations.runAnimation(self.canvas, self, obstacles, images, background.backgrounds)
        elif self.direction == "fall":
            self.image = animations.fallAnimation(self.canvas, background.backgrounds, self, images, obstacles)
        elif self.direction == "jump":
            self.image = animations.jumpAnimation(self.canvas, background.backgrounds, self, images, obstacles)
        else:
            self.image = animations.idleAnimation(self.canvas, self, images)
    
    def checkFallState(self, keys):
        """
        Checks if the player is colliding with an object or it not on the ground. If yes, the player state is set to fall.
        """
        yCoordinate = self.canvas.coords(self.playerObject)[1]
        if self.jumpTime > 17 and self.direction == "jump":
            self.direction = "fall"
            self.speed = 0
            self.jumpTime = 0
        elif self.collision and self.direction == "fall":
            self.speed = 0
            self.direction = ""
            self.updateDirections(keys)
        elif self.collision:
            pass
        elif yCoordinate <= 0 and yCoordinate <= 50:
            self.direction = "fall"
            if self.frames > 3:
                self.frames=1
            self.jumpTime = 0
            self.speed = 2
        elif yCoordinate <= 490 and self.direction != "jump":
            self.direction = "fall"
            if self.frames > 3:
                self.frames=1
            self.jumpTime = 0
        elif self.direction == "fall":
            self.speed = 0
            self.direction = ""
            self.updateDirections(keys)
    
    def updateDirections(self, keys):
        if self.direction in ["jump", "fall"] and "jump" in keys:
            self.previousDirection = self.direction
            return
        elif self.direction == "fall" and not self.collision:
            return
        elif self.canvas.coords(self.playerObject)[0] <= -70 and "right" not in keys:
            self.direction = "idle"
        elif "right" in keys and "jump" in keys and not self.jump:
            self.jump = True
            self.jumpRight = True
            self.jumpLeft = False
            self.resetSpeed = False
            self.direction = "jump"
        elif "left" in keys and "jump" in keys and not self.jump:
            self.jump = True
            self.jumpLeft = True
            self.resetSpeed = False
            self.jumpRight = False
            self.direction = "jump"
        elif all(elements == "jump" for elements in keys) and len(keys) != 0 and not self.jump:
            self.jump = True
            self.jumpLeft = False
            self.jumpRight = False
            self.direction = "jump"
        elif "right" in keys:
            self.direction = "right"
        elif "left" in keys:
            self.direction = "left"
        else:
            self.direction = "idle"

        if self.direction != self.previousDirection:
            self.frames = 1
            self.speed = 0
            self.inFrame = 1
            self.fallSpeed = 0
            self.jumpSpeed = 0

            if (self.direction == "right" and self.previousDirection == "left") or (self.direction == "left" and self.previousDirection == "right") or self.direction == "idle":
                self.runSpeed = 0

        self.previousDirection = self.direction
    
    def collisionDetection(self, obstacles):
        collisionDetectionPlayer(self.canvas, self, obstacles)

class Backgrounds():
    def __init__(self, canvas, fileLocation="level.png"):
        self.filelocation = fileLocation
        self.canvas = canvas
        self.image = tk.PhotoImage(file = self.filelocation, height = 768, width = 1368)
        self.backgrounds = []
        self.change(fileLocation)
        self.Bosskey = False
        self.bossImage = tk.PhotoImage(file = "bossImage.png", height = 768, width = 1368)
    
    def change(self, fileLocation):
        self.image = tk.PhotoImage(file = self.filelocation, height = 768, width = 1368)
        for i in range(3):
            if i == 0:
                self.backgrounds.append(self.canvas.create_image(1366/2, 768/2, image = self.image, anchor=tk.CENTER))
            elif i == 1:
                self.backgrounds.append(self.canvas.create_image(2000, 768/2, image = self.image, anchor=tk.CENTER))
            else:
                self.backgrounds.append(self.canvas.create_image(3250, 768/2, image = self.image, anchor=tk.CENTER))
    
    def bossKey(self):
        if not self.Bosskey:
            self.bossCurrentBossImage = self.canvas.create_image(1366/2, 768/2, image=self.bossImage)
            self.Bosskey = True
        else:
            self.canvas.delete(self.bossCurrentBossImage)
            self.Bosskey = False


class Coin():
    def __init__(self, position, canvas):
        self.canvas = canvas
        self.coinObject = self.canvas.create_image(position[0], position[1])
        self.coinHitbox = canvas.create_rectangle(position[0] - 10, position[1] + 17, position[0] + 10, position[1] - 17, outline="")
        self.frames = 1
        self.inFrame = 1
        self.image = None
    
    def animateCoin(self, images):
        return animations.coinAnimation(self, images)
    
    def coinCollect(self, playerHitbox):
        if projectileCollision(self.canvas.coords(playerHitbox), self.canvas.coords(self.coinHitbox)):
            return True

class Enemy():
    """
    Class for creating enemy objects
    """
    def __init__(self, canvas, enemies, images, position = None,state = "run"):
        self.canvas = canvas
        self.position = position
        self.enemyState = state
        self.player = False
        self.dead = False
        self.frames = 1
        self.inFrame = 1
        self.runSpeed = 1.3
        self.orientation = "left"
        self.upOrientation = "up"
        self.image = None
        self.projectiles = []
        self.projectilesFired = 0

        if self.enemyState == "run":
            position = [position, 570]
            self.enemyObject = self.canvas.create_image(position[0], position[1])
            self.enemyHitbox = self.canvas.create_rectangle(position[0] - 35, position[1] + 60, position[0] + 35, position[1] - 60, outline="")
        else:
            position = [1600,200]
            self.enemyObject = self.canvas.create_image(position[0], position[1])
            self.enemyHitbox = self.canvas.create_rectangle(position[0] - 50, position[1] + 10, position[0] + 90, position[1] + 150, outline="")

        if len(enemies) == 0:
            enemyNumber = 1
        else:
            enemyNumber = int(enemies[-1].enemyNumber[-1:]) + 1

        self.enemyNumber = "enemy" + str(enemyNumber)
    
    def move(self, obstacles, playerHitbox, images, enemies, deathAnimations, cheatHealth):
        if self.enemyState == "run":
            self.image = animations.runAnimation(self.canvas, self, obstacles, images)
            return

        if self.canvas.coords(self.enemyHitbox)[0] >= 1200:
            self.canvas.move(self.enemyHitbox, -2, 0)
            self.canvas.move(self.enemyObject, -2, 0)

        else:
            if self.canvas.coords(self.enemyHitbox)[1] <= 50:
                self.upOrientation = "up"
            elif self.canvas.coords(self.enemyHitbox)[1] >= 480:
                self.upOrientation = "down"

            if self.upOrientation == "up":
                self.canvas.move(self.enemyHitbox, 0, 3)
                self.canvas.move(self.enemyObject, 0, 3)

            elif self.upOrientation == "down":
                self.canvas.move(self.enemyHitbox, 0, -3)
                self.canvas.move(self.enemyObject, 0, -3)

        self.image = animations.enemyAttack(self.canvas, self, images)
        self.shootProjectile(playerHitbox, cheatHealth)

    def shootProjectile(self, player, cheatHealth):
        if self.frames >= 9.5:
            if self.orientation == "right":
                self.position = self.canvas.coords(self.enemyObject)
                self.projectiles.append(self.canvas.create_oval(self.position[0] - 35, self.position[1] + 80, self.position[0] - 25, self.position[1] + 90, fill="purple", outline=""))
            else:
                self.position = self.canvas.coords(self.enemyObject)
                self.projectiles.append(self.canvas.create_oval(self.position[0] + 35, self.position[1] + 80, self.position[0] + 25, self.position[1] + 90, fill="purple", outline=""))
        for projectile in self.projectiles:
            if self.canvas.coords(projectile)[0] <= -2:
                self.projectiles.remove(projectile)
                self.canvas.delete(projectile)
            elif projectileCollision(self.canvas.coords(player.area), self.canvas.coords(projectile)):
                if not cheatHealth:
                    player.dead = True
                self.projectiles.remove(projectile)
                self.canvas.delete(projectile)
            else:
                if self.orientation == "right":
                    self.canvas.move(projectile, -3, 0)
                else:
                    self.canvas.move(projectile, 3, 0)

class Obstacles():
    """
    Class which creates different types of obstacles
    """
    def __init__(self):
        self.loadedNextObject = False
        
    def fourTile(self, canvas, xPosition, obstacles, coins, level = 1):
        self.obstacleName= "fourTile"
        self.level = level
        if level == 1:
            position = [xPosition, 580]
        else:
            position = [xPosition, 380]

        self.objectHitbox = canvas.create_rectangle(position[0] - 133, position[1] - 153, position[0] + 67, position[1] - 93, fill="grey", outline="")
        self.image = tk.PhotoImage(file = "fourTile.png")
        self.objectImage = canvas.create_image(position[0], position[1])
        obstacles.append(self)

        coins.append(Coin([position[0] + 20,position[1] - 190], canvas))
        coins.append(Coin([position[0] - 80,position[1] - 190], canvas))
    
    def twoTile(self, canvas, xPosition, obstacles, coins,level = 1):
        self.obstacleName = "twoTile"
        self.level = level
        if level == 1:
            position = [xPosition, 580]
        else:
            position = [xPosition, 380]

        self.objectHitbox = canvas.create_rectangle(position[0] - 177, position[1] - 159, position[0] - 80, position[1] - 98, fill="grey", outline="")
        self.image = tk.PhotoImage(file = "twoTile.png")
        self.objectImage = canvas.create_image(position[0], position[1])
        obstacles.append(self)

        coins.append(Coin([position[0] - 130,position[1] - 190], canvas))
    def longTile(self, canvas, xPosition, obstacles, coins, level = 1):
        self.obstcaleName = "longTile"
        self.level = level
        if level == 1:
            position = [xPosition, 580]
        else:
            position = [xPosition, 380]

        self.objectHitbox = canvas.create_rectangle(position[0] - 308, position[1] - 161, position[0] + 47, position[1] - 87, fill="grey", outline="")
        self.image = tk.PhotoImage(file = "longTile.png")
        self.objectImage = canvas.create_image(position[0], position[1])
        obstacles.append(self)

        coins.append(Coin([position[0] + 20,position[1] - 190], canvas))
        coins.append(Coin([position[0] - 80,position[1] - 190], canvas))
        coins.append(Coin([position[0] - 180,position[1] - 190], canvas))
        coins.append(Coin([position[0] - 280,position[1] - 190], canvas))
    
    def smallPipe(self, canvas, xPosition, obstacles, level = 1):
        self.obstacleName= "smallPipe"
        self.level = level
        if level == 1:
            position = [xPosition, 384]
        else:
            position = [xPosition, 380]
        
        self.objectHitbox = canvas.create_rectangle(position[0] - 98, position[1] + 90, position[0] + 91, position[1] + 240, fill="", outline="")
        self.image = tk.PhotoImage(file = "smallPipe.png")
        self.objectImage = canvas.create_image(position[0], position[1], image = self.image)
        obstacles.append(self)
    
    def bigPipe(self, canvas, xPosition, obstacles, level = 1):
        self.obstacleName = "bigPipe"
        self.level = level
        if level == 1:
            position = [xPosition, 384]
        else:
            position = [xPosition, 180]
        
        self.objectHitbox = canvas.create_rectangle(position[0] - 92, position[1] + 5, position[0] + 90, position[1] + 240, fill="", outline="")
        self.image = tk.PhotoImage(file = "bigPipe.png")
        self.objectImage = canvas.create_image(position[0], position[1], image = self.image)
        obstacles.append(self)

class GameImages():
    """
    Class that is used to store the images of all sprites and objects used in a photoimage. This is efficient as it prevents the need to keep loading the same images, which can slow down the program noticeably. Stores images as well as its flipped version to allow a seemless animation when changing direction.
    """
    def __init__(self):
        self.playerRunImages = [tk.PhotoImage(file = "WarriorModels/Run/Warrior_Run_1.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Run/Warrior_Run_2.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Run/Warrior_Run_3.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Run/Warrior_Run_4.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Run/Warrior_Run_5.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Run/Warrior_Run_6.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Run/Warrior_Run_7.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Run/Warrior_Run_8.v3.png", height = 200, width = 140)]

        self.playerRunImagesFlipped = [tk.PhotoImage(file = "WarriorModels/Run/Warrior_Run_Rotate_1.v3.png", height = 200, width = 300), tk.PhotoImage(file = "WarriorModels/Run/Warrior_Run_Rotate_2.v3.png", height = 200, width = 300), tk.PhotoImage(file = "WarriorModels/Run/Warrior_Run_Rotate_3.v3.png", height = 200, width = 300), tk.PhotoImage(file = "WarriorModels/Run/Warrior_Run_Rotate_4.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Run/Warrior_Run_Rotate_5.v3.png", height = 200, width = 300), tk.PhotoImage(file = "WarriorModels/Run/Warrior_Run_Rotate_6.v3.png", height = 200, width = 300), tk.PhotoImage(file = "WarriorModels/Run/Warrior_Run_Rotate_7.v3.png", height = 200, width = 300), tk.PhotoImage(file = "WarriorModels/Run/Warrior_Run_Rotate_8.v3.png", height = 200, width = 300)]

        self.playerIdleImages = [tk.PhotoImage(file = "WarriorModels/Idle/Warrior_Idle_1.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Idle/Warrior_Idle_2.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Idle/Warrior_Idle_3.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Idle/Warrior_Idle_4.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Idle/Warrior_Idle_5.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Idle/Warrior_Idle_6.v3.png", height = 200, width = 140)]

        self.playerIdleImagesFlipped = [tk.PhotoImage(file = "WarriorModels/Idle/Warrior_Idle_Rotate_1.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Idle/Warrior_Idle_Rotate_2.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Idle/Warrior_Idle_Rotate_3.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Idle/Warrior_Idle_Rotate_4.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Idle/Warrior_Idle_Rotate_5.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Idle/Warrior_Idle_Rotate_6.v3.png", height = 200, width = 140)]

        self.playerJumpImages = [tk.PhotoImage(file = "WarriorModels/Jump/Warrior_Jump_1.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Jump/Warrior_Jump_2.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Jump/Warrior_Jump_3.v3.png", height = 200, width = 140)]

        self.playerJumpImagesFlipped = [tk.PhotoImage(file = "WarriorModels/Jump/Warrior_Jump_Rotate_1.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Jump/Warrior_Jump_Rotate_2.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Jump/Warrior_Jump_Rotate_3.v3.png", height = 200, width = 140)]

        self.playerFallImages = [tk.PhotoImage(file = "WarriorModels/Fall/Warrior_Fall_1.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Fall/Warrior_Fall_2.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Fall/Warrior_Fall_3.v3.png", height = 200, width = 140)]

        self.playerFallImagesFlipped = [tk.PhotoImage(file = "WarriorModels/Fall/Warrior_Fall_Rotate_1.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Fall/Warrior_Fall_Rotate_2.v3.png", height = 200, width = 140), tk.PhotoImage(file = "WarriorModels/Fall/Warrior_Fall_Rotate_3.v3.png", height = 200, width = 140)]

        self.enemyRunImages = [tk.PhotoImage(file = "Enemy/Run/enemyrun1.png"), tk.PhotoImage(file = "Enemy/Run/enemyrun2.png"), tk.PhotoImage(file = "Enemy/Run/enemyrun3.png"), tk.PhotoImage(file = "Enemy/Run/enemyrun4.png"), tk.PhotoImage(file = "Enemy/Run/enemyrun5.png"), tk.PhotoImage(file = "Enemy/Run/enemyrun6.png"), tk.PhotoImage(file = "Enemy/Run/enemyrun7.png"), tk.PhotoImage(file = "Enemy/Run/enemyrun8.png")]

        self.enemyRunImagesFlipped = [tk.PhotoImage(file = "Enemy/Run/enemyrunrotate1.png"), tk.PhotoImage(file = "Enemy/Run/enemyrunrotate2.png"), tk.PhotoImage(file = "Enemy/Run/enemyrunrotate3.png"), tk.PhotoImage(file = "Enemy/Run/enemyrunrotate4.png"), tk.PhotoImage(file = "Enemy/Run/enemyrunrotate5.png"), tk.PhotoImage(file = "Enemy/Run/enemyrunrotate6.png"), tk.PhotoImage(file = "Enemy/Run/enemyrunrotate7.png"), tk.PhotoImage(file = "Enemy/Run/enemyrunrotate8.png")]

        self.enemyDeathImages = [tk.PhotoImage(file = "Enemy/Death/enemydeath1.png"), tk.PhotoImage(file = "Enemy/Death/enemydeath2.png"), tk.PhotoImage(file = "Enemy/Death/enemydeath3.png"), tk.PhotoImage(file = "Enemy/Death/enemydeath4.png")]

        self.enemyDeathImagesFlipped = [tk.PhotoImage(file = "Enemy/Death/enemydeathrotate1.png"), tk.PhotoImage(file = "Enemy/Death/enemydeathrotate2.png"), tk.PhotoImage(file = "Enemy/Death/enemydeathrotate3.png"), tk.PhotoImage(file = "Enemy/Death/enemydeathrotate4.png")]

        self.enemyAttackImages = [tk.PhotoImage(file = "Enemy/Attack/enemyattack1.png"), tk.PhotoImage(file = "Enemy/Attack/enemyattack2.png"), tk.PhotoImage(file = "Enemy/Attack/enemyattack3.png"), tk.PhotoImage(file = "Enemy/Attack/enemyattack4.png"), tk.PhotoImage(file = "Enemy/Attack/enemyattack5.png"), tk.PhotoImage(file = "Enemy/Attack/enemyattack6.png"), tk.PhotoImage(file = "Enemy/Attack/enemyattack7.png"), tk.PhotoImage(file = "Enemy/Attack/enemyattack8.png")]

        self.enemyAttackImagesFlipped = [tk.PhotoImage(file = "Enemy/Attack/enemyattackrotate1.png"), tk.PhotoImage(file = "Enemy/Attack/enemyattackrotate2.png"), tk.PhotoImage(file = "Enemy/Attack/enemyattackrotate3.png"), tk.PhotoImage(file = "Enemy/Attack/enemyattackrotate4.png"), tk.PhotoImage(file = "Enemy/Attack/enemyattackrotate5.png"), tk.PhotoImage(file = "Enemy/Attack/enemyattackrotate6.png"), tk.PhotoImage(file = "Enemy/Attack/enemyattackrotate7.png"), tk.PhotoImage(file = "Enemy/Attack/enemyattackrotate8.png")]

        self.enemyWizardDeathImages = [tk.PhotoImage(file = "Enemy/Wdeath/enemydeath1.png"), tk.PhotoImage(file = "Enemy/Wdeath/enemydeath2.png"), tk.PhotoImage(file = "Enemy/Wdeath/enemydeath3.png"), tk.PhotoImage(file = "Enemy/Wdeath/enemydeath4.png"), tk.PhotoImage(file = "Enemy/Wdeath/enemydeath5.png"), tk.PhotoImage(file = "Enemy/Wdeath/enemydeath6.png"), tk.PhotoImage(file = "Enemy/Wdeath/enemydeath7.png")]

        self.enemyWizardDeathImagesFlipped = [tk.PhotoImage(file = "Enemy/Wdeath/enemydeathrotate1.png"), tk.PhotoImage(file = "Enemy/Wdeath/enemydeathrotate2.png"), tk.PhotoImage(file = "Enemy/Wdeath/enemydeathrotate3.png"), tk.PhotoImage(file = "Enemy/Wdeath/enemydeathrotate4.png"), tk.PhotoImage(file = "Enemy/Wdeath/enemydeathrotate5.png"), tk.PhotoImage(file = "Enemy/Wdeath/enemydeathrotate6.png"), tk.PhotoImage(file = "Enemy/Wdeath/enemydeathrotate7.png")]

        self.coinImages = [tk.PhotoImage(file="Coin/coin1.v3.png"), tk.PhotoImage(file="Coin/coin2.v3.png"), tk.PhotoImage(file="Coin/coin3.v3.png"), tk.PhotoImage(file="Coin/coin4.v3.png"), tk.PhotoImage(file="Coin/coin5.v3.png")]

        self.background = tk.PhotoImage(file = "level.png")
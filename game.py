import tkinter as tk
import animations
from collisions import collisionDetectionPlayer, projectileCollision
import gameClasses

def shootProjectile(self):
    """
    Function which checks if an enemy projectile has hit the player and also moves the enemy projectile
    """
    if self.frames >= 9.5:
        if self.orientation == "right":
            self.position = canvas.coords(self.enemyObject)
            self.projectiles.append(canvas.create_oval(self.position[0] - 35, self.position[1] + 80, self.position[0] - 25, self.position[1] + 90, fill="purple", outline=""))
        else:
            self.position = canvas.coords(self.enemyObject)
            self.projectiles.append(canvas.create_oval(self.position[0] + 35, self.position[1] + 80, self.position[0] + 25, self.position[1] + 90, fill="purple", outline=""))
    for projectile in self.projectiles:
        if canvas.coords(projectile)[0] <= -2:
            self.projectiles.remove(projectile)
            canvas.delete(projectile)
        elif projectileCollision(canvas.coords(player.area), canvas.coords(projectile)):
            if not cheatHealth:
                player.dead = True
            self.projectiles.remove(projectile)
            canvas.delete(projectile)
        else:
            if self.orientation == "right":
                canvas.move(projectile, -6, 0)
            else:
                canvas.move(projectile, 6, 0)

def playerDead(enemy):
    """
    Function that checks whether an enemy has colliided with the player, if yes the player dead variable is set to true. Also checks if the player has jumped on top of the enemy, which kills the enemy.
    """
    checkProjectileCollision = projectileCollision(canvas.coords(player.area), canvas.coords(enemy.enemyHitbox), True)
    if checkProjectileCollision == "hit":
        enemy.frames = 1
        player.frames = 1
        player.direction = "jump"
        
        if enemy.enemyState != "run":
            for projectile in enemy.projectiles:
                canvas.delete(projectile)
            
        player.score += 200
        canvas.itemconfig(scoreLabel, text=" Score: " + str(player.score))
        enemies.remove(enemy)
        deathAnimations.append(enemy)
    elif checkProjectileCollision:
        if not cheatHealth:
            player.dead = True
        return True
    
    return False

def setWindow(root, height, width):
    """
    Set window size and resize attributes of root
    """
    root.geometry("{height}x{width}".format(height = height, width = width))
    root.resizable(height = False, width = False)
    root.title("Platformer")

def addKey(key):
    """
    Adds keys pressed by the player to a list
    """
    global keys

    if key not in keys:
        keys.append(key)

        if key == "right" and "left" in keys:
            keys.remove("left")
        elif key == "left" and "right" in keys:
            keys.remove("right")

def removeKey(key):
    """
    Removes key from key array when released
    """
    if key == "jump":
        player.jump = False

    global keys
    if key in keys:
        keys.remove(key)

def fallDeathAnimation():
    if not player.collision and canvas.coords(player.area)[1] <= 525:
        canvas.move(player.area, 0, 7)
        canvas.move(player.playerObject, 0, 7)
        return True
    return False

def moveObject(object, objectImage, objectHitbox,speed, list, obstacle = False):
    """
    Checks whether the object is below 700 via x coordinates. If yes, the object new object is created. Also checks if the level is over. If below -10, object is deleted.
    """
    canvas.move(objectHitbox, speed, 0)
    canvas.move(objectImage, speed, 0)

    if canvas.coords(objectHitbox)[2] < 1300:
        global gameOver
        if obstacle and not object.loadedNextObject:
            object.loadedNextObject = True
            level.pop(0)
            if len(level) == 0 or level[0] == "":
                gameOver = True
                return "Game over"
            loadLevel()
    elif canvas.coords(objectHitbox)[2] < -10:
        list.remove(object)
        canvas.delete(objectImage)
        canvas.delete(objectHitbox)
        return True

def loadLevel():
    """
    Loads the next obstacle of the level via level file.
    """
    objectToLoad = level[0].split(",")

    if objectToLoad[0].lower() == "fourtile":
        gameClasses.Obstacles().fourTile(canvas, int(objectToLoad[1]), obstacles, coins, int(objectToLoad[2]))
    elif objectToLoad[0].lower() == "twotile":
        gameClasses.Obstacles().twoTile(canvas, int(objectToLoad[1]), obstacles, coins, int(objectToLoad[2]))
    elif objectToLoad[0].lower() == "longtile":
        gameClasses.Obstacles().longTile(canvas, int(objectToLoad[1]), obstacles, coins, int(objectToLoad[2]))
    elif objectToLoad[0].lower() == "smallpipe":
        gameClasses.Obstacles().smallPipe(canvas, int(objectToLoad[1]), obstacles, int(objectToLoad[2]))
    elif objectToLoad[0].lower() == "bigpipe":
        gameClasses.Obstacles().bigPipe(canvas, int(objectToLoad[1]), obstacles, int(objectToLoad[2]))
    elif objectToLoad[0].lower() == "wizard":
        enemies.append(gameClasses.Enemy(canvas, enemies, images, state="wizard"))
        level.pop(0)
    else:
        enemies.append(gameClasses.Enemy(canvas, enemies, images, position=int(objectToLoad[1])))
        level.pop(0)

def gameLoop():
    """
    Loop for the game which checks if the player is dead or if game is over.
    """
    global gameOver
    if player.dead:
        collisionDetectionPlayer(canvas, player, obstacles)
        fallDeathAnimation()
        player.image, done = animations.playerDeathAnimation(player)
        if done:
            canvas.itemconfig(player.playerObject, image=player.image)
            if not fallDeathAnimation():
                gameOver = True
                return
    else:
        player.move(background, obstacles, keys, images)

    for enemy in enemies: 
        if player.moveObjects and enemy.enemyState == "run":
            canvas.move(enemy.enemyHitbox, -1, 0)
            canvas.move(enemy.enemyObject, -1, 0)
        elif canvas.coords(enemy.enemyHitbox)[0] < -100:
            canvas.delete(enemy.enemyObject)
            canvas.delete(enemy.enemyHitbox)
            enemies.remove(enemy)
            continue
        enemy.move(obstacles, player, images, enemies, deathAnimations, cheatHealth)
        canvas.itemconfig(enemy.enemyObject, image=enemy.image)

        if not player.dead:
            if playerDead(enemy):
                return

    for enemy in deathAnimations:
        frame, remove = animations.enemyDeathAnimation(enemy, images)
        if remove:
            canvas.delete(enemy.enemyObject)
            canvas.delete(enemy.enemyHitbox)
            deathAnimations.remove(enemy)
        else:
            canvas.itemconfig(enemy.enemyObject, image=frame)
    
    for coin in coins:
        if player.moveObjects:
            if player.runSpeed > 1.5:
                speed = -1.5
            else:
                speed = -player.runSpeed


            moveObjects = moveObject(coin, coin.coinObject, coin.coinHitbox, speed, coins)
            if moveObjects == "Game over":
                return
            elif  moveObjects:
                continue

        coin.image = coin.animateCoin(images)
        canvas.itemconfig(coin.coinObject, image=coin.image)
        if coin.coinCollect(player.area):
            player.score += 100
            canvas.itemconfig(scoreLabel, text="Score: " + str(player.score))
            player.coins += 1
            coins.remove(coin)
            canvas.delete(coin.coinObject)
            canvas.delete(coin.coinHitbox)

    if player.moveObjects:
        for obstacle in obstacles:
            if player.runSpeed > 1.5:
                speed = -1.5
            else:
                speed = -player.runSpeed
            

            moveObjects = moveObject(obstacle, obstacle.objectImage, obstacle.objectHitbox, speed, obstacles, True)
            if moveObjects == "Game over":
                return
def endGame():
    root.destroy()
def saveGame():
    """
    Saves game by saving the position of the obstacles to a save file
    """
    saveFileText = ""

    for obstacle in obstacles:
        position = obstacle.obstacleName + "," +str(int(canvas.coords(obstacle.objectImage)[0])) + "," + str(obstacle.level)

        saveFileText += position

    saveFile = open("Save.txt", "w")
    saveFileText += " ! "
    for words in level:
        saveFileText+=words + " "
    saveFileText += "! " + str(canvas.coords(player.playerObject)[0]) + "," + str(canvas.coords(player.playerObject)[1]) + "," + str(canvas.coords(player.area)[0]) + "," + str(canvas.coords(player.area)[1]) + "," + str(canvas.coords(player.area)[2]) + "," + str(canvas.coords(player.area)[3])

    saveFile.write(saveFileText)
    saveFile.close()
    root.destroy()
    
def loadGame():
    """
    loads game from save text and loads obstacles according to their position
    """
    saveFile = open("Save.txt").readline()

    for objectToLoad in saveFile.split("!")[0].strip().split(" "):
        if objectToLoad.split(",")[0].lower() == "fourtile":
            gameClasses.Obstacles().fourTile(canvas, int(objectToLoad.split(",")[1]), obstacles, coins, int(objectToLoad.split(",")[2]))
        elif objectToLoad.split(",")[0].lower() == "twotile":
            gameClasses.Obstacles().twoTile(canvas, int(objectToLoad.split(",")[1]), obstacles, coins, int(objectToLoad.split(",")[2]))
        elif objectToLoad.split(",")[0].lower() == "longtile":
            gameClasses.Obstacles().longTile(canvas, int(objectToLoad.split(",")[1]), obstacles, coins, int(objectToLoad.split(",")[2]))
        elif objectToLoad.split(",")[0].lower() == "smallpipe":
            gameClasses.Obstacles().smallPipe(canvas, int(objectToLoad.split(",")[1]), obstacles, int(objectToLoad.split(",")[2]))
        elif objectToLoad.split(",")[0].lower() == "bigpipe":
            gameClasses.Obstacles().bigPipe(canvas, int(objectToLoad.split(",")[1]), obstacles, int(objectToLoad.split(",")[2]))
        elif objectToLoad.split(",")[0].lower() == "wizard":
            enemies.append(gameClasses.Enemy(canvas, enemies, images, state="wizard"))
        elif objectToLoad.split(",")[0].lower() == "mushroom":
            enemies.append(gameClasses.Enemy(canvas, enemies, images, position=int(objectToLoad.split(",")[1])))
        


    levels = open("Level.txt", "w")
    levels.write(saveFile.split("!")[1].strip())
    playerCoordinates = saveFile.split("!")[2].strip().split(",")
    canvas.coords(player.playerObject, float(playerCoordinates[0]), float(playerCoordinates[1]))
    canvas.coords(player.area, float(playerCoordinates[2]), float(playerCoordinates[3]), float(playerCoordinates[4]), float(playerCoordinates[5]))
def pause(buttons):
    """
    Pauses game when p is pressed by breaking out of the game loop and then rejoining the loop when p is clicked again.
    """
    global paused
    if paused:
        for index, button in enumerate(buttons):
            canvas.delete(button)
            buttons.pop(index)
        paused = False
        for index, button in enumerate(buttons):
            canvas.delete(button)
            buttons.pop(index)
    else:
        buttons.append(canvas.create_window(700, 260, window=tk.Button(canvas, text= "Exit Game", command=endGame, height=3, width=40)))
        buttons.append(canvas.create_window(700, 350, window=tk.Button(canvas, text= "Save Game", command=saveGame, height=3, width=40)))
        paused = True

    startGame()

def cheatHealth():
    """
    Enables cheat if u is clicked
    """
    global cheatHealth
    cheatHealth = True

def endGameCheat():
    global gameOver
    gameOver = True

def bossImage():
    global paused
    if background.Bosskey:
        paused = False
    else:
        paused = True
    background.bossKey()
    startGame()

def startGame(load=False, name = None, keys="Arrow"):
    """
    Starts game when start game is pressed on the menu screen and initialises all variables
    """
    global initialised
    if not initialised:
        global canvas, images, background, player, scoreLabel, root, playerName
        root, playerName
        root = tk.Tk()
        playerName = name
        if keys == "Arrow":
            root.bind('<Up>', lambda event: addKey("jump"))
            root.bind('<KeyRelease-Up>', lambda event: removeKey("jump"))
            root.bind('<Right>', lambda event: addKey("right"))
            root.bind('<KeyRelease-Right>', lambda event: removeKey("right"))
            root.bind('<Left>', lambda event: addKey("left"))
            root.bind('<KeyRelease-Left>', lambda event: removeKey("left"))
            root.bind('<p>', lambda event: pause(buttons))
            root.bind('<u>', lambda event: cheatHealth())
            root.bind('<t>', lambda event: endGameCheat())
            root.bind('<b>', lambda event: bossImage())
        else:
            root.bind('<w>', lambda event: addKey("jump"))
            root.bind('<KeyRelease-w>', lambda event: removeKey("jump"))
            root.bind('<d>', lambda event: addKey("right"))
            root.bind('<KeyRelease-d>', lambda event: removeKey("right"))
            root.bind('<a>', lambda event: addKey("left"))
            root.bind('<KeyRelease-a>', lambda event: removeKey("left"))
            root.bind('<p>', lambda event: pause(buttons))
            root.bind('<u>', lambda event: cheatHealth())
            root.bind('<u>', lambda event: endGameCheat())
            root.bind('<b>', lambda event: bossImage())

        canvas = tk.Canvas(root, height = height, width = width, bg="white")
        images = gameClasses.GameImages()
        background = gameClasses.Backgrounds(canvas)
        player = gameClasses.Player(canvas)
        enemies.append(gameClasses.Enemy(canvas, enemies, images, state="wizard"))
        enemies.append(gameClasses.Enemy(canvas, enemies, images, position=1100))
        scoreLabel = canvas.create_text(70, 20, text="Score: " + str(player.score), fill="white", font=('Helvetica 15 bold'))

        setWindow(root, width, height)
        if load:
            loadGame()
        else:
            loadLevel()
        canvas.pack()
        initialised = True
    while not gameOver and not player.dead and not paused:
        gameLoop()
        canvas.itemconfig(player.playerObject, image=player.image)
        root.after(15, root.update())
    
    if gameOver and not player.dead:
        canvas.create_window(700, 400, window=tk.Label(canvas, text = "YOU WON", font=('Helvetica 15 bold', 60))) 
        root.after(5000, leaderboard)
    elif player.dead:
        canvas.create_window(700, 400, window=tk.Label(canvas, text = "GAME OVER", font=('Helvetica 15 bold', 60))) 
        root.after(5000, leaderboard)

    root.mainloop()

def createLeaderboardLabel(yPos, score):
    canvas.create_window(700, yPos, window=tk.Label(canvas, text = score, font=('Helvetica 15 bold', 25))) 

def leaderboard():
    """
    Updates leaderboard file and displays leaderboard to player
    """
    leaderboardFile = open("leaderboard.txt")
    leaderboards = leaderboardFile.read().splitlines()
    for index,score in enumerate(leaderboards):
        if int(score.split(":")[1]) <= int(player.score):
            leaderboards[index] = playerName + ":" + str(player.score)
            break
    leaderboardFile.close()

    open("leaderboard.txt", "w").close()
    leaderboardFile = open("leaderboard.txt", "a")
    
    for index,score in enumerate(leaderboards):
        if index == 0:
            leaderboardFile.write(score)
        else:
            leaderboardFile.write("\n"+score)
    leaderboardFile.close()
    canvas.delete("all")
    canvas.create_window(700, 100, window=tk.Label(canvas, text = "LEADERBOARD", font=('Helvetica 15 bold', 60)))
   
    for i in range(len(leaderboards)):
        if leaderboards[i].split(":")[0] == "None":
            continue
        score = str(i+1) + ". "+leaderboards[i].split(":")[0] + " : " + leaderboards[i].split(":")[1]
        createLeaderboardLabel(200 + i *40, score)


height, width = 768, 1366
keys = []
obstacles = []
enemies = []
deathAnimations = []
coins = []
createObstacles = []
level = open("Level.txt").readline().split(" ")
gameOver = False
initialised = False
paused = False
playerName = None
buttons = []
cheatHealth =False
root = None
canvas = None
images = None
background = None
player = None
scoreLabel = None
bossKey = False
loadedObject = False
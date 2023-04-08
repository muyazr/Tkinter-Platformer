import tkinter as tk
import collisions

"""
Assets
https://clembod.itch.io/warrior-free-animation-set
https://admurin.itch.io/parallax-backgrounds-caves
https://www.freepik.com/free-vector/different-wall-textures_959312.htm#query=pixel%20art%20ground&position=0&from_view=keyword
https://luizmelo.itch.io/monsters-creatures-fantasy
https://luizmelo.itch.io/evil-wizard-2
https://laredgames.itch.io/gems-coins-free
"""


def loopBackground(background, canvas, speed):
    """
    Constantly moves the background image when the player is moving.
    """
    for i in range(3):
        canvas.move(background[i], speed, 0)

        if canvas.coords(background[i])[0] < -675:
            canvas.coords(background[i], 3250, 768/2)

def delayFrames(object, maxFrame, frameDelay):
    """
    Delays animation frames to give a smoother animation.
    """
    if object.frames == maxFrame and object.inFrame == frameDelay:
        object.frames = 1
    elif object.inFrame < frameDelay:
        object.inFrame += 1
    else:
        object.frames += 1
        object.inFrame = 1

def moveBackground(background, canvas):
    """
    Move the background when objects are moving
    """
    for i in range(3):
        canvas.move(background[i], -3.5, 0)

        if canvas.coords(background[i])[0] < -675:
            canvas.coords(background[i], 3250, 768/2)

def runAnimation(canvas, object, obstacles, images, background = None):
    """
    Constantly changes the images of the player object/enemy object when moving to give the animation affect.
    If there are any collisions, the player speed is set to 0 to stop the player from moving. Also checks the orientation of the player and flips the image accordingly.
    """
    if not object.player:
        collisions.enemyCollision(canvas, object, obstacles)
        if object.orientation == "left":
            frame = images.enemyRunImagesFlipped[object.frames - 1]
            canvas.move(object.enemyObject, -object.runSpeed, 0)
            canvas.move(object.enemyHitbox, -object.runSpeed, 0)
        else:
            frame = images.enemyRunImages[object.frames - 1]
            canvas.move(object.enemyObject, object.runSpeed, 0)
            canvas.move(object.enemyHitbox, object.runSpeed, 0)

        delayFrames(object, 8, 10)
        return frame

    if object.runSpeed == 0:
        object.runSpeed = 0.2
    elif object.runSpeed < 7:
        object.runSpeed += 0.1

    collisions.playerCollisions(canvas, object, obstacles)

    if object.orientation == "left":
        object.moveObjects = False
        frame = images.playerRunImagesFlipped[object.frames - 1]
        canvas.move(object.playerObject, -object.runSpeed, 0)
        canvas.move(object.area, -object.runSpeed, 0)
    else:
        frame = images.playerRunImages[object.frames - 1]
        if canvas.coords(object.playerObject)[0] < 575:
            object.moveObjects = False
            canvas.move(object.area, object.runSpeed, 0)  
            canvas.move(object.playerObject, object.runSpeed, 0)
        else:
            object.moveObjects = True
            loopBackground(background, canvas, -object.runSpeed)

    delayFrames(object, 8, 20)
    return frame


def idleAnimation(canvas, object, images):
    """
    Constantly changes the image of the player with idle images when the player is standing still.
    """
    object.moveObjects = False

    if object.orientation == "left":
        frame = images.playerIdleImagesFlipped[object.frames - 1]
    else:
        frame = images.playerIdleImages[object.frames - 1]

    canvas.itemconfig(object.playerObject, image = frame)

    delayFrames(object, 6, 12)
    return frame

def fallAnimation(canvas, background, object, images, obstacles):
    """
    The speed of the player increases for the amount of time they are in the air. The speed caps out at 12. This gives the affect of gravity affecting the player. The player object is moved if they are behind the center of the screen, else the background is moved. The player image is also updated to give the animation affect of falling.
    """
    horizontalSpeed = 6

    if collisions.playerCollisions(canvas, object, obstacles):
        horizontalSpeed = 0

    if object.speed == 0:
        object.speed = 0.001
    elif object.speed < 12:
        object.speed += 0.65
    
    if object.jumpRight:
        frame = images.playerFallImages[object.frames - 1]

        if canvas.coords(object.playerObject)[0] < 575:
            object.moveObjects = False
            canvas.move(object.playerObject, horizontalSpeed, object.speed)
            canvas.move(object.area, horizontalSpeed, object.speed)
        else:
            object.moveObjects = True
            loopBackground(background, canvas, -object.runSpeed)
            canvas.move(object.area, 0, object.speed)
            canvas.move(object.playerObject, 0, object.speed)
    elif object.jumpLeft:
        frame = images.playerFallImagesFlipped[object.frames - 1]
        if canvas.coords(object.playerObject)[0] >= -70:
            object.moveObjects = False
            canvas.move(object.area, -horizontalSpeed, object.speed)
            canvas.move(object.playerObject, -horizontalSpeed, object.speed)
        else:
            object.moveObjects = False
            canvas.move(object.area, 0, object.speed)
            canvas.move(object.playerObject, 0, object.speed)
    else:
        if object.orientation == "right":
            object.moveObjects = False
            frame = images.playerFallImages[object.frames - 1]
        else:
            frame = images.playerFallImages[object.frames - 1]
        canvas.move(object.area, 0, object.speed)
        canvas.move(object.playerObject, 0, object.speed)

    delayFrames(object, 3, 9)
    return frame

def jumpAnimation(canvas, background, object, images, obstacles):
    """
    The speed of the player decreases the longer they jump. It eventually zeros out and the fall state is played. The player object is moved if they are behind the center of the screen, else the background is moved. The player image is also updated to give the animation affect of jumping.
    """
    horizontalSpeed = 6

    if collisions.playerCollisions(canvas, object, obstacles):
        horizontalSpeed = 0
    
    if object.jumpTime == 0:
        object.speed = 17
    else:
        object.speed -= 0.4

    if object.jumpRight:
        frame = images.playerJumpImages[object.frames - 1]
        if canvas.coords(object.playerObject)[0] < 575:
            object.moveObjects = False
            canvas.move(object.area, horizontalSpeed, -object.speed)
            canvas.move(object.playerObject, horizontalSpeed, -object.speed)
        else:
            object.moveObjects = True
            loopBackground(background, canvas, -object.runSpeed)
            canvas.move(object.area, 0, -object.speed)
            canvas.move(object.playerObject, 0, -object.speed)
    elif object.jumpLeft:
        frame = images.playerJumpImagesFlipped[object.frames - 1]
        object.moveObjects = False
        if canvas.coords(object.playerObject)[0] >= -70:
            canvas.move(object.area, -horizontalSpeed, -object.speed)
            canvas.move(object.playerObject, -horizontalSpeed, -object.speed)
        else:
            canvas.move(object.area, 0, -object.speed)
            canvas.move(object.playerObject, 0, -object.speed)
    else:
        object.moveObjects = False
        if object.orientation == "right":
            frame = images.playerJumpImages[object.frames - 1]
        else:
            frame = images.playerJumpImagesFlipped[object.frames - 1]
        canvas.move(object.area, 0, -object.speed)
        canvas.move(object.playerObject, 0, -object.speed)

    delayFrames(object, 3, 4)

    object.jumpTime += 1
    return frame

def enemyAttack(canvas, object, images):
    """
    Constantly updates the image of the enemy to give the animation of shooting a projectile.
    """
    if object.frames >= 9:
        object.frames = 1

    if canvas.coords(object.enemyHitbox)[0] > 575:
        frame = images.enemyAttackImagesFlipped[int(object.frames) - 1]
        object.orientation = "right"
    else:
        frame = images.enemyAttackImages[int(object.frames) - 1]
        object.orientation = "left"
    
    if object.frames == 8 and object.inFrame >= 7:
        object.frames = 1
    elif object.inFrame < 7:
        object.inFrame += 1
    elif object.frames <=3:
        object.frames += 0.5
        object.inFrame =1
    else:
        object.frames += 1
        object.inFrame = 1
    return frame

def playerDeathAnimation(object):
    """
    Player death animation for when the player dies.
    """
    done = False
    fileLocation = "WarriorModels/Death"
    currentFile = fileLocation + "/Warrior_Death_" + str(object.frames) + ".v3.png"
    frame = tk.PhotoImage(file = currentFile, height = 200, width = 140)

    if object.frames == 11 and object.inFrame == 13:
        done = True

    delayFrames(object, 11, 13)
    return frame, done

def enemyDeathAnimation(object, images):
    """
    Enemy image object is constantly updated with its death images when the enemy dies to give a death animation.
    """
    remove = False

    if object.enemyState == "run":

        if object.orientation == "left":
            frame = images.enemyDeathImagesFlipped[object.frames - 1]
        else:
            frame = images.enemyDeathImages[object.frames - 1]

        if object.frames == 4 and object.inFrame == 18:
            remove = True

        delayFrames(object, 4, 18)
        return frame, remove
    else:
        if object.orientation == "right":
            frame = images.enemyWizardDeathImagesFlipped[object.frames - 1]
        else:
            frame = images.enemyWizardDeathImages[object.frames - 1]

        if object.frames == 7 and object.inFrame == 14:
            remove = True
        
        delayFrames(object, 7, 14)
        return frame, remove

def coinAnimation(object, images):
    """
    Constantly updates the image of the coin to give an animation effect.
    """
    delayFrames(object, 5, 8)
    return images.coinImages[object.frames - 1]
        
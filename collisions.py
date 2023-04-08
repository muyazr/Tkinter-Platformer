"""
This module is used creating collision logic which is accessed by other parts of the program via an import
"""
def obstacleCollisionHorizontal(canvas, objectHitbox, object, coordinates, enemy = False):
    """
    Checks whether an object is between the x and y coordinates of another obstacle. If true, a message is returned indicating where the object is colliding with the obstacle. This is then used to set the speed of the object to 0 to prevent it going into the obstacle.
    """
    width = coordinates[2] - coordinates[0]
    depthHorizontal = 0.08 * width
    objectCoordinates = canvas.coords(objectHitbox)

    if coordinates[1] <= objectCoordinates[1] <= coordinates[3] or coordinates[1] <= objectCoordinates[3] <= coordinates[3] or enemy:
        if coordinates[0] - 10 <= canvas.coords(objectHitbox)[2] <= coordinates[0] + depthHorizontal:
            if object.orientation != "left":
                return "collisionRight"
        elif coordinates[2] - depthHorizontal <= objectCoordinates[0] <= coordinates[2]:
            if object.orientation != "right":
                return "collisionLeft"
    
    return False


def projectileCollision(player, coordinates, enemy = False):
    """"
    Checks whether an object is between the x and y coordinates of another obstacle. If true, a message is returned indicating where the object is colliding with the obstacle. This is then used to set the speed of the object to 0 to prevent it going into the obstacle.
    """
    if enemy and coordinates[1] <= player[3] <= coordinates[1] + coordinates[1] * 0.1:
        if coordinates[0] <= player[0] <= coordinates[2] or coordinates[0] <= player[2] <= coordinates[2]:
            return "hit"
    elif (coordinates[1] <= player[3] <= coordinates[3] + coordinates[3] * 0.1 or coordinates[1] <= player[1] <= coordinates[3] + coordinates[3] * 0.1)  and enemy:
        if player[0] <= coordinates[0] <= player[2] or player[0] <= coordinates[2] <= player[2]:
            return True
    elif player[1] <= coordinates[1] <= player[3] or player[1] <= coordinates[3] <= player[3]:
        if player[0] <= coordinates[0] <= player[2] or player[0] <= coordinates[2] <= player[2]:
            return True
    

def obstacleCollisionVertical(canvas, objectHitbox, object, coordinates):
    """
    Checks wether the the top coordinate of the players hitbox is colliding with the bottom y coordinate of an object. If true, the players direction is set to a fall state, which gives the effect of bouncing off the object.
    """
    width = coordinates[2] - coordinates[0]
    height = coordinates[3] - coordinates[1]
    depthHorizontal = 0.08 * width
    depthVertical = 0.9 * height
    objectCoordinates = canvas.coords(objectHitbox)

    if coordinates[3] - depthVertical <= objectCoordinates[1] <= coordinates[3] + depthVertical:
        if coordinates[0] <= objectCoordinates[0] <= coordinates[2] or coordinates[0] <= objectCoordinates[2] <= coordinates[0] + depthHorizontal:
            if object.direction != "fall":
                object.speed = 0
                object.direction = "fall"
                return True
    return False

def enemyCollision(canvas, object, obstacles):
    """
    Checks whether an enemy object has collided with an obstacle. If true, the object is turned around so it can run the other. This prevents the object from walking through obstacles.
    """
    for obstacle in obstacles:
        coordinates = canvas.coords(obstacle.objectHitbox)
        horizontalCollision = obstacleCollisionHorizontal(canvas, object.enemyHitbox, object, coordinates, True)
        
        if horizontalCollision == "collisionRight":
            object.orientation = "left"
        elif horizontalCollision == "collisionLeft":
            object.orientation = "right"

def playerCollisions(canvas, object, obstacles):
    """
    This function uses the two previously made functions obstacleCollisionVertical and obstacleCollisionHorizontal to check whether the player has collided with any obstacles. If true, the player is pushed backwards to prevent them from walking through the obstacle.
    """
    for obstacle in obstacles:
        coordinates = canvas.coords(obstacle.objectHitbox)

        if coordinates[2] < canvas.coords(object.area)[0] and object.moveObjects:
            continue

        if obstacleCollisionVertical(canvas, object.area, object, coordinates):
            if object.direction != "fall":
                object.speed = 0
                object.direction = "fall"
                return True
        elif object.collision:
            return False

        horizonalCollision = obstacleCollisionHorizontal(canvas, object.area, object, coordinates)

        if horizonalCollision == "collisionRight" and object.orientation != "left":
            canvas.move(object.playerObject, -4, 0)
            canvas.move(object.area, -4, 0)
            object.runSpeed = 0
            return True
        elif horizonalCollision == "collisionLeft" and object.orientation != "right":
            canvas.move(object.playerObject, 4, 0)
            canvas.move(object.area, 4, 0)
            object.runSpeed = 0
            return True

def collisionDetectionPlayer(canvas, object, obstacles):
    """
    Checks whether the y coordinates of the player are between the top and half way below the of an obstacle. If yes, the x coordinates of the player are checked to see if they are between the obstacles x coordinates. If yes the variable collision is set to true which allows the player to stand on top of the obstacle by disabling the fall state.
    """
    for obstacle in obstacles:
        coordinates = canvas.coords(obstacle.objectHitbox)
        height = coordinates[3] - coordinates[1]
        if object.orientation == "left":
            coordinates[0] -= 25
            coordinates[2] -= 25

        if (coordinates[0] <= canvas.coords(object.area)[0] <= coordinates[2] or coordinates[0] <= canvas.coords(object.area)[2] <= coordinates[2]) and coordinates[1] - 0.1 * height <= canvas.coords(object.area)[3] <= coordinates[1] + 0.5 * height:
            if not object.collision:
                if object.runSpeed > 6:
                    object.runSpeed = 6 
                object.jumpRight=False
                object.jumpLeft=False
            object.collision=True

            obstacles.remove(obstacle)
            obstacles.insert(0, obstacle)
            return 
        else:
            object.collision = False
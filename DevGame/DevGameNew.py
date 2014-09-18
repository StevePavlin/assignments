#!/usr/bin/python
#
#-------------------------------------------------------------------------------
# Name:    Adventure Game? IDK.
#
# Author:  Steve Pavlin
#
# Created: September 14, 2014
#-------------------------------------------------------------------------------




import sys, pygame


class Game(object):

    def __init__(self):
        pygame.init()
        
        self.screenWidth = 512
        self.screenHeight = 512
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.isRunning = False
        
        # Create a map object with a 32x32 map.
        self.mapObject = Map([[] for row in range(16)])

        # Create a player object with an initial position in the middle of the screen.
        self.playerObject = Player(self.screenWidth / 2 + 100, self.screenHeight / 2 + 160)

    # Game loop.
    def initialize(self):
       
        self.isRunning = True

        firstRun = True
        while self.isRunning:

            print(self.playerObject.gridY)
            print(self.playerObject.gridX)
            self.playerObject.updateGridXY()
 

            self.drawPlayer('idle_%s' % self.playerObject.facing, self.playerObject.x, self.playerObject.y)
            
            if firstRun:
                self.drawMap()
                self.drawPlayer('idle_south', self.playerObject.x, self.playerObject.y)
                firstRun = False

        
            if self.mapObject.mapArray[self.playerObject.gridY][self.playerObject.gridX] == '@':
                print('hit a rock')
                self.playerObject.hasCollided = True
                print(self.playerObject.hasCollided)
               

            if self.playerObject.countToOtherSide >= 40:
                 if self.playerObject.movementDirection == 0:
                     self.playerObject.movementDirection = 1
                 else:
                     self.playerObject.movementDirection = 0
                
                 self.playerObject.countToOtherSide = 0

 


            # TODO Fix collisions here.
    
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:

                if self.mapObject.mapArray[self.playerObject.gridY + 1][self.playerObject.gridX] == '#' and self.playerObject.hasCollided == True:
                    self.playerObject.hasCollided = False
                
               

                if self.playerObject.hasCollided != True:
                    self.playerObject.y += 1
               
                self.playerObject.state = 'run_south'
                self.playerObject.facing = 'south'
                self.drawPlayer(self.playerObject.state, self.playerObject.x, self.playerObject.y)
                self.playerObject.countToOtherSide += 1

            if keys[pygame.K_UP]:


                #if self.mapObject.mapArray[self.playerObject.gridY - 1][self.playerObject.gridX] == '#' and self.playerObject.hasCollided == True:
                #    self.playerObject.hasCollided = False


                if self.playerObject.hasCollided != True:
                    self.playerObject.y -= 1
                
                self.playerObject.state = 'run_north'
                self.playerObject.facing = 'north'
                self.drawPlayer(self.playerObject.state, self.playerObject.x, self.playerObject.y)
                
                self.playerObject.countToOtherSide += 1
  

            if keys[pygame.K_LEFT]:
                

                #if self.mapObject.mapArray[self.playerObject.gridY][self.playerObject.gridX + 1] == '#' and self.playerObject.hasCollided == True:
                #    self.playerObject.hasCollided = False



                if self.playerObject.hasCollided != True:
                    self.playerObject.x -= 1
                
                self.playerObject.state = 'run_west'
                self.playerObject.facing = 'west'
                self.drawPlayer(self.playerObject.state, self.playerObject.x, self.playerObject.y)
                self.playerObject.countToOtherSide += 1
  
            if keys[pygame.K_RIGHT]:


                #if self.mapObject.mapArray[self.playerObject.gridY][self.playerObject.gridX - 1] == '#' and self.playerObject.hasCollided == True:
                #    self.playerObject.hasCollided = False


                if self.playerObject.hasCollided != True:
                    self.playerObject.x += 1
                
                self.playerObject.state = 'run_east'
                self.playerObject.facing = 'east'
                self.drawPlayer(self.playerObject.state, self.playerObject.x, self.playerObject.y)
                
                self.playerObject.countToOtherSide += 1
  

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     self.isRunning = False

            pygame.display.flip()
   

    
    def drawMap(self):
        grass = pygame.image.load('grass.png')
        stone = pygame.image.load('stone.png')

        currentWidth = 0
        currentHeight = 0

        # 32 bits always...
        imageWidth = grass.get_size()[0]
        imageHeight = grass.get_size()[1]
        
        for row in self.mapObject.mapArray:
            for block in row:
                if block == '#':
                     self.screen.blit(grass, (currentWidth, currentHeight))
                if block == '@':
                    self.screen.blit(stone, (currentWidth, currentHeight))

                currentWidth += imageWidth

                if currentWidth == self.screenWidth:
                    currentHeight += imageHeight
                    currentWidth = 0
            

        """        for i in range(0, self.screenWidth):
            self.screen.blit(image, (currentWidth, currentHeight))

            currentWidth += imageWidth

            if currentWidth == self.screenWidth:
                currentHeight += imageHeight
                currentWidth = 0
        """

    def drawPlayer(self, action, xPos, yPos):
        spriteSheet = pygame.image.load('avatar.png')
        actions = {'IDLE_SOUTH_0': (0, 0, 50, 80),
        'IDLE_SOUTH_1': (100, 0, 50, 80),
        'IDLE_NORTH_0': (0, 240, 50, 80),
        'IDLE_NORTH_1': (100, 0, 50, 80),
        'IDLE_WEST_0': (0, 80, 50, 80),
        'IDLE_WEST_1': (100, 80, 50, 80),
        'IDLE_EAST_0': (0, 160, 50, 80),
        'IDLE_EAST_1': (100, 160, 50, 80),
        'RUN_SOUTH_0': (50, 0, 50, 80), 
        'RUN_SOUTH_1': (150, 0, 50, 80),
        'RUN_NORTH_0': (50, 240, 50, 80),
        'RUN_NORTH_1': (150, 240, 50, 80),
        'RUN_WEST_0': (50, 80, 50, 80), 
        'RUN_WEST_1': (150, 80, 50, 80),
        'RUN_EAST_0': (50, 160, 50, 80),
        'RUN_EAST_1': (150, 160, 50, 80)
}
        
        # Flush the screen.
        self.screen.fill((0, 0, 0))
        self.drawMap()       

        # Draw the image.


        direction = action.upper() + '_' + str(self.playerObject.movementDirection)
        self.screen.blit(spriteSheet, (xPos, yPos), actions[direction])
            
            
class Player(object):

    def __init__(self, x, y):
        # Set the player in the middle of the screen initially.
        self.x = x / 2
        self.y = y / 2 

        self.gridX = round(self.x / 32)
        self.gridY = round(self.y / 32)

        self.currentAction = 'idle'
        self.movementDirection = 0
        self.countToOtherSide = 0
        self.facing = 'south'

        self.hasCollided = False


    def updateGridXY(self):
        self.gridX = round(self.x / 32)
        self.gridY = round(self.y / 32) + 1

class Map(object):

    def __init__(self, mapArray):
        """ # is grass, @ is stone """
        self.mapArray = mapArray

    def isWalkable(self, _block):
        
        for column in self.mapArray:
            for block in column:
                if block == _block and _block == "@":
                    return False

        return True
                    


testGame = Game()

print(testGame.mapObject.mapArray)
# Populate with grass.
for column in testGame.mapObject.mapArray:
    
    for i in range(len(testGame.mapObject.mapArray)):
        column += '#'

# Draw a row of stone.
for i in range(16):
    testGame.mapObject.mapArray[2][i] = '@'

# Leave and opening
testGame.mapObject.mapArray[2][4] = '#'

print(testGame.mapObject.mapArray)
testGame.initialize()

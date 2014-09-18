import sys, pygame


pygame.init()

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game')
running = True


def avatarAction(image, action):
    
    actions = {'IDLE': (0, 0, 40, 80), 'RUN_SOUTH': (50, 0, 50, 80)}
    midPoint = (SCREEN_WIDTH / 2 - 40, SCREEN_HEIGHT / 2 - 80)
    

    screen.fill((0, 0, 0))
    #initializeGame()
    screen.blit(image, midPoint, actions[action])



def drawGrass(image):
    width = 0
    height = 0

    imageWidth = image.get_size()[0]
    imageHeight = image.get_size()[1]   

    for i in range(0, SCREEN_WIDTH):
        screen.blit(image, (width, height))
        
        width += 32

        if width == 1024:
            height += 32
            width = 0
        
        
        

        print((width, height))



def initializeGame():
    grass = pygame.image.load('grass.png')
    drawGrass(grass)
                
    avatar = pygame.image.load('avatar.png')
    avatarAction(avatar, 'IDLE')
 


gameInitialized = False
while running:

    if gameInitialized == False:
        initializeGame()
        gameInitialized = True


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                avatarAction(pygame.image.load('avatar.png'), 'RUN_SOUTH')

    pygame.display.flip()

import pygame

# pygame setup
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Noto Serif Bold', 100)
game_over_text = my_font.render('GAME OVER', True, "red")
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.display.set_caption("Snake Tron")
icon = pygame.image.load('images/motorbike.png')
player_icon = pygame.image.load('images/motorbike.png')
width = player_icon.get_rect().width
height = player_icon.get_rect().height
player_icon = pygame.transform.smoothscale(player_icon,(width/10,height/10))
pygame.display.set_icon(icon)
running = True
game_over = False
startX = 50
startY = 50
currentX = startX
currentY = startY
directionX = 1
directionY = 1

moveX = True

def player(x=startX, y=startY):
    screen.blit(player_icon, (x, y))

def draw_game_over(x=200,y=200):
    screen.blit(game_over_text, (x, y))


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # pygame.KEYDOWN
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                directionX = -1
                moveX = True
            elif event.key == pygame.K_RIGHT:
                directionX = 1
                moveX = True
            elif event.key == pygame.K_DOWN:
                directionY = 1
                moveX = False
            elif event.key == pygame.K_UP:
                directionY = -1
                moveX = False

    # Move player
    if moveX:
        currentX = currentX + 3 * directionX
    else:
        currentY = currentY + 3 * directionY

    # Check borders
    if currentX > screen.get_width() - player_icon.get_width() or currentX < 0 or currentY > screen.get_height() - player_icon.get_height() or currentY < 0:
        game_over = True


    # currentY = currentY + 2
    # fill the screen with a color
    screen.fill("black")

    if game_over:
        x = (screen.get_width() - game_over_text.get_width()) / 2
        y = (screen.get_height() - game_over_text.get_height()) / 2
        draw_game_over(x,y)
    else:
        # Display player
        player(currentX, currentY)


    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
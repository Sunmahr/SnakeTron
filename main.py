import pygame

# pygame setup
pygame.init()
pygame.font.init()
# Put a font on program
my_font = pygame.font.SysFont('Noto Serif Bold', 100)
# Set the "game over text" and "start text"
game_over_text = my_font.render('GAME OVER', True, "red")
start_text = my_font.render('Press space to start', True, "green")
# Size of screen
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
# Clock for the refresh
clock = pygame.time.Clock()
# Set name of the window
pygame.display.set_caption("Snake Tron")
# Load the picture "mortorbike"
icon = pygame.image.load('images/motorbike.png')
# Set the player icon for the game
player_icon = pygame.image.load('images/motorbike.png')
# The size of the player icon
width = player_icon.get_rect().width
height = player_icon.get_rect().height
player_icon = pygame.transform.smoothscale(player_icon,(width/10,height/10))
# Icon of the window
pygame.display.set_icon(icon)
# All Variables
running = True
game_over = False
start = True
startX = 50
startY = 50
currentX = startX
currentY = startY
directionX = 1
directionY = 1
moveX = True


def draw(object_to_draw, _x, _y):
    screen.blit(object_to_draw, (_x, _y))

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
            elif event.key == pygame.K_SPACE:
                start = False

    if not start and not game_over:
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
    if start:
        x = (screen.get_width() - start_text.get_width()) / 2
        y = (screen.get_height() - start_text.get_height()) / 2
        draw(start_text, x, y)
    elif game_over:
        x = (screen.get_width() - game_over_text.get_width()) / 2
        y = (screen.get_height() - game_over_text.get_height()) / 2
        draw(game_over_text, x, y)
    else:
        # Display player
        draw(player_icon, currentX, currentY)
        draw(icon_trail, currentX- player_icon.get_width(), currentY)

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(50)  # limits FPS to 60

pygame.quit()
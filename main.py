import pygame

# pygame setup
pygame.init()
pygame.font.init()
# Put a font on program
my_font = pygame.font.SysFont('Noto Serif Bold', 100)
# Set the "game over text" and "start text"
game_over_text = my_font.render('GAME OVER', True, "red")
start_text = my_font.render('Press space to start', True, "green")
restart_text = my_font.render('Press space to restart', True, "orange")
# Size of screen
screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
# Clock for the refresh
clock = pygame.time.Clock()
# Set name of the window
pygame.display.set_caption("Snake Tron")
# Load the picture "mortorbike"
icon = pygame.image.load('images/motorbike.png')
# Set the player icon for the game
player_icon = pygame.image.load('images/motorbike.png')
player_icon2 = pygame.image.load('images/motorbike2.png')



# Icon of the window
pygame.display.set_icon(icon)
# All Variables
running = True
game_over = False
start = True
player_size_ratio = 30000 / screen.get_width()
player_icon = pygame.transform.smoothscale(player_icon,(player_icon.get_rect().width/player_size_ratio,player_icon.get_rect().height/player_size_ratio))
startX = screen.get_width() - 50 - player_icon.get_width()
startY = 50
currentX = startX
currentY = startY
trail_size = 4
player_speed = 3.5 + screen.get_width() / 1500


half_height = player_icon.get_height() / 2
half_width = player_icon.get_width() / 2
direction = pygame.K_LEFT
list_positions = [[startX, startY + half_height]]




def is_colliding(_list_positions, rect_player):
    for pos in range(len(_list_positions) - 3):
        x1 = _list_positions[pos][0] if _list_positions[pos][0] <= _list_positions[pos + 1][0] else _list_positions[pos + 1][0]
        y1 = _list_positions[pos][1] if _list_positions[pos][1] <= _list_positions[pos + 1][1] else _list_positions[pos + 1][1]
        x2 = _list_positions[pos + 1][0] if _list_positions[pos][0] <= _list_positions[pos + 1][0] else _list_positions[pos][0]
        y2 = _list_positions[pos + 1][1] if _list_positions[pos][1] <= _list_positions[pos + 1][1] else _list_positions[pos][1]

        # Vertical line:
        if x1 == x2:
            # Check if player X is colliding:
            if rect_player.x <= x1 <= rect_player.x + rect_player.width:
                # Check if player top or bottom is colliding:
                if y1 <= rect_player.y <= y2 or y1 <= rect_player.y + rect_player.height <= y2:
                    return True
        # Horizontal line:
        if y1 == y2:
            # Check if player Y is colliding:
            if rect_player.y <= y1 <= rect_player.y + rect_player.height:
                # Check if player right or left is colliding:
                if x1 <= rect_player.x <= x2 or x1 <= rect_player.x + rect_player.width <= x2:
                    return True
    return False

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
            if event.key == pygame.K_LEFT and direction != pygame.K_RIGHT and direction != pygame.K_LEFT:
                direction = pygame.K_LEFT
                list_positions.append([currentX+half_width, currentY+half_height])
            elif event.key == pygame.K_RIGHT and direction != pygame.K_LEFT and direction != pygame.K_RIGHT:
                direction = pygame.K_RIGHT
                list_positions.append([currentX+half_width, currentY+half_height])
            elif event.key == pygame.K_DOWN and direction != pygame.K_UP and direction != pygame.K_DOWN:
                direction = pygame.K_DOWN
                list_positions.append([currentX+half_width, currentY+half_height])
            elif event.key == pygame.K_UP and direction != pygame.K_DOWN and direction != pygame.K_UP:
                direction = pygame.K_UP
                list_positions.append([currentX+half_width, currentY+half_height])
            elif event.key == pygame.K_SPACE:
                start = False
                if game_over:
                    game_over = False
                    direction = pygame.K_LEFT
                    list_positions = [[startX, startY + half_height]]
                    currentX = startX
                    currentY = startY
            elif event.key == pygame.K_ESCAPE:
                running = False

    if not start and not game_over:
        # Move player
        if direction == pygame.K_RIGHT:
            currentX = currentX + player_speed
        elif direction == pygame.K_LEFT:
            currentX = currentX - player_speed
        elif direction == pygame.K_DOWN:
            currentY = currentY + player_speed
        else:
            currentY = currentY - player_speed

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
        x = (screen.get_width() - restart_text.get_width()) / 2
        draw(restart_text, x, y+game_over_text.get_height()+5)
    else:
        if is_colliding(list_positions, pygame.Rect(currentX,currentY, player_icon.get_width(), player_icon.get_height())):
            game_over = True
        else:
            if len(list_positions) > 1:
                for i in range(len(list_positions)-3):
                    pygame.draw.line(screen, "red",list_positions[i], list_positions[i+1], width=trail_size)
                for i in range(len(list_positions)-3, len(list_positions)-1):
                    pygame.draw.line(screen, "orange", list_positions[i], list_positions[i + 1], width=trail_size)
            pygame.draw.line(screen, "yellow", list_positions[-1], [currentX+half_width, currentY + half_height], width=trail_size)

            # Display player
            draw(player_icon, currentX, currentY)


    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
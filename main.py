import pygame

class Player:
    def __init__(self, player_name, icon_ratio, start_x, start_y, speed, initial_direction = "left", trail_size = 4, right = pygame.K_RIGHT, left = pygame.K_LEFT, up = pygame.K_UP, down = pygame.K_DOWN):
        self.player_name = player_name
        self.right = right
        self.left = left
        self.up = up
        self.down = down
        self.current_y = None
        self.current_x = None
        self.positions = None
        self.direction = None
        self.current_icon = None
        self.icon_left = pygame.image.load("images/{0}_left.png".format(player_name))
        self.icon_right = pygame.transform.flip(pygame.image.load("images/{0}_left.png".format(player_name)), True, False)
        self.icon_up = pygame.transform.flip(pygame.image.load("images/{0}_down.png".format(player_name)), False, True)
        self.icon_down = pygame.image.load("images/{0}_down.png".format(player_name))
        self.icon_left = pygame.transform.smoothscale(self.icon_left, (self.icon_left.get_rect().width / icon_ratio,
                                               self.icon_left.get_rect().height / icon_ratio))
        self.icon_right = pygame.transform.smoothscale(self.icon_right, (self.icon_right.get_rect().width / icon_ratio,
                                               self.icon_right.get_rect().height / icon_ratio))
        self.icon_down = pygame.transform.smoothscale(self.icon_down, (self.icon_down.get_rect().width / icon_ratio,
                                               self.icon_down.get_rect().height / icon_ratio))
        self.icon_up = pygame.transform.smoothscale(self.icon_up, (self.icon_up.get_rect().width / icon_ratio,
                                               self.icon_up.get_rect().height / icon_ratio))
        self.start_x = start_x
        self.start_y = start_y
        self.speed = speed
        self.initial_direction = initial_direction
        self.trail_size = trail_size
        self.is_game_over = False
        self.re_init()



    def mark_position(self):
        self.positions.append([self.rect().center[0], self.rect().center[1]])

    def change_direction(self, direction):
        self.direction = direction
        if self.direction == self.left:
            self.current_icon = self.icon_left
        elif self.direction == self.right:
            self.current_icon = self.icon_right
        elif self.direction == self.up:
            self.current_icon = self.icon_up
        elif self.direction == self.down:
            self.current_icon = self.icon_down



    def check_key(self, key):
         if key in [self.left, self.right] and self.direction not in [self.right, self.left] \
                or key in [self.up, self.down] and self.direction not in [self.up, self.down]:
            self.change_direction(key)
            self.mark_position()

    def re_init(self):
        if self.initial_direction == "left":
            self.change_direction(self.left)
        elif self.initial_direction == "right":
            self.change_direction(self.right)
        elif self.initial_direction == "up":
            self.change_direction(self.up)
        else:
            self.change_direction(self.down)



        self.current_x = self.start_x
        self.current_y = self.start_y
        self.positions = [[self.rect().center[0], self.rect().center[1]]]
        self.is_game_over = False

    def move(self):
        if self.direction == self.right:
            self.current_x = self.current_x + self.speed
        elif self.direction == self.left:
            self.current_x = self.current_x - self.speed
        elif self.direction == self.down:
            self.current_y = self.current_y + self.speed
        elif self.direction == self.up:
            self.current_y = self.current_y - self.speed

    def rect(self):
        reduce = 0
        return pygame.Rect(self.current_x+reduce,self.current_y+reduce, self.current_icon.get_width()-reduce, self.current_icon.get_height()-reduce)

# pygame setup
pygame.init()
pygame.font.init()
# Put a font on program
my_font = pygame.font.SysFont('Noto Serif Bold', 100)
# Set the "game over text" and "start text"
game_over_text = my_font.render('GAME OVER', True, "red")
start_text = my_font.render('Press space to start', True, "green")
restart_text = my_font.render('Press space to restart', True, "green")
player1_win = my_font.render('Player 1 WIN', True, "yellow")
player2_win = my_font.render('Player 2 WIN', True, "lightblue")
# Size of screen
screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
# Clock for the refresh
clock = pygame.time.Clock()
# Set name of the window
pygame.display.set_caption("Snake Tron")
# Load the picture "mortorbike"
icon = pygame.image.load('images/motorbike.png')


# Icon of the window
pygame.display.set_icon(icon)
# All Variables
running = True
start = True
player_size_ratio = 150000 / screen.get_width()

player1 = Player('orange'
                 , player_size_ratio
                 , screen.get_width() - 150
                 , 50
                 , 4.5 + screen.get_width() / 1500)

player2 = Player('blue'
                 , player_size_ratio
                 , 50
                 , 50
                 , 4.5 + screen.get_width() / 1500
                 , "right"
                 , 4
                 , right = pygame.K_d
                 , left = pygame.K_q
                 , up = pygame.K_z
                 , down = pygame.K_s)




def check_screen_limit(player):
    if not player.is_game_over:
        if player.current_x > screen.get_width() - player.current_icon.get_width() or player.current_x < 0 or player.current_y > screen.get_height() - player.current_icon.get_height() or player.current_y < 0:
            player.is_game_over = True

def check_rect_colliding(rect_a, rect_b):
    return rect_a.left <= rect_b.right and rect_a.right >= rect_b.left and rect_a.top <= rect_b.bottom and rect_a.bottom >= rect_b.top

def check_trails_colliding(player_a, player_b, number_line_to_ignore = 1):
    if not player_a.is_game_over:
        _pos = player_b.positions.copy()
        _pos.append([player_b.rect().center[0], player_b.rect().center[1]])
        for pos in range(len(_pos) - number_line_to_ignore):
            x1 = _pos[pos][0] if _pos[pos][0] <= _pos[pos + 1][0] else _pos[pos + 1][0]
            y1 = _pos[pos][1] if _pos[pos][1] <= _pos[pos + 1][1] else _pos[pos + 1][1]
            x2 = _pos[pos + 1][0] if _pos[pos][0] <= _pos[pos + 1][0] else _pos[pos][0]
            y2 = _pos[pos + 1][1] if _pos[pos][1] <= _pos[pos + 1][1] else _pos[pos][1]

            rect_trail = pygame.Rect(x1, y1, x2-x1, player_b.trail_size)
            # Vertical line:
            if x1 == x2:
                rect_trail = pygame.Rect(x1, y1, player_b.trail_size, y2-y1)

            if check_rect_colliding(player_a.rect(), rect_trail):
                player_a.is_game_over = True
                break

def draw_trails(player, color1, color2, color3):
    if len(player.positions) > 1:
        for i in range(len(player.positions)-3):
            pygame.draw.line(screen, color1,player.positions[i], player.positions[i+1], width=player.trail_size)
        for i in range(len(player.positions)-3, len(player.positions)-1):
            pygame.draw.line(screen, color2, player.positions[i], player.positions[i + 1], width=player.trail_size)
    pygame.draw.line(screen, color3, player.positions[-1], player.rect().center, width=player.trail_size)

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
            player1.check_key(event.key)
            player2.check_key(event.key)
            if event.key == pygame.K_SPACE:
                start = False
                if player1.is_game_over or player2.is_game_over:
                    player1.re_init()
                    player2.re_init()
            elif event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_KP_PLUS:
                player1.speed = player1.speed + 0.5
                player2.speed = player2.speed + 0.5
            elif event.key == pygame.K_KP_MINUS:
                player1.speed = player1.speed - 0.5
                player2.speed = player2.speed - 0.5

    if not start and not (player1.is_game_over or player2.is_game_over):
        # Move player
        player1.move()
        player2.move()

    # Check borders
    check_screen_limit(player1)
    check_screen_limit(player2)
    if check_rect_colliding(player1.rect(), player2.rect()):
        player1.is_game_over = True
        player2.is_game_over = True
    check_trails_colliding(player1, player2)
    check_trails_colliding(player2, player1)
    check_trails_colliding(player1, player1, 4)
    check_trails_colliding(player2, player2, 4)


    # fill the screen with a color
    screen.fill("black")
    if start:
        x = (screen.get_width() - start_text.get_width()) / 2
        y = (screen.get_height() - start_text.get_height()) / 2
        draw(start_text, x, y)
    elif player1.is_game_over and player2.is_game_over:
        x = (screen.get_width() - game_over_text.get_width()) / 2
        y = (screen.get_height() - game_over_text.get_height()) / 2
        draw(game_over_text, x, y)
        x = (screen.get_width() - restart_text.get_width()) / 2
        draw(restart_text, x, y+game_over_text.get_height()+5)
    elif player1.is_game_over:
        x = (screen.get_width() - player2_win.get_width()) / 2
        y = (screen.get_height() - player2_win.get_height()) / 2
        draw(player2_win, x, y)
        x = (screen.get_width() - restart_text.get_width()) / 2
        draw(restart_text, x, y+player2_win.get_height()+5)
    elif player2.is_game_over:
        x = (screen.get_width() - player1_win.get_width()) / 2
        y = (screen.get_height() - player1_win.get_height()) / 2
        draw(player1_win, x, y)
        x = (screen.get_width() - restart_text.get_width()) / 2
        draw(restart_text, x, y+player1_win.get_height()+5)
    else:
        draw_trails(player1,"red", "orange", "yellow")
        draw_trails(player2, "darkblue", "cyan", "lightblue")
        # Display players
        if not player1.is_game_over or player2.is_game_over:
            draw(player1.current_icon, player1.current_x, player1.current_y)
            draw(player2.current_icon, player2.current_x, player2.current_y)

    # flip() (draw) the display
    pygame.display.flip()

    clock.tick(60)  # limits FPS

pygame.quit()

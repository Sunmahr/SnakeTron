import pygame

class Player:
    def __init__(self, icon_path, icon_ratio, start_x, start_y, speed, initial_direction = "left", trail_size = 4, right = pygame.K_RIGHT, left = pygame.K_LEFT, up = pygame.K_UP, down = pygame.K_DOWN):
        self.right = right
        self.left = left
        self.up = up
        self.down = down
        self.current_y = None
        self.current_x = None
        self.positions = None
        self.direction = None
        self.icon = pygame.image.load(icon_path)
        self.icon = pygame.transform.smoothscale(self.icon,(self.icon.get_rect().width/icon_ratio,self.icon.get_rect().height/icon_ratio))
        self.start_x = start_x
        self.start_y = start_y
        self.speed = speed
        self.initial_direction = initial_direction
        self.trail_size = trail_size
        self.is_game_over = False
        self.re_init()

    def mark_position(self):
        self.positions.append([self.current_x + self.icon.get_width() / 2, self.current_y + self.icon.get_height() / 2])

    def check_key(self, key):
         if key in [self.left, self.right] and self.direction not in [self.right, self.left] \
                or key in [self.up, self.down] and self.direction not in [self.up, self.down]:
            self.direction = key
            self.mark_position()

    def re_init(self):
        if self.initial_direction == "left":
            self.direction = self.left
        elif self.initial_direction == "right":
            self.direction = self.right
        elif self.initial_direction == "up":
            self.direction = self.up
        else:
            self.direction = self.down

        self.positions = [[self.start_x + self.icon.get_width() / 2, self.start_y + self.icon.get_height() / 2]]
        self.current_x = self.start_x
        self.current_y = self.start_y
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
        return pygame.Rect(self.current_x,self.current_y, self.icon.get_width(), self.icon.get_height())

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


# Icon of the window
pygame.display.set_icon(icon)
# All Variables
running = True
game_over = False
start = True
player_size_ratio = 30000 / screen.get_width()

player1 = Player('images/motorbike.png'
                 , player_size_ratio
                 , screen.get_width() - 50
                 , 50
                 , 3.5 + screen.get_width() / 1500)

player2 = Player('images/motorbike2.png'
                 , player_size_ratio
                 , 50
                 , 50
                 , 3.5 + screen.get_width() / 1500
                 , "right"
                 , 4
                 , right = pygame.K_d
                 , left = pygame.K_q
                 , up = pygame.K_z
                 , down = pygame.K_s)


def check_screen_limit(player):
    if not player.is_game_over:
        if player.current_x > screen.get_width() - player.icon.get_width() or player.current_x < 0 or player.current_y > screen.get_height() - player.icon.get_height() or player.current_y < 0:
            player.is_game_over = True

def check_rect_colliding(rect_a, rect_b):
    return rect_a.left <= rect_b.right and rect_a.right >= rect_b.left and rect_a.top <= rect_b.bottom and rect_a.bottom >= rect_b.top

def check_trails_colliding(player_a, player_b, number_line_to_ignore = 1):
    if not player_a.is_game_over and len(player_b.positions) > 1:
        for pos in range(len(player_b.positions) - number_line_to_ignore):
            x1 = player_b.positions[pos][0] if player_b.positions[pos][0] <= player_b.positions[pos + 1][0] else player_b.positions[pos + 1][0]
            y1 = player_b.positions[pos][1] if player_b.positions[pos][1] <= player_b.positions[pos + 1][1] else player_b.positions[pos + 1][1]
            x2 = player_b.positions[pos + 1][0] if player_b.positions[pos][0] <= player_b.positions[pos + 1][0] else player_b.positions[pos][0]
            y2 = player_b.positions[pos + 1][1] if player_b.positions[pos][1] <= player_b.positions[pos + 1][1] else player_b.positions[pos][1]

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
                if game_over:
                    game_over = False
                    player1.re_init()
                    player2.re_init()
            elif event.key == pygame.K_ESCAPE:
                running = False

    if not start and not game_over:
        # Move player
        player1.move()
        player2.move()

    # Check borders
    check_screen_limit(player1)
    check_screen_limit(player2)
    if check_rect_colliding(player1.rect(), player2.rect()):
        game_over = True
    check_trails_colliding(player1, player2)
    check_trails_colliding(player2, player1)
    check_trails_colliding(player1, player1, 3)
    check_trails_colliding(player2, player2, 3)


    if player1.is_game_over or player2.is_game_over:
        game_over = True

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
        draw_trails(player1,"red", "orange", "yellow")
        draw_trails(player2, "darkblue", "cyan", "lightblue")
        # Display players
        if not player1.is_game_over:
            draw(player1.icon, player1.current_x, player1.current_y)

        if not player2.is_game_over:
            draw(player2.icon, player2.current_x, player2.current_y)

    # flip() (draw) the display
    pygame.display.flip()

    clock.tick(60)  # limits FPS

pygame.quit()

"""
  יבצה שחנ
Snake Eater
Made with PyGaime
"""

import pygame, sys, time, random


# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120

DIFFICULTY = 25
difficulty = DIFFICULTY

# Window size
frame_size_x = 720
frame_size_y = 480


# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

pygame.init()

#info = pygame.display.Info()
#print(info)


#frame_size_y = info.current_h
#frame_size_x = info.current_w
# Initialise game window
pygame.display.set_caption('נחש הצבי')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y), pygame.RESIZABLE | pygame.DOUBLEBUF)


# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# Game variables
snake_pos = None
snake_body = None
score = 0

def init():
    global snake_pos
    global snake_body
    global score
    global difficulty
    score = 0
    difficulty = DIFFICULTY
    snake_pos = [100, 50]
    snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

init()

random.seed(21)
food_pos = [[random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10] for i in range(33)]
food_spawn = True

direction = 'RIGHT'
change_to = direction


# Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU STILL ALIVE!', True, green )
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
#    game_window.fill(black)
#    pygame.display.flip()
    init()
#    pygame.quit()
#    sys.exit()


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()

_sleep = 0
_change_to_save = 'RIGHT'

_events = []

tapS = pygame.mixer.Sound("tapuah.aiff")
scrS = pygame.mixer.Sound("titss.wav")
music = pygame.mixer.music.load("music.mp3")

pygame.mixer.music.play(-1) 

# Main logic
while True:
    #info = pygame.display.Info()
    #print(info)
    #frame_size_y = info.current_h
    #frame_size_x = info.current_w
    # frame_size_x, frame_size_y = game_window.get_size()
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            game_window = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
            frame_size_y, frame_size_x = event.h, event.w

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if event.key == ord('b'):
                print("'b' pressed")
                _change_to_save = change_to
                change_to = 'BREAK'

   # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if change_to == 'BREAK':
        import pdb
        pdb.set_trace()
        change_to = _change_to_save

    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    i = -1
    _eat = False
    for _food in food_pos:
        i += 1
        if snake_pos[0] == _food[0] and snake_pos[1] == _food[1]:
            _eat = True
            break

    if _eat:
        score += 1
        if score % 10 == 0:
            difficulty += 5
            scrS.play()
        else:
            tapS.play()

        food_pos.pop(i)
        food_pos.append([random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10])
    else:
        snake_body.pop()
    
    # GFX
    game_window.fill(black)
    for pos in snake_body:
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))


    # Snake food
    for _food in food_pos:
        pygame.draw.rect(game_window, white, pygame.Rect(_food[0], _food[1], 10, 10))

    # Game Over conditions
    # Getting out of bounds
    if snake_pos[0] < 0:
        snake_pos[0] = frame_size_x-10

    if snake_pos[0] > frame_size_x-10:
        snake_pos[0] = 0

    if snake_pos[1] > frame_size_y-10:
        snake_pos[1] = 0
    elif snake_pos[1] <= 0:
        snake_pos[1] = frame_size_y-10

#    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
#        game_over()
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score(1, white, 'consolas', 20)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)

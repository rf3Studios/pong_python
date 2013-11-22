"""
The MIT License (MIT)

Copyright (c)2013 Rich Friedel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
##################################################
#                 !IMPORTANT!                    #
# You must have PyGame installed for this to run #
# Download: http://www.pygame.org/download.shtml #
##################################################
import sys
import pygame
import random

if not pygame.font:
    print('Warning! PyGame fonts disabled!')
else:
    pygame.font.init()

# Constants
FRAME_WIDTH = 600
FRAME_HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 10
PAD_HEIGHT = 80
PAD_VELOCITY = 3.5
GAME_TITLE = "Pong Clone"
WHITE_COLOR = (255, 255, 255)
DIR_RIGHT = True
DIR_LEFT = False
PLAYER_LEFT = 0
PLAYER_RIGHT = 1


def spawn_ball(direction):
    global ball_pos, ball_vel

    ball_pos = [FRAME_WIDTH // 2, FRAME_HEIGHT // 2]

    x_vel = random.randrange(120, 240) / 60
    y_vel = random.randrange(60, 180) / 60

    if direction == DIR_RIGHT:
        x_vel *= -1

    ball_vel = [x_vel, -y_vel]


def new_game():
    global paddle_left_pos, paddle_right_pos, paddle_left_vel, paddle_right_vel
    global score_left, score_right

    # Set player scores
    score_left = 0
    score_right = 0

    # Set paddle positions
    paddle_left_pos = (FRAME_HEIGHT / 2) - (PAD_HEIGHT / 2)
    paddle_right_pos = (FRAME_HEIGHT / 2) - (PAD_HEIGHT / 2)

    # Set paddle velocities
    paddle_left_vel = 0
    paddle_right_vel = 0

    # Choose a random direction that the ball will travel
    if random.randrange(0, 2) == 1:
        _direction = DIR_RIGHT
    else:
        _direction = DIR_LEFT

    # Spawn the ball in the direction that was randomly generated
    spawn_ball(_direction)


def draw_handler(surface):
    """Draws to the surface every iteration"""
    # Clear surface
    surface.fill((0, 0, 0))

    # Draw midline and gutters
    pygame.draw.line(surface, WHITE_COLOR, (FRAME_WIDTH / 2, 0), (FRAME_WIDTH / 2, FRAME_HEIGHT), 1)
    pygame.draw.line(surface, WHITE_COLOR, (PAD_WIDTH, 0), (PAD_WIDTH, FRAME_HEIGHT), 1)
    pygame.draw.line(surface, WHITE_COLOR, (FRAME_WIDTH - PAD_WIDTH, 0),
                     (FRAME_WIDTH - PAD_WIDTH, FRAME_HEIGHT), 1)

    # Draw ball
    render_ball(surface)

    # Draw paddles
    render_paddles(surface)

    # Draw player scores
    draw_text_helper(surface, score_left, (125, 50), 72, WHITE_COLOR)
    draw_text_helper(surface, score_right, (425, 50), 72, WHITE_COLOR)

    pygame.display.update()


def keydown_handler(event_key):
    """Invoked when the user presses a keyboard key"""
    global paddle_left_vel, paddle_right_vel

    # Left player paddle
    if event_key == 115:
        paddle_left_vel = PAD_VELOCITY
    elif event_key == 119:
        paddle_left_vel = -PAD_VELOCITY

    if event_key == 274:
        paddle_right_vel = PAD_VELOCITY
    elif event_key == 273:
        paddle_right_vel = -PAD_VELOCITY


def keyup_handler(event_key):
    """Invoked when the user releases a pressed key on the keyboard"""
    global paddle_left_vel, paddle_right_vel

    if event_key == 119 or event_key == 115:
        paddle_left_vel = 0

    if event_key == 273 or event_key == 274:
        paddle_right_vel = 0


def frame():
    """Creates a new game surface for the game to run in"""
    new_game()

    # Create the surface
    _game_surface = pygame.display.set_mode((FRAME_WIDTH, FRAME_HEIGHT))

    # Set the title
    pygame.display.set_caption(GAME_TITLE)

    # Set clock
    _clock = pygame.time.Clock()

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                keydown_handler(event.key)
            elif event.type == pygame.KEYUP:
                keyup_handler(event.key)

        draw_handler(_game_surface)

        # FPS limit to 60 -- essentially, setting the draw handler timing
        # it micro pauses so while loop only runs 60 times a second max.
        _clock.tick(60)

# Helpers
def render_ball(surface):
    global ball_pos, ball_vel

    ball_pos[0] = int(ball_pos[0])
    ball_pos[1] = int(ball_pos[1])

    # Update ball
    if ball_pos[0] + (BALL_RADIUS + PAD_WIDTH) >= FRAME_WIDTH:
        # Check to see if the ball is colliding with the paddle
        if paddle_right_pos < ball_pos[1] < paddle_right_pos + PAD_HEIGHT:
            ball_vel[0] = (ball_vel[0] + 0.1) * -1
        else:
            player_score(PLAYER_LEFT)
            spawn_ball(DIR_RIGHT)

    if ball_pos[0] - (BALL_RADIUS + PAD_WIDTH) <= 0:
        # Check to see if the ball is colliding with the paddle
        if paddle_left_pos < ball_pos[1] < paddle_left_pos + PAD_HEIGHT:
            ball_vel[0] = (ball_vel[0] - 0.1) * -1
        else:
            player_score(PLAYER_RIGHT)
            spawn_ball(DIR_LEFT)

    # If ball hits the top or bottom
    if ball_pos[1] - BALL_RADIUS == 0:
        ball_vel[1] *= -1

    if ball_pos[1] + BALL_RADIUS == FRAME_HEIGHT:
        ball_vel[1] *= -1

    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    print(ball_vel)

    pygame.draw.circle(surface, WHITE_COLOR, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS, 0)


def render_paddles(surface):
    global paddle_left_vel, paddle_right_vel, paddle_left_pos, paddle_right_pos

    # Update paddle velocity
    if 0 <= paddle_left_vel + paddle_left_pos + paddle_left_vel <= FRAME_HEIGHT - PAD_HEIGHT:
        paddle_left_pos += paddle_left_vel

    if 0 <= paddle_right_vel + paddle_right_pos + paddle_right_vel <= FRAME_HEIGHT - PAD_HEIGHT:
        paddle_right_pos += paddle_right_vel

    # Draw paddles
    pygame.draw.line(surface, WHITE_COLOR, (PAD_WIDTH / 2, paddle_left_pos),
                     (PAD_WIDTH / 2, paddle_left_pos + PAD_HEIGHT), PAD_WIDTH)
    pygame.draw.line(surface, WHITE_COLOR, (FRAME_WIDTH - PAD_WIDTH / 2, paddle_right_pos),
                     (FRAME_WIDTH - PAD_WIDTH / 2, paddle_right_pos + PAD_HEIGHT), PAD_WIDTH)


def draw_text_helper(surface, value, pos, size, color, font="sans-serif"):
    """Helper that creates the blit for PyGame to render text on the surface"""
    _font_object = pygame.font.Font(pygame.font.match_font(font), size)
    _font_draw = _font_object.render(str(value), True, color)
    surface.blit(_font_draw, pos)


def player_score(player):
    global score_left, score_right

    if player == PLAYER_LEFT:
        score_left += 1
    elif player == PLAYER_RIGHT:
        score_right += 1


def main():
    frame()


if __name__ == '__main__':
    main()
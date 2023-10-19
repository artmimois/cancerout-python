import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()

pygame.mixer.init()


try:
    pygame.mixer.music.load('gsk.mp3')
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"Error loading music: {e}")


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

def display_briefing():
    screen.fill(WHITE)

    font_1 = pygame.font.SysFont('Arial', 20)
    briefing_texts = [
        ("Let's kill the   ", ORANGE, (SCREEN_WIDTH / 2 - 60, SCREEN_HEIGHT / 2 - 20)),
        ("CANCER", RED, (SCREEN_WIDTH / 2 + 30, SCREEN_HEIGHT / 2 - 20)),
        (" cell!", ORANGE, (SCREEN_WIDTH / 2 + 90, SCREEN_HEIGHT / 2 - 20)),
        ("Controls:", ORANGE, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 10)),
        ("Left Syringe - W & S", ORANGE, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40)),
        ("Right Syringe - " + '\u2191' + " & " + '\u2193', ORANGE, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 70)),
        ("Press ENTER to start", ORANGE, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 110))
    ]

    for text, color, pos in briefing_texts:
        rendered_text = font_1.render(text, True, color)
        text_rect = rendered_text.get_rect(center=pos)
        screen.blit(rendered_text, text_rect)

    pygame.display.flip()

initial_ball_radius = 120
ball_radius = initial_ball_radius
min_ball_radius = 5  

ball = pygame.Rect(SCREEN_WIDTH//2 - ball_radius//2, SCREEN_HEIGHT//2 - ball_radius//2, ball_radius, ball_radius)
ball_speed = [3, 3]

left_paddle = pygame.Rect(10, SCREEN_HEIGHT//2 - 50, 100, 20)
right_paddle = pygame.Rect(SCREEN_WIDTH - 110, SCREEN_HEIGHT//2 - 50, 100, 20)
paddle_speed = 6

def draw_syringe(surface, rect, color, direction="left"):
    body_length = rect.width * 0.6
    needle_length = rect.width * 0.4
    
    body_rect = pygame.Rect(rect.x, rect.y, body_length, rect.height) if direction == "left" else pygame.Rect(rect.right - body_length, rect.y, body_length, rect.height)
    needle_rect = pygame.Rect(body_rect.right, rect.top + rect.height//2 - rect.height//8, needle_length, rect.height // 4) if direction == "left" else pygame.Rect(rect.x, rect.top + rect.height//2 - rect.height//8, needle_length, rect.height // 4)
    
    pygame.draw.rect(surface, color, body_rect)
    pygame.draw.rect(surface, color, needle_rect)
    
    pygame.draw.rect(surface, BLACK, body_rect, 2)
    pygame.draw.rect(surface, BLACK, needle_rect, 2)

    myfont = pygame.font.SysFont('Arial', 15)
    text = myfont.render('GSK', True, WHITE)
    text_rect = text.get_rect(center=body_rect.center)
    surface.blit(text, text_rect)

success = False

is_briefing = True

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_RETURN:
            is_briefing = False

    if is_briefing:
        display_briefing()
        continue

    # Ball movement
    ball.move_ip(ball_speed)
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed[1] = -ball_speed[1]
    if not success:
        if ball.colliderect(left_paddle):
            ball_speed[0] = -ball_speed[0]
            ball.left = left_paddle.right  
            ball_radius = max(min_ball_radius, ball_radius - 5)  
            ball.width = ball_radius
            ball.height = ball_radius
        elif ball.colliderect(right_paddle):
            ball_speed[0] = -ball_speed[0]
            ball.right = right_paddle.left  
            ball_radius = max(min_ball_radius, ball_radius - 5)
            ball.width = ball_radius
            ball.height = ball_radius

    if ball_radius <= min_ball_radius:
        success = True

    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        ball_radius = initial_ball_radius
        ball.width = ball_radius
        ball.height = ball_radius
        success = False
        ball_speed[0] = -ball_speed[0]

    keys = pygame.key.get_pressed()
    if keys[K_UP] and right_paddle.top > 0:
        right_paddle.move_ip(0, -paddle_speed)
    if keys[K_DOWN] and right_paddle.bottom < SCREEN_HEIGHT:
        right_paddle.move_ip(0, paddle_speed)
    if keys[K_w] and left_paddle.top > 0:
        left_paddle.move_ip(0, -paddle_speed)
    if keys[K_s] and left_paddle.bottom < SCREEN_HEIGHT:
        left_paddle.move_ip(0, paddle_speed)

    # Rendering
    screen.fill(WHITE)
    if not success:
        pygame.draw.ellipse(screen, RED, ball)
        pygame.draw.ellipse(screen, BLACK, ball, 2)
        draw_syringe(screen, left_paddle, ORANGE, "left")
        draw_syringe(screen, right_paddle, ORANGE, "right")

        font_size = int(25 * (ball_radius / initial_ball_radius))
        myfont = pygame.font.SysFont('Arial', font_size)
        text = myfont.render('CANCER', False, WHITE)
        text_rect = text.get_rect(center=ball.center)
        screen.blit(text, text_rect)
    else:
        myfont = pygame.font.SysFont('Arial', 50)
        text = myfont.render('SUCCESS!', False, ORANGE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(text, text_rect)

    pygame.display.flip()

    pygame.time.Clock().tick(60)  # 60 FPS

pygame.quit()

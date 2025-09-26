import pygame
import random

# --- 常數 ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# 尺寸建議
PADDLE_NEW_WIDTH = 110
PADDLE_NEW_HEIGHT = 22
BRICK_NEW_WIDTH = 80
BRICK_NEW_HEIGHT = 25
# 顏色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# 球設定
BALL_RADIUS = 10

# --- 類別 ---
class Paddle(pygame.sprite.Sprite):
    """ 代表玩家控制的球拍 """
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PADDLE_NEW_WIDTH, PADDLE_NEW_HEIGHT])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - self.rect.width) // 2
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 10

class Ball(pygame.sprite.Sprite):
    """ 代表遊戲中的球 """
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([BALL_RADIUS * 2, BALL_RADIUS * 2])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.circle(self.image, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.reset()
    
    def reset(self):
        """ 重置球的位置和速度 """
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed_x = random.choice([-4, 4])
        self.speed_y = -4

# --- 遊戲主迴圈 ---
def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Breakout")
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # --- 繪圖 ---
        screen.fill(BLACK)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    game_loop()
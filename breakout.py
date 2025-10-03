import pygame
import random
import os

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

# --- 圖片資源路徑 ---
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')

# --- 輔助函式 ---
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# --- 類別 ---
class Paddle(pygame.sprite.Sprite):
    """ 代表玩家控制的球拍 """
    def __init__(self):
        super().__init__()
        # 載入球拍圖片
        paddle_img = pygame.image.load(os.path.join(ASSETS_DIR, 'paddle_2.png'))
        # 從精靈圖中提取單一幀（取中間部分作為球拍）
        self.image = pygame.Surface([PADDLE_NEW_WIDTH, PADDLE_NEW_HEIGHT], pygame.SRCALPHA)
        # 縮放圖片以適應球拍尺寸
        scaled_img = pygame.transform.scale(paddle_img, (PADDLE_NEW_WIDTH, PADDLE_NEW_HEIGHT))
        self.image.blit(scaled_img, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - self.rect.width) // 2
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 10
    
    def move(self, keys):
        """ 根據按鍵移動球拍 """
        if keys[pygame.K_LEFT]:
            self.rect.x -= 7
        if keys[pygame.K_RIGHT]:
            self.rect.x += 7
        # 防止球拍移出視窗
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width

class Ball(pygame.sprite.Sprite):
    """ 代表遊戲中的球 """
    def __init__(self):
        super().__init__()
        # 載入球圖片
        ball_img = pygame.image.load(os.path.join(ASSETS_DIR, 'ball_blue.png'))
        # 縮放球圖片至適當大小
        self.image = pygame.transform.scale(ball_img, (BALL_RADIUS * 2, BALL_RADIUS * 2))
        self.rect = self.image.get_rect()
        self.reset()
    
    def reset(self):
        """ 重置球的位置和速度 """
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed_x = random.choice([-4, 4])
        self.speed_y = -4
    
    def update(self):
        """ 移動球並處理邊界碰撞 """
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0:
            self.speed_y = -self.speed_y

class Brick(pygame.sprite.Sprite):
    """ 代表一個可以被打掉的磚塊 """
    def __init__(self, x, y, color, points):
        super().__init__()
        self.color = color
        self.points = points
        self.health = 2
        
        # 載入磚塊圖片（從精靈圖中提取第一幀）
        brick_img_path = os.path.join(ASSETS_DIR, f'brick_{color}.png')
        brick_cracked_img_path = os.path.join(ASSETS_DIR, f'brick_{color}_cracked.png')
        
        # 載入完整圖片
        full_brick_img = pygame.image.load(brick_img_path)
        full_brick_cracked_img = pygame.image.load(brick_cracked_img_path)
        
        # 精靈圖尺寸為 384x128，包含 3 幀，每幀 128x128
        frame_width = 128
        frame_height = 128
        
        # 提取第一幀作為完整磚塊
        brick_frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        brick_frame.blit(full_brick_img, (0, 0), (0, 0, frame_width, frame_height))
        
        # 提取第一幀作為破損磚塊
        brick_cracked_frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        brick_cracked_frame.blit(full_brick_cracked_img, (0, 0), (0, 0, frame_width, frame_height))
        
        # 縮放至遊戲中的磚塊尺寸
        self.normal_image = pygame.transform.scale(brick_frame, (BRICK_NEW_WIDTH, BRICK_NEW_HEIGHT))
        self.cracked_image = pygame.transform.scale(brick_cracked_frame, (BRICK_NEW_WIDTH, BRICK_NEW_HEIGHT))
        
        # 設定初始圖片為完整磚塊
        self.image = self.normal_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def get_color(self):
        colors = {
            'red': (255, 0, 0),
            'orange': (255, 165, 0),
            'yellow': (255, 255, 0),
            'green': (0, 255, 0),
            'cyan': (0, 255, 255),
            'blue': (0, 0, 255),
            'purple': (128, 0, 128)
        }
        return colors.get(self.color, WHITE)
    
    def hit(self):
        """ 處理磚塊被擊中的邏輯，並在銷毀時回傳分數 """
        self.health -= 1
        if self.health <= 0:
            self.kill()
            return self.points
        else:
            # 切換到破損磚塊圖片
            self.image = self.cracked_image
            return 0

# --- 遊戲主迴圈 ---
def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Breakout")
    clock = pygame.time.Clock()
    game_state = "start"
    score = 0
    all_sprites = pygame.sprite.Group()
    bricks = pygame.sprite.Group()
    paddle = Paddle()
    ball = Ball()
    
    def create_brick_wall():
        """ 建立磚塊牆並回傳 bricks sprite group """
        bricks.empty()
        all_sprites.empty()
        all_sprites.add(paddle)
        all_sprites.add(ball)
        BRICK_COLORS = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple']
        for row, color in enumerate(BRICK_COLORS):
            points = (row + 1) * 10
            for column in range(SCREEN_WIDTH // (BRICK_NEW_WIDTH + 5)):
                brick = Brick(
                    column * (BRICK_NEW_WIDTH + 5) + 10,
                    row * (BRICK_NEW_HEIGHT + 5) + 50,
                    color, points
                )
                all_sprites.add(brick)
                bricks.add(brick)
    
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_state == "start":
                    game_state = "playing"
                    score = 0
                    paddle.rect.x = (SCREEN_WIDTH - paddle.rect.width) // 2
                    ball.reset()
                    create_brick_wall()
                elif game_state == "game_over":
                    game_state = "start"
        
        if game_state == "start":
            screen.fill(BLACK)
            draw_text(screen, "BREAKOUT", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
            draw_text(screen, "Press any key to start", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            pygame.display.flip()
        elif game_state == "playing":
            # --- 處理輸入 ---
            keys = pygame.key.get_pressed()
            paddle.move(keys)
            # --- 遊戲邏輯更新 ---
            all_sprites.update()
            # --- 碰撞偵測 ---
            if pygame.sprite.collide_rect(ball, paddle):
                ball.speed_y = -ball.speed_y
            brick_hit_list = pygame.sprite.spritecollide(ball, bricks, False)
            if brick_hit_list:
                ball.speed_y = -ball.speed_y
                for brick in brick_hit_list:
                    score += brick.hit()
            # --- 遊戲結束條件 ---
            if ball.rect.top > SCREEN_HEIGHT:
                game_state = "game_over"
            if not bricks:
                game_state = "game_over"
            # --- 繪圖 ---
            screen.fill(BLACK)
            all_sprites.draw(screen)
            draw_text(screen, f"Score: {score}", 24, SCREEN_WIDTH / 2, 10)
            pygame.display.flip()
        elif game_state == "game_over":
            screen.fill(BLACK)
            draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
            draw_text(screen, f"Final Score: {score}", 30, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            draw_text(screen, "Press any key to restart", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
            pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    game_loop()
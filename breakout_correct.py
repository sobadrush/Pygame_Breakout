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

# --- 輔助函式 ---
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# --- 類別 ---

class PowerUp(pygame.sprite.Sprite):
    """ 代表一個會掉落的道具 """
    def __init__(self, center_x, center_y):
        super().__init__()
        self.image = pygame.image.load("assets/powerup_expand.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (BRICK_NEW_WIDTH, BRICK_NEW_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.centerx = center_x
        self.rect.centery = center_y
        self.speed_y = 3

    def update(self):
        """ 移動道具並處理邊界 (掉出畫面就刪除) """
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.kill() # 道具掉出畫面，自我銷毀


class Paddle(pygame.sprite.Sprite):
    """ 代表玩家控制的球拍 """
    def __init__(self):
        super().__init__()
        # 載入並縮放 paddle 動畫影格
        self.animation_frames = [
            pygame.transform.scale(pygame.image.load("assets/paddle_1.png").convert_alpha(), (PADDLE_NEW_WIDTH, PADDLE_NEW_HEIGHT)),
            pygame.transform.scale(pygame.image.load("assets/paddle_2.png").convert_alpha(), (PADDLE_NEW_WIDTH, PADDLE_NEW_HEIGHT)),
            pygame.transform.scale(pygame.image.load("assets/paddle_3.png").convert_alpha(), (PADDLE_NEW_WIDTH, PADDLE_NEW_HEIGHT))
        ]
        self.current_frame = 0
        self.image = self.animation_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - self.rect.width) // 2
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 10
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100 # 動畫更新頻率 (毫秒)

    def update(self):
        """ 更新 paddle 的動畫 """
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.current_frame]

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

    def widen(self):
        """ 讓球拍變寬 """
        # 取得目前中心點
        center = self.rect.centerx
        # 縮放所有動畫影格
        new_width = int(PADDLE_NEW_WIDTH * 1.5)
        self.animation_frames = [
            pygame.transform.scale(frame, (new_width, PADDLE_NEW_HEIGHT))
            for frame in self.animation_frames
        ]
        self.image = self.animation_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.centerx = center
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 10

class Ball(pygame.sprite.Sprite):
    """ 代表遊戲中的球 """
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/ball_blue.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (BALL_RADIUS * 2, BALL_RADIUS * 2))
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
        self.all_sprites_group = None
        self.powerups_group = None

        self.color = color
        self.points = points
        self.image_normal = pygame.transform.scale(pygame.image.load(f"assets/brick_{self.color}.png").convert_alpha(), (BRICK_NEW_WIDTH, BRICK_NEW_HEIGHT))
        self.image_cracked = pygame.transform.scale(pygame.image.load(f"assets/brick_{self.color}_cracked.png").convert_alpha(), (BRICK_NEW_WIDTH, BRICK_NEW_HEIGHT))
        self.image = self.image_normal
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 2

    def hit(self):
        """ 處理磚塊被擊中的邏輯，並在銷毀時回傳分數 """
        self.health -= 1
        if self.health <= 0:
            # 在銷毀前建立道具
            if self.all_sprites_group is not None and self.powerups_group is not None:
                if random.randint(1, 2) == 1:  # 50% 機率
                    new_powerup = PowerUp(self.rect.centerx, self.rect.centery)
                    self.all_sprites_group.add(new_powerup)
                    self.powerups_group.add(new_powerup)
            self.kill()
            return self.points
        else:
            self.image = self.image_cracked
            return 0

# --- 遊戲主迴圈 ---
def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Breakout")
    clock = pygame.time.Clock()

    game_state = "start"
    score = 0
    
    # 將遊戲物件的創建放在迴圈外，以便在需要時重新創建
    all_sprites = pygame.sprite.Group()
    bricks = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    paddle = Paddle()
    ball = Ball()

    def create_brick_wall():
        """ 建立磚塊牆並回傳 bricks sprite group """
        bricks.empty()
        all_sprites.empty()
        powerups.empty()
        all_sprites.add(paddle)
        all_sprites.add(ball)
        BRICK_COLORS = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple']
        for row, color in enumerate(BRICK_COLORS):
            points = (row + 1) * 10
            for column in range(SCREEN_WIDTH // (BRICK_NEW_WIDTH + 5)):
                brick = Brick(
                    column * (BRICK_NEW_WIDTH + 5) + 10, 
                    row * (BRICK_NEW_HEIGHT + 5) + 50,
                    color,
                    points
                )
                brick.all_sprites_group = all_sprites
                brick.powerups_group = powerups
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
            
            powerup_hit_list = pygame.sprite.spritecollide(paddle, powerups, True) # True = 撞到就刪除
            for powerup in powerup_hit_list:
                # 觸發球拍變寬
                paddle.widen()
            
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

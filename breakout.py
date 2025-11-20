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


def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# 定義球拍類別


class Paddle(pygame.sprite.Sprite):
    def __init__(self):  # 建構子
        super().__init__()

        self.animation_frames = [
            pygame.transform.scale(pygame.image.load(
                "assets/paddle_1.png").convert_alpha(), (PADDLE_NEW_WIDTH, PADDLE_NEW_HEIGHT)),
            pygame.transform.scale(pygame.image.load(
                "assets/paddle_2.png").convert_alpha(), (PADDLE_NEW_WIDTH, PADDLE_NEW_HEIGHT)),
            pygame.transform.scale(pygame.image.load(
                "assets/paddle_3.png").convert_alpha(), (PADDLE_NEW_WIDTH, PADDLE_NEW_HEIGHT))
        ]
        # self.image = pygame.Surface([PADDLE_NEW_WIDTH, PADDLE_NEW_HEIGHT])
        # self.image.fill(WHITE)
        self.current_frame = 0
        self.image = self.animation_frames[self.current_frame]

        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - self.rect.width) // 2
        self.rect.y = SCREEN_HEIGHT - 10 - self.rect.height

        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100

    def update(self):
        now = pygame.time.get_ticks()
        if now-self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame +
                                  1) % len(self.animation_frames)
            self.image = self.animation_frames[self.current_frame]

    def move(self, keys):
        # 平板移動
        if keys[pygame.K_LEFT]:
            self.rect.x -= 7
        if keys[pygame.K_RIGHT]:
            self.rect.x += 7
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0

# 定義球類別


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/ball_blue.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (BALL_RADIUS*2, BALL_RADIUS*2))
        self.rect = self.image.get_rect()
        self.reset()  # 歸位的方法

    def reset(self):
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed_x = random.choice([-4, 4])
        self.speed_y = -4

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.right >= SCREEN_WIDTH or \
                self.rect.left <= 0:
            self.speed_x = -self.speed_x

        if self.rect.top <= 0:
            self.speed_y = -self.speed_y


class Brick(pygame.sprite.Sprite):
    """ 代表一個可以被打掉的磚塊 """

    def __init__(self, x, y, color, points):
        super().__init__()
        self.color = color
        self.points = points
        self.image_normal = pygame.transform.scale(pygame.image.load(
            f"assets/brick_{self.color}.png").convert_alpha(), (BRICK_NEW_WIDTH, BRICK_NEW_HEIGHT))
        self.image_cracked = pygame.transform.scale(pygame.image.load(
            f"assets/brick_{self.color}_cracked.png").convert_alpha(), (BRICK_NEW_WIDTH, BRICK_NEW_HEIGHT))
        self.image = self.image_normal
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 2
        self.all_sprites_group = None
        self.powerups_group = None

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            new_powerup = PowerUp(self.rect.centerx, self.rect.centery)
            self.all_sprites_group.add(new_powerup)
            self.powerups_group.add(new_powerup)
            self.kill()
            return self.points
        else:
            self.image = self.image_cracked
            return 0


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = center_x
        self.rect.centery = center_y
        self.speed_y = 3

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Breakout")
    clock = pygame.time.Clock()

    score = 0
    game_state = "start"

    all_sprites = pygame.sprite.Group()  # 建立 Sprite 群組
    bricks = pygame.sprite.Group()  # 建立 brick 群組
    powerups = pygame.sprite.Group()

    paddle = Paddle()
    ball = Ball()

    def create_brick_wall():
        bricks.empty()
        all_sprites.empty()
        all_sprites.add(paddle)
        all_sprites.add(ball)
        powerups.empty() # 清空道具群組

        # 建立磚塊牆
        BRICK_COLORS = ["red", "orange", "yellow",
                        "green", "cyan", "blue", "purple"]
        for row, color in enumerate(BRICK_COLORS):
            points = (7 - row) * 10
            for column in range(SCREEN_WIDTH // (BRICK_NEW_WIDTH + 5)):
                brick = Brick(
                    column * (BRICK_NEW_WIDTH + 5) + 10,
                    row * (BRICK_NEW_HEIGHT + 5) + 50,
                    color,
                    points
                )
                all_sprites.add(brick) # 將磚塊加入 all_sprites 群組
                bricks.add(brick) # 將磚塊加入 bricks 群組

                # 把 groups 傳給 brick 物件
                brick.all_sprites_group = all_sprites
                brick.powerups_group = powerups

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
                    paddle.rect.x = (SCREEN_WIDTH-paddle.rect.width)//2
                    ball.reset()
                    create_brick_wall()

                elif game_state == "game_over":
                    game_state = "start"
        # --- 處理輸入 ---

        if game_state == "start":
            screen.fill(BLACK)
            draw_text(screen, "BREAKOUT", 64, SCREEN_WIDTH/2, SCREEN_HEIGHT/4)
            draw_text(screen, "Press any key to restart",
                      22, SCREEN_WIDTH/2, SCREEN_HEIGHT*3/4)
            pygame.display.flip()

        elif game_state == "playing":
            keys = pygame.key.get_pressed()
            paddle.move(keys)

            all_sprites.update()

            # --- 碰撞偵測 ---
            if pygame.sprite.collide_rect(ball, paddle):
                ball.speed_y = -ball.speed_y

            if ball.rect.top > SCREEN_HEIGHT:
                ball.reset

            # 球與磚塊碰撞
            # spritecollide 的參數說明：
            # 第一個參數：要檢測碰撞的 sprite
            # 第二個參數：要檢測碰撞的 group
            # 第三個參數：是否要刪除碰撞到的 sprite
            brick_hit_list = pygame.sprite.spritecollide(ball, bricks, False)
            if brick_hit_list:
                ball.speed_y = -ball.speed_y
                for brick in brick_hit_list:
                    score += brick.hit()  # 呼叫磚塊的 hit 方法

            # --- 遊戲結束條件 ---
            if ball.rect.top > SCREEN_HEIGHT:
                # ball.reset() # 先重置球位置
                game_state = "game_over"

            if not bricks:
                # running=False
                game_state = "game_over"

            # --- 繪圖 ---
            screen.fill(BLACK)
            all_sprites.draw(screen)  # 透過 group 畫出來
            draw_text(screen, f"Score:{score}", 24, SCREEN_WIDTH/2, 10)
            pygame.display.flip()

        elif game_state == "game_over":
            screen.fill(BLACK)
            draw_text(screen,
                      "GAME OVER", 64, SCREEN_WIDTH/2, SCREEN_HEIGHT/4)
            draw_text(screen, f"Final Score:{score}",
                      30, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
            draw_text(screen, "Press any key to restart",
                      22, SCREEN_WIDTH/2, SCREEN_HEIGHT*3/4)
            pygame.display.flip()

    pygame.quit()


# 主程式
if __name__ == "__main__":
    game_loop()

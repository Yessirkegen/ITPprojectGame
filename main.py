import pygame
import sys
import os
import random

# Инициализация Pygame
pygame.init()

# Размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BACKGROUND_COLOR = (135, 206, 250)  # Голубой цвет для заднего фона


# Класс для героя
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Состояния анимации
        self.idle_images = self.load_images('run', 1, 0.1)
        self.run_images = self.load_images('run', 2, 0.1)
        self.jump_images = self.load_images('jump', 1, 0.1)
        self.fall_images = self.load_images('jump', 1, 0.1)

        self.current_state = 'idle'
        self.images = self.idle_images
        self.index = 0  # Текущий индекс кадра
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5
        self.y_speed = 0
        self.gravity = 0.5
        self.on_ground = False

    def load_images(self, prefix, num_images, scale):
        images = []
        for i in range(1, num_images + 1):
            image_path = os.path.join('images', f'{prefix}_{i}.jpg')
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
            images.append(image)
        return images

    def update(self, keys, platforms):
        self.y_speed += self.gravity

        # Применение гравитации
        self.rect.y += self.y_speed

        # Проверка столкновения с платформой
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for platform in hits:
            if self.y_speed > 0:
                self.rect.bottom = platform.rect.top
                self.on_ground = True
                self.y_speed = 0
            elif self.y_speed < 0:
                self.rect.top = platform.rect.bottom
                self.y_speed = 0

        # Обработка прыжка
        if keys[pygame.K_UP] and self.on_ground:
            self.y_speed = -12  # Начальная скорость прыжка
            self.on_ground = False
            self.current_state = 'jump'

        # Управление по горизонтали
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.current_state = 'run'
        elif keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
            self.current_state = 'run'
        else:
            self.current_state = 'idle'

        # Обновление анимации
        self.animate()

    def animate(self):
        # Переключение между кадрами для создания анимации
        self.index += 1

        if self.current_state == 'idle':
            self.images = self.idle_images
        elif self.current_state == 'run':
            self.images = self.run_images
        elif self.current_state == 'jump':
            self.images = self.jump_images
        elif self.current_state == 'fall':
            self.images = self.fall_images

        if self.index >= len(self.images):
            self.index = 0
            if self.current_state == 'jump':
                self.current_state = 'fall'
                self.images = self.fall_images

        self.image = self.images[self.index]


# Класс для счета
class Score:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.score = 0

    def render(self, surface):
        rendered_score = self.font.render(f"Score: {self.score}", True, WHITE)
        surface.blit(rendered_score, (10, 10))


# Класс для собираемых предметов
class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100, SCREEN_WIDTH - 20)
        self.rect.y = random.randint(100, SCREEN_HEIGHT - 20)

    def update(self):
        pass


# Класс для врагов
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(100, SCREEN_HEIGHT - 20)
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.x = SCREEN_WIDTH
            self.rect.y = random.randint(100, SCREEN_HEIGHT - 20)


# Класс для платформ
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()


# Создание группы спрайтов
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
items = pygame.sprite.Group()
enemies = pygame.sprite.Group()
score = Score()

# Создание героя
player = Player()
all_sprites.add(player)

# Создание платформ
platform_width = 200
platform_height = 20
platform1 = Platform(platform_width, platform_height)
platform1.rect.x = SCREEN_WIDTH // 2 - platform_width // 2
platform1.rect.y = SCREEN_HEIGHT - 100

platform2 = Platform(platform_width, platform_height)
platform2.rect.x = 100
platform2.rect.y = SCREEN_HEIGHT - 200

platform3 = Platform(platform_width,platform_height)
platform3.rect.x=450
platform3.rect.y = 300

all_sprites.add(platform1, platform2,platform3)
platforms.add(platform1, platform2,platform3)

# Создание собираемых предметов
for _ in range(5):  # Создаем пять предметов
    item = Item()
    all_sprites.add(item)
    items.add(item)

# Создание врагов
for _ in range(5):  # Создаем пять врагов
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Player Animation States")

# Основной цикл игры
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Получение текущего состояния клавиш
    keys = pygame.key.get_pressed()

    # Обновление героя
    player.update(keys, platforms)

    # Обновление собираемых предметов
    items.update()

    # Обновление врагов
    enemies.update()

    # Проверка столкновений героя с собираемыми предметами
    collected_items = pygame.sprite.spritecollide(player, items, True)
    for item in collected_items:
        score.score += 10

    # Проверка столкновений героя с врагами
    if pygame.sprite.spritecollide(player, enemies, False):
        print("Game Over! You collided with an enemy.")
        pygame.quit()
        sys.exit()

    # Очистка экрана
    screen.fill(BACKGROUND_COLOR)

    # Отрисовка всех спрайтов
    all_sprites.draw(screen)

    # Обновление и отрисовка счета
    score.render(screen)

    # Обновление экрана
    pygame.display.flip()

    # Установка FPS
    clock.tick(30)

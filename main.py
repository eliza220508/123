import random
import pygame
import sys
import os

pygame.init()
size1 = width1, height1 = 700, 500
size = width, height = 520, 520
screen = pygame.display.set_mode(size1)
clock = pygame.time.Clock()
FPS = 50

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player1_group = pygame.sprite.Group()
player2_group = pygame.sprite.Group()
evil_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
wins_group = pygame.sprite.Group()  # Создаем группу для изображений победы


class Win(pygame.sprite.Sprite):
    def __init__(self, image, win):
        super().__init__(wins_group, all_sprites)  # Добавляем в wins_group
        if win == 1:
            self.image = win1
        else:
            self.image = win2
        self.image = pygame.transform.scale(self.image, (520, 520))
        self.rect = self.image.get_rect()



class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, abs(y2 - y1)])  # abs для избежания отрицательной длины
            self.rect = pygame.Rect(x1, y1, 1, abs(y2 - y1))
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([abs(x2 - x1), 1])  # abs для избежания отрицательной длины
            self.rect = pygame.Rect(x1, y1, abs(x2 - x1), 1)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.tile_type = tile_type
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, type_tank):
        super().__init__(bullet_group, all_sprites)
        if type_tank == 1:
            self.image = bullet_image
        else:
            self.image = bullet_image2
        self.image = pygame.transform.scale(self.image, (8, 8))
        self.rect = self.image.get_rect()
        self.rect.x = -105
        self.rect.y = -105
        self.side = None

    def move_bullet(self, napr, pos_x, pos_y):
        print(napr)
        if self.side == None:
            self.side = napr
            if self.side == 'up':
                self.rect = self.image.get_rect().move(pos_x + 13, pos_y - 10)
            if self.side == 'down':
                self.rect = self.image.get_rect().move(pos_x + 13, pos_y + 10)
            if self.side == 'left':
                self.rect = self.image.get_rect().move(pos_x - 13, pos_y + 10)
            if self.side == 'right':
                self.rect = self.image.get_rect().move(pos_x + 13, pos_y + 10)
    def check_win(self):
        if pygame.sprite.spritecollideany(self, tiles_group):
            n = pygame.sprite.spritecollide(self, tiles_group, False)
            if n[0].tile_type == 'stab1':
                win = 2
                return win
            if n[0].tile_type == 'stab2':
                win = 1
                return win
            if n[0].tile_type != 'wall':
                n[0].kill()
                self.side = None
                self.rect.x = -105
                self.rect.y = -105
            ## проверка на тип ячейки
            elif n[0].tile_type == 'wall':
                self.side = None
                self.rect.x = -105
                self.rect.y = -105
    def check_tank(self, tank):
        if pygame.sprite.spritecollideany(self, player1_group) or pygame.sprite.spritecollideany(self, player2_group):
            tank.rect.x = tank.x_start
            tank.rect.y = tank.y_start



    def update(self):
        if self.side == 'up':
            self.rect.y -= 5
        elif self.side == 'down':
            self.rect.y += 5
        elif self.side == 'left':
            self.rect.x -= 5
        elif self.side == 'right':
            self.rect.x += 5
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.side = None
            self.rect.x = -105
            self.rect.y = -105
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.side = None
            self.rect.x = -105
            self.rect.y = -105






class Player_2(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player2_group, all_sprites)

        self.image = player2_image
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.side = 'down'
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 3, tile_height * pos_y)
        self.x_start, self.y_start = tile_width * pos_x + 3, tile_height * pos_y

    def move_player(self, keys, tiles_group):  # двигается по (-1, 0)

        if keys[pygame.K_a]:
            if self.rect.x >= 5:
                if self.side == 'up':
                    self.image = pygame.transform.rotate(self.image, 90)
                    self.side = 'left'
                if self.side == 'right':
                    self.image = pygame.transform.rotate(self.image, 180)
                    self.side = 'left'
                if self.side == 'down':
                    self.image = pygame.transform.rotate(self.image, 270)
                    self.side = 'left'
                self.rect.x -= 3
                if pygame.sprite.spritecollideany(self, tiles_group):
                    self.rect.x += 4
        elif keys[pygame.K_d]:
            if self.rect.x <= 485:
                if self.side == 'up':
                    self.image = pygame.transform.rotate(self.image, 270)
                    self.side = 'right'
                if self.side == 'left':
                    self.image = pygame.transform.rotate(self.image, 180)
                    self.side = 'right'
                if self.side == 'down':
                    self.image = pygame.transform.rotate(self.image, 90)
                    self.side = 'right'
                self.rect.x += 3
                if pygame.sprite.spritecollideany(self, tiles_group):
                    self.rect.x -= 4
        elif keys[pygame.K_w]:
            if self.rect.y >= 5:
                if self.side == 'right':
                    self.image = pygame.transform.rotate(self.image, 90)
                    self.side = 'up'
                if self.side == 'left':
                    self.image = pygame.transform.rotate(self.image, 270)
                    self.side = 'up'
                if self.side == 'down':
                    self.image = pygame.transform.rotate(self.image, 180)
                    self.side = 'up'
                self.rect.y -= 3
                if pygame.sprite.spritecollideany(self, tiles_group):
                    self.rect.y += 4
        elif keys[pygame.K_s]:
            if self.rect.y <= 485:
                if self.side == 'left':
                    self.image = pygame.transform.rotate(self.image, 90)
                    self.side = 'down'
                if self.side == 'right':
                    self.image = pygame.transform.rotate(self.image, 270)
                    self.side = 'down'
                if self.side == 'up':
                    self.image = pygame.transform.rotate(self.image, 180)
                    self.side = 'down'
                self.rect.y += 3
                if pygame.sprite.spritecollideany(self, tiles_group):
                    self.rect.y -= 4


class Player_1(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player1_group, all_sprites)

        self.image = player_image
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.side = 'up'
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 3, tile_height * pos_y)
        self.x_start, self.y_start = tile_width * pos_x + 3, tile_height * pos_y
    def move_player(self, keys, tiles_group):  # двигается по (-1, 0)

        if keys[pygame.K_LEFT]:
            # keys[pygame.K_a]):
            if self.rect.x >= 5:
                if self.side == 'up':
                    self.image = pygame.transform.rotate(self.image, 90)
                    self.side = 'left'
                if self.side == 'right':
                    self.image = pygame.transform.rotate(self.image, 180)
                    self.side = 'left'
                if self.side == 'down':
                    self.image = pygame.transform.rotate(self.image, 270)
                    self.side = 'left'
                self.rect.x -= 3
                if pygame.sprite.spritecollideany(self, tiles_group):
                    self.rect.x += 4
        elif keys[pygame.K_RIGHT]:
            # keys[pygame.K_d]):
            if self.rect.x <= 485:
                if self.side == 'up':
                    self.image = pygame.transform.rotate(self.image, 270)
                    self.side = 'right'
                if self.side == 'left':
                    self.image = pygame.transform.rotate(self.image, 180)
                    self.side = 'right'
                if self.side == 'down':
                    self.image = pygame.transform.rotate(self.image, 90)
                    self.side = 'right'
                self.rect.x += 3
                if pygame.sprite.spritecollideany(self, tiles_group):
                    self.rect.x -= 4
        elif keys[pygame.K_UP]:
            # keys[pygame.K_w]):
            if self.rect.y >= 5:
                if self.side == 'right':
                    self.image = pygame.transform.rotate(self.image, 90)
                    self.side = 'up'
                if self.side == 'left':
                    self.image = pygame.transform.rotate(self.image, 270)
                    self.side = 'up'
                if self.side == 'down':
                    self.image = pygame.transform.rotate(self.image, 180)
                    self.side = 'up'
                self.rect.y -= 3
                if pygame.sprite.spritecollideany(self, tiles_group):
                    self.rect.y += 4
        elif keys[pygame.K_DOWN]:
            if self.rect.y <= 485:
                if self.side == 'left':
                    self.image = pygame.transform.rotate(self.image, 90)
                    self.side = 'down'
                if self.side == 'right':
                    self.image = pygame.transform.rotate(self.image, 270)
                    self.side = 'down'
                if self.side == 'up':
                    self.image = pygame.transform.rotate(self.image, 180)
                    self.side = 'down'
                self.rect.y += 3
                if pygame.sprite.spritecollideany(self, tiles_group):
                    self.rect.y -= 4


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=- 1):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_images = {
    'wall': load_image('бетонка.jpg'),
    'bеt': load_image('кирпич.jpg'),
    # 'black': load_image('black.jpg'),
    'stab1': load_image('stab.jpg'),
    'stab2': load_image('stab.jpg')

}
player_image = load_image('танчик.jpeg')
player2_image = load_image('танчик — копия.jpeg')
bullet_image = load_image('Twemoji_1f534.svg.png')
bullet_image2 = load_image('254654.svg.png')
win1 = load_image('win_gold.png')
win2 = load_image('win_silver.png')

Border(0, 0, width, 0)
Border(0, height, width, height)
Border(0, 0, 0, height)
Border(width, 0, width, height)


def generate_level(level):
    new_player2, new_player1, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pass
                # Tile('black', x, y)
            elif level[y][x] == '+':
                Tile('wall', x, y)
            elif level[y][x] == '*':
                print('dfghjhgfdghjkjhgvcxcfghj')
                # Evil_Tanks(x, y)
                new_player2 = Player_2(x, y)
            elif level[y][x] == '@':
                # Tile('black', x, y)
                new_player1 = Player_1(x, y)
            elif level[y][x] == '#':
                Tile('bеt', x, y)
            elif level[y][x] == '$':
                Tile('stab1', x, y)
            elif level[y][x] == '%':
                Tile('stab2', x, y)

    # вернем игрока, а также размер поля в клетках
    return new_player2, new_player1, x, y


#
#
tile_width = 40
tile_height = 40
player2, player1, level_x, level_y = generate_level(load_level(random.choice(['map.txt', 'map2.txt'])))
print(player2)
bullet1 = Bullet(player1.rect.x, player1.rect.y, 1)
bullet2 = Bullet(player2.rect.x, player2.rect.y, 2)

# win_gold_image = load_image('win_gold.png')  # Загружаем изображение
# win_silver_image = load_image('win_silver.png')  # Загружаем изображение
# win_gold = Win(win_gold_image, 0, 0)  # Создаем спрайт win_gold
# win_silver = Win(win_silver_image, 0, 0)  # Создаем спрайт win_silver
# win_silver.kill()
# win_gold.kill()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ['ЧТОБЫ НАЧАТЬ',
                  'НАЖМИТЕ ПРОБЕЛ']
    fon = pygame.transform.scale(load_image('lklk.png'), (600, 146))
    screen.blit(fon, (50, 50))
    font = pygame.font.SysFont('Arial', 60, bold=True)
    text_coord = 220  # координата по у
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(255, 255, 255))  # формируем текст и цвет текста
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        if line == intro_text[0]:

            intro_rect.x = 135
        else:
            intro_rect.x = 110
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)  # расположить его на такой высоте
    level = 0
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    if level == 0:
                        # player, level_x, level_y = generate_level(load_level('map2.txt'))
                        level = 1
                        screen1 = pygame.display.set_mode((520, 520))
                        screen2 = pygame.display.set_mode((520, 520))
                        continue
                    else:
                        bullet1.move_bullet(player1.side, player1.rect.x, player1.rect.y)
                if event.key == pygame.K_RETURN:
                    bullet2.move_bullet(player2.side, player2.rect.x, player2.rect.y)

        keys = pygame.key.get_pressed()
        player1.move_player(keys, tiles_group)
        player2.move_player(keys, tiles_group)
        bullet1.check_tank(player2)
        bullet2.check_tank(player1)
        if level == 1:
            screen.fill('black')
            tiles_group.draw(screen1)
            player1_group.draw(screen1)
            player2_group.draw(screen1)
            evil_group.draw(screen1)
            bullet_group.draw(screen1)
        if level == 2:
            tiles_group.draw(screen1)
            player1_group.draw(screen1)
            player2_group.draw(screen1)
            level += 1
        if level == 3:
            wins_group.draw(screen2)


        evil_group.update()
        bullet_group.update()
        res = bullet1.check_win()
        if res:
            win = Win(win1, res)
            level = 3
        res = bullet2.check_win()
        if res:
            win = Win(win1, res)
            level = 3
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    start_screen()

from asyncio.windows_events import NULL
import random
import pygame
import pygame.freetype

pygame.init()
clock = pygame.time.Clock()
# -*- coding: utf-8 -*-


# Создает и заполняет матрицу случайными числа от 1 до 4
def create_board(width, height):
    return [[random.randrange(1, 5) for x in range(width)] for y in range(height)]

# Проверяет, есть ли в матрице 3-в-ряд
def match_exist(board):
    for y in range(len(board)):
        streak = 0
        for x in range(1, len(board[y])):
            if board[y][x] == board[y][x - 1]:
                streak += 1
            else:
                streak = 0
            if streak >= 2:
                return True
        
    for x in range(len(board)):
        streak = 0
        for y in range(1, len(board[y])):
            if board[y][x] == board[y - 1][x]:
                streak += 1
            else:
                streak = 0
            if streak >= 2:
                return True
    return False

# Форматирует матрицу так, что бы там больше не было 3-в-ряд
def format_board(board):
    while match_exist(board):
        for y in range(len(board)):
            for x in range(len(board[0])):
                board[y][x] = random.randrange(1, 5)
    return board

# Рисует фигуры по матрице
def draw_board(board):
    for x in range(10):
        for y in range(10):
            if (x + y) % 2 == 0:
                pygame.draw.rect(display, CHECKER, (25 + x*50, 25 + y*50, 50, 50))
            else:
                pygame.draw.rect(display, BACKGROUND, (25 + x*50, 25 + y*50, 50, 50))
    for y in range(10):
        for x in range(10):
            if board[y][x] == 1:
                pygame.draw.rect(display, RED, (32 + x*50, 32 + y*50, 36, 36))
            elif board[y][x] == 2:
                pygame.draw.circle(display, YELLOW, (50 + x*50, 50 + y*50), 18)
            elif board[y][x] == 3:
                pygame.draw.rect(display, GREEN, (32 + x*50, 32 + y*50, 36, 36))
            elif board[y][x] == 4:
                pygame.draw.circle(display, BLUE, (50 + x*50, 50 + y*50), 18)

# Получаем элемент через координаты нажатия мышки
def get_element(cords):
    x, y = -1, -1
    if  0 < cords[0] - 25 < 500:
        x = (cords[0] - 25) // 50
    if 0 < cords[1] - 25 < 500:
        y = (cords[1] - 25) // 50

    if x != -1 and y != -1:
        return (x, y)

# Меняет местами элементы в массиве
def swap(board, elem1, elem2):
    if (not -1 in elem1) and (not -1 in elem2) and (-1 <= elem1[1] - elem2[1] <= 1) and (-1 <= elem1[0] - elem2[0] <= 1) and ((elem1[1] - elem2[1]) + (elem1[0] - elem2[0]) != 0) and (abs((elem1[1] - elem2[1]) + (elem1[0] - elem2[0])) != 2):
        board[elem1[1]][elem1[0]], board[elem2[1]][elem2[0]] = board[elem2[1]][elem2[0]], board[elem1[1]][elem1[0]]
        if not match_exist(board):
            board[elem1[1]][elem1[0]], board[elem2[1]][elem2[0]] = board[elem2[1]][elem2[0]], board[elem1[1]][elem1[0]]
    return board

# Делает цвет выбранного элемента темнее
def on_select_color(board, elem_cords):
    if elem_cords != (-1, -1):
        x = elem_cords[0]
        y = elem_cords[1]
        elem = board[y][x]
        if elem == 1:
            pygame.draw.rect(display, RED_DARK, (32 + x*50, 32 + y*50, 36, 36))
        elif elem == 2:
            pygame.draw.circle(display, YELLOW_DARK, (50 + x*50, 50 + y*50), 18)
        elif elem == 3:
            pygame.draw.rect(display, GREEN_DARK, (32 + x*50, 32 + y*50, 36, 36))
        elif elem == 4:
            pygame.draw.circle(display, BLUE_DARK, (50 + x*50, 50 + y*50), 18)

# Удаляет совпадения (3-в-ряд), а так же возвращает счет (Колличество удаленных элементов * 5)
def delete_matches(board):
    delete = []
    for y in range(len(board)):
        streak = 0
        for x in range(1, len(board[y])):
            if board[y][x] == board[y][x - 1]:
                streak += 1
            else:
                streak = 0

            if streak == 2:
                delete += [[x - 2, y]]
                delete += [[x - 1, y]]
                delete += [[x, y]]
            elif streak > 2:
                delete += [[x, y]]
                
        
    for x in range(len(board)):
        streak = 0
        for y in range(1, len(board[x])):
            if board[y][x] == board[y - 1][x]:
                streak += 1
            else:
                streak = 0
            
            if streak == 2:
                delete += [[x, y - 2]]
                delete += [[x, y - 1]]
                delete += [[x, y]]
            elif streak > 2:
                delete += [[x, y]]
                
    for i in range(len(delete)):
        board[delete[i][1]][delete[i][0]] = 0

    return (board, len(delete) * 5)

# Проверяет, есть ли в матрице пустые(0) элементы
def is_empty(board):
    for y in range(10):
        for x in range(10):
            if board[y][x] == 0:
                return True
    return False

# Заставляет элементы "упасть"
def pull_down(board):
    for x in range(10):
        for y in range(9):
            if board[y][x] != 0 and board[y + 1][x] == 0:
                board[y][x], board[y + 1][x] = board[y + 1][x], board[y][x]
    return board

# Генерирует новые элементы в первой строке матрицы
def generate_elements(board):
    for x in range(10):
        if board[0][x] == 0:
            board[0][x] = random.randrange(1, 5)
    return board

# Константы цветов
RED = (252, 40, 71)
RED_DARK = (202, 40, 71)
BLUE = (123, 104,238)
BLUE_DARK = (123, 104, 188)
GREEN = (11, 230, 81)
GREEN_DARK = (11, 180, 81)
YELLOW = (248, 243, 43)
YELLOW_DARK = (200, 200, 43)
BACKGROUND = (220, 220, 220)
CHECKER = (200, 200, 200 )
SCORE = (40, 40, 40)

# Заполняет задний фон
display = pygame.display.set_mode((550, 750))
display.fill(BACKGROUND)

# Загаловок приложения
pygame.display.set_caption("Match-3 By NBcheslam, Dospasito, Srassul and Snuskarim")

# Создает отформатированную матрицу 
board = format_board(create_board(10, 10))

# Переменные:
first_elem = (-1, -1)
second_elem = (-1, -1)
selected = False
score = 0
font = pygame.freetype.SysFont("Comic sans", 40)

# Главный цикл игры. Вся логика происходит тут
game_over = False
while not game_over:

    # event.get() проверяет все события. 
    for event in pygame.event.get():

        # Смотрим было ли событие "Выход"
        if event.type == pygame.QUIT:
            game_over = True

        # Управление: Получение положения элемента по позиции мышки. 
        elif event.type == pygame.MOUSEBUTTONDOWN and not is_empty(board):
            if not selected:
                first_elem = get_element(pygame.mouse.get_pos())
                selected = True
            else:
                second_elem = get_element(pygame.mouse.get_pos())
                selected = False

    # Защита в случае нажатия на неигровое поле
    if first_elem is None or second_elem is None:
        first_elem, second_elem = (-1, -1), (-1, -1)
        selected = False

    # Когда в двух координатах отсутствует -1 (То есть, два элемента выбрано):
    # 1. Меняет эти два элемента местами
    # 2. Удаляет совпадения (3-в-ряд)
    # 3. Обновляет счет
    # 4. Сбрасывает выбранные элементы (То есть, приравнивает их к (-1, -1))
    if (not -1 in first_elem) and (not -1 in second_elem):
        board = swap(board, first_elem, second_elem)

        temp = delete_matches(board)
        board = temp[0]
        score += temp[1]

        pygame.draw.rect(display, BACKGROUND, (130, 600, 500, 50))
        first_elem, second_elem = (-1, -1), (-1, -1)   

    # Физика элементов и заполнение пустот
    board = pull_down(board)
    board = generate_elements(board)

    # Удаление возникших совпадении
    if not is_empty(board):
        temp = delete_matches(board)
        board = temp[0]
        score += temp[1]
        pygame.draw.rect(display, BACKGROUND, (130, 600, 500, 50))

    # Отображает счет
    text, rect = font.render("Your score: " + str(score), SCORE)
    display.blit(text, (130, 600))
    
    # Рисует доску
    draw_board(board)
    on_select_color(board, second_elem)
    
    pygame.display.update()
    clock.tick(15)

    



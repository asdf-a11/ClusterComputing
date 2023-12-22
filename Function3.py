#   In the name of god  #
# Game of life
# By Pooya.Sh.K
# inspired by John conway

import pygame
import sys
import os
import random
pygame.init()

BOARDW = 60#WINW//BOXW
BOARDH = 60#WINH//BOXH

BOXW = 10
BOXH = 10

dis = pygame.display.set_mode((BOARDW * BOXW, BOARDH * BOXH))
pygame.display.set_caption("Game of Life")

WINW, WINH = dis.get_size()

fill_color = (255, 255, 255)
empty_color = (0, 0, 0)


def make_new_board(w, h):
    return list([0]*w for i in range(h))


def check(board, x, y):
    m = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not(i == j == 0) and (0 <= i+y < BOARDH) and (0 <= j+x < BOARDW):
                m += board[i+y][j+x]
    if board[y][x]:
        if m == 2 or m == 3:
            return True
    if not board[y][x]:
        if m == 3:
            return True
    return False


def update(board):
    nb = make_new_board(BOARDW, BOARDH)
    for i in range(BOARDH):
        for j in range(BOARDW):
            nb[i][j] = check(board, j, i)
    #for i in range(3):
    #    for x in range(i,BOARDW, 3):
    #        for y in range(BOARDH):
    #            nb[y][x] = check(board, x, y)
    return nb


def draw(win, board):
    for i in range(BOARDH):
        for j in range(BOARDW):
            if board[i][j]:
                pygame.draw.rect(win, fill_color, (j*BOXW, i*BOXH, BOXW, BOXH))
            else:
                pygame.draw.rect(win, empty_color,
                                 (j*BOXW, i*BOXH, BOXW, BOXH))


def recommend_name():
    n = 0
    a = os.listdir()
    l = []
    for f in a:
        if f.startswith("gol") and f.endswith(".png"):
            l.append(f)
    t = True
    while t:
        n += 1
        t = False
        if "gol"+str(n)+".png" in l:
            t = True
    return "gol"+str(n)+".png"


def load(name):
    nb = make_new_board(BOARDW, BOARDH)
    s = pygame.image.load(name)
    for i in range(BOARDH):
        for j in range(BOARDW):
            nb[i][j] = (s.get_at((j*BOXW+BOXW//2, i*BOXH+BOXH//2))
                        == fill_color)
    return nb

def InitBoard():
    for w in range(BOARDW):
        for h in range(BOARDH):
            board[w][h] = bool(random.randint(0,1))

board = make_new_board(BOARDW, BOARDH)
InitBoard()
updating = True
drag = False
down = False
dragval = False
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        '''
        elif e.type == pygame.MOUSEBUTTONUP:
            down = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                updating = not updating
            elif e.key == pygame.K_RIGHT:
                board = update(board)
            elif e.key == pygame.K_s:
                pygame.image.save(dis, recommend_name())
            elif e.key == pygame.K_l:
                board = load(input())
            elif e.key == pygame.K_d:
                drag = not drag
        '''
    if drag and down:
        x, y = pygame.mouse.get_pos()
        x, y = x//BOXW, y//BOXH
        board[y][x] = dragval
    if updating:
        board = update(board)

    draw(dis, board)
    pygame.display.update()
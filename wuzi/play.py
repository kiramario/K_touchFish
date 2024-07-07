#!/usr/bin/env python
# -*- coding: utf-8 -*-
# K_touchFish.play
# @Calendar: 2024-07-04 21:22
# @Time: 21:22
# @Author: mammon, kiramario

from enum import StrEnum
from typing import NamedTuple

board = [[' ']*15 for line in range(15)]

class Chess(StrEnum):
    # WHITE = "⚪"
    WHITE = "🟢"
    # BLACK = "⚫ 🔵🔴🟢"
    BLACK = "🔴"


class FillPoint(NamedTuple):
    x: int
    y: int
    chess: Chess

    def getXy(self):
        return (self.x, self.y)


def get_chess(x, y) -> str:
    return board[x][y]


def printboard1(board):
    """
    打印board 样式1
    :param board:
    :return:
    """
    for x in range(len(board)):
        if x == 0:
            print('\033[0;30;43m' + '-'*75 + '\033[0m')
        for y in range(len(board[x])):
            chess_color = get_chess(x, y)
            chess_color = chess_color if chess_color != ' ' else "  "
            if y == 0:
                print('\033[0;30;43m' + '| '+ chess_color + '| ' + '\033[0m',end = '')
            elif y == 14:
                print('\033[0;30;43m' + chess_color + ' |' + '\033[0m',end = '')
            else:
                print('\033[0;30;43m' + chess_color +' | '+ '\033[0m',end = '')
        print()
        print('\033[0;30;43m' + '-'*75 + '\033[0m')

def in_bound(coord) -> bool:
    """
    coordination should in board
    :param coord:
    :return:
    """
    return 0 <= coord[0] <= 14 and 0 <= coord[1] <= 14


def is_win(p: FillPoint) -> bool:
    """
    从给定点，东西，南北，西南东北，西北东南，计算和此给定点的颜色相同的点数
    :param p:
    :return:
    """
    print(f"current p: {p}")
    def count_till(pxy, fxy, gxy):
        init_xy = pxy.getXy()
        def count_till2(xy, txy, state_list):
            if in_bound(xy) and get_chess(*xy) == str(pxy.chess):
                state_list.append(xy)
                return count_till2(txy(xy), txy, state_list)
            else:
                return state_list
        return count_till2(fxy(init_xy), fxy,  []) + [init_xy] + count_till2(gxy(init_xy), gxy,  [])

    for flag in range(4):
        count = []
        if flag == 0: # ( x - 1, y ) <- (x, y) -> (x + 1, y) y = y
            count = count_till(p, lambda xy: (xy[0] - 1, xy[1]), lambda xy: (xy[0] + 1, xy[1]))
        elif flag == 1: # ( x, y - 1 ) <- (x, y) -> (x, y + 1) x = x
            count = count_till(p, lambda xy: (xy[0], xy[1] - 1), lambda xy: (xy[0], xy[1] + 1))
        elif flag == 2: # ( x - 1, y + 1 ) <- (x, y) -> (x + 1, y - 1) y = -x
            count = count_till(p, lambda xy: (xy[0] - 1, xy[1] + 1), lambda xy: (xy[0] + 1, xy[1] - 1))
        elif flag == 3: # ( x - 1, y - 1 ) <- (x, y) -> (x + 1, y + 1) y = x
            count = count_till(p, lambda xy: (xy[0] - 1, xy[1] - 1), lambda xy: (xy[0] + 1, xy[1] + 1))

        if len(count) >= 5:
            count.sort()
            print(f"5 complete: {count}")
            return True

    return False

def fall_chess(x, y, chess: Chess) -> bool:
    """
    board是一个二维数组， x其实是纵坐标，y是横坐标，原点再左上角

    ¦  (0, 0)  -----------------------Y
    ¦  (1, 0) ....  (1, 2)
    ¦        (2, 1)
    ¦               (3, 2)
    X
    :param x:
    :param y:
    :param chess:
    :return:
    """
    if not in_bound((x, y)):
        print(f'{x}, {y} not on board')
        return False

    elif board[x][y] != ' ':
        print('already filled !')
        return False
    else:
        board[x][y] = str(chess)
        return True


def run():
    print("run wuzi")
    max_step = 15 * 15
    step_count = 0
    black_turn = True
    while True:
        try:
            if black_turn:
                xy_arr = input('[黑棋] 请输入棋子（横坐标0-14, 纵坐标0-14)：').split()
                xy = int(xy_arr[0]), int(xy_arr[1])
                chess = Chess.BLACK
            else:
                xy_arr = input('[白棋]: 请输入棋子（横坐标0-14, 纵坐标0-14)：').split()
                xy = int(xy_arr[0]), int(xy_arr[1])
                chess = Chess.WHITE
        except Exception as e:
            print(e)
            continue

        fall_res = fall_chess(xy[0], xy[1], chess)
        if not fall_res:
            continue
        step_count = step_count + 1
        black_turn = not black_turn

        printboard1(board)

        win_flag = is_win(FillPoint(xy[0], xy[1], chess))
        if win_flag:
            print(f"{str(chess)} win !")
            break

if __name__ == "__main__":
    run()

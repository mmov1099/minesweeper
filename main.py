import random
from readchar import readkey, key
import os
import time

# 初級：9×9のマスに10個の地雷（Windows Meまでのバージョンは8×8）
# 中級：16×16のマスに40個の地雷
# 上級：30×16のマスに99個の地雷
os.system('cls')
print("Select difficulty: 1: Beginner, 2: Intermediate, 3: Advanced")
difficulty = int(input())

if difficulty == 1:
    height = 9
    width  = 9
    mine_num = 10
elif difficulty == 2:
    height = 16
    width  = 16
    mine_num = 40
elif difficulty == 3:
    height = 16
    width  = 30
    mine_num = 99

blocks = [i for i in range(1, height * width + 1)]
opened_blocks = set()
mines = set(random.sample(blocks, k = mine_num))
mines_flag = set()

def count_mines(blocks, i):
    if i % width == 0:
        target_idx = [
        i - width, i - width + 1,
        i + 1,
        i + width, i + width + 1
        ]
    elif i % width == width-1:
        target_idx = [
            i - width - 1, i - width,
            i - 1,
            i + width - 1, i + width
        ]
    else:
        target_idx = [
            i - width - 1, i - width, i - width + 1,
            i - 1, i + 1,
            i + width - 1, i + width, i + width + 1
        ]

    mines_num = 0
    for idx in target_idx:
        if idx >= 0 and idx < len(blocks) and blocks[idx] in mines:
            mines_num += 1
    return mines_num

mine_num_dict = {i: count_mines(blocks, i-1) for i in blocks}

def print_field(blocks, current_block):
    for i in range(1, len(blocks)+1):
        if i % width == 1:
            print()
        if i == current_block:
            print("▽", end = ' ', ) if i in opened_blocks else print("▼", end = ' ')
        elif i in mines_flag:
            print("●", end = ' ')
        elif i in opened_blocks:
            mines_num = mine_num_dict[i]
            print(mines_num, end = ' ') if mines_num > 0 else print("□", end = ' ')
        else:
            print("■", end = ' ')
    print("\n")

def print_blocks(blocks):
    for i in range(1, len(blocks)+1):
        if i % width == 1:
            print()
        print(i, end = '\t')
    print("\n")

def print_mines(blocks):
    for i in range(1, len(blocks)+1):
        if i % width == 1:
            print()
        print("X", end = ' ') if i in mines else print("■", end = ' ')
    print("\n")

def print_mine_num(blocks):
    for i in range(1, len(blocks)+1):
        if i % width == 1:
            print()
        print(mine_num_dict[i], end = ' ')
    print("\n")

def auto_open_blocks(selected_block):
    if selected_block % width == 1:
        side_block = [
            selected_block - width,
            selected_block + 1,
            selected_block + width
        ]
    elif selected_block % width == 0:
        side_block = [
            selected_block - width,
            selected_block - 1,
            selected_block + width
        ]
    else:
        side_block = [
            selected_block - width,
            selected_block - 1, selected_block + 1,
            selected_block + width
        ]
    if mine_num_dict[selected_block] == 0:
        side_block += [
            selected_block - width - 1, selected_block - width + 1,
            selected_block + width - 1, selected_block + width + 1
        ]

    for block in side_block:
        if block in blocks and block not in opened_blocks and block not in mines:
            opened_blocks.add(block)
            if mine_num_dict[block] == 0:
                auto_open_blocks(block)

start_time = time.time()
current_block = width*height//2 + width//2
while len(opened_blocks) < len(blocks) - len(mines) + 1:
    # os.system('cls')
    # print_blocks(blocks)
    print_field(blocks, current_block)
    # print_mines(blocks)
    # print_mine_num(blocks)
    # selected_block = int(input('\nSelect a number: '))
    print(f"Mine: {len(mines_flag)}/{len(mines)}")
    print(f"Time: {int(time.time() - start_time)}s")
    print('Move: ↑, ↓, ←, →, Open: Enter, Flag: Space')

    k = readkey()
    if k == key.DOWN:
        if current_block + width in blocks:
            current_block += width
    if k == key.UP:
        if current_block - width in blocks:
            current_block -= width
    if k == key.LEFT:
        if current_block - 1 in blocks:
            current_block -= 1
    if k == key.RIGHT:
        if current_block + 1 in blocks:
            current_block += 1
    if k == key.ENTER:
        selected_block = current_block
        if selected_block in mines and len(opened_blocks) == 0:
            mines.remove(selected_block)
            while True:
                new_mine = random.choice(blocks)
                if new_mine not in mines and new_mine != selected_block:
                    break
            mines.add(new_mine)
            mine_num_dict = {i: count_mines(blocks, i-1) for i in blocks}
        elif selected_block in mines:
            print("You lose!")
            exit()
        opened_blocks.add(selected_block)
        opened_blocks.add(auto_open_blocks(selected_block))
    if k == key.SPACE:
        # 地雷フラグの処理
        if current_block in mines_flag:
            mines_flag.remove(current_block)
        elif current_block not in opened_blocks:
            mines_flag.add(current_block)

print('You win!')

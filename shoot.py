import curses
import random

# curses
curses.initscr()
height = 20; width = 30
win = curses.newwin(height, width, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

# others
lose = 0
score = 0
key = -1
ESC = 27
buttons = [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, ESC]

# ship coords
if width % 2 == 0:
    shipx = int(width / 2)
else:
    shipx = int((width-1)/2)
shipy = height - 2

# asteroid coords
astx_minmax = range(1, width-2)
asty_minmax = range(1, height-10)
astx = random.sample(astx_minmax, 7)
asty = random.sample(asty_minmax, 7)
prev_asty = []
prev_astx = []
# bullet coords
init_bulx = []
init_buly = []
prev_bulx = []
prev_buly = []
# ammo system
ammomax = 16
ammocurrent = ammomax
ammx_minmax = range(1, width-2)
ammy_minmax = range(1, height-10)
ammlen = 3
ammx = random.sample(ammx_minmax, ammlen)
ammy = random.sample(ammy_minmax, ammlen)
prev_ammy = []
prev_ammx = []
# spawn objects
def others():
    win.addstr(0, 2, 'Score: ' + str(score) + ' ')
    win.addstr(0, width - 12, 'Ammo: ' + str(ammocurrent) + "/" + str(ammomax) + ' ')
    win.addch(shipy, shipx, '#')
# spawn asteroids
def asteroids():
    i = 0
    while i <= len(asty) - 1:
        win.addch(prev_asty[i], prev_astx[i], ' ')
        win.addch(asty[i], astx[i], '*')
        i += 1
# spawn ammo crates
def ammosys():
    j = 0
    while j <= len(ammy) - 1:
        win.addch(prev_ammy[j], prev_ammx[j], ' ')
        win.addch(ammy[j], ammx[j], '$')
        j += 1
# spawn bullets
def bullet():
    j = 0
    while j <= len(prev_buly) - 1:
        win.addch(prev_buly[j], prev_bulx[j], ' ')
        win.addch(init_buly[j], init_bulx[j], '+')
        j += 1
# amm collide
def detect_amm():
    if init_buly != []:
        i = 0
        j = 0
        while i <= len(ammy)-1:
            if ammy[i] == height - 2:
                if ammx[i] == shipx:
                    ammy.remove(ammy[i])
                    ammx.remove(ammx[i])
                    ammy.append(random.randint(1, height-10))
                    ammx.append(random.randint(1, width-2))
                    return 1
            while j <= len(init_buly) - 1:
                if ammy[i] == init_buly[j]:
                    if ammx[i] == init_bulx[j]:
                        win.addch(init_buly[j], init_bulx[j], ' ')
                        init_buly.remove(init_buly[j])
                        init_bulx.remove(init_bulx[j])
                        ammy.remove(ammy[i])
                        ammx.remove(ammx[i])
                        ammy.append(random.randint(1, height-10))
                        ammx.append(random.randint(1, width-2))
                        return 1
                j += 1
            i += 1
            j = 0
# ast collide
def detect_ast():
    if init_buly != []:
        i = 0
        j = 0
        while i <= len(asty)-1:
            while j <= len(init_buly) - 1:
                if asty[i] == init_buly[j]:
                    if astx[i] == init_bulx[j]:
                        win.addch(init_buly[j], init_bulx[j], ' ')
                        init_buly.remove(init_buly[j])
                        init_bulx.remove(init_bulx[j])
                        asty.remove(asty[i])
                        astx.remove(astx[i])
                        asty.append(random.randint(1, height-10))
                        astx.append(random.randint(1, width-2))
                        return 1
                j += 1
            i += 1
            j = 0
# lagpas amm
def lagpas_amm():
    i = 0
    while i <= len(ammy)-1:
        if ammy[i] == height - 2:
            win.addch(ammy[i], ammx[i], ' ')
            ammy.remove(ammy[i])
            ammx.remove(ammx[i])
            ammy.append(random.randint(1, height-10))
            ammx.append(random.randint(1, width-2))
        i += 1
# lagpas ast
def lagpas_ast():
    i = 0
    while i <= len(asty)-1:
        if asty[i] == height - 2:
            return 1
        i += 1
            


clock = 0

# main loop
while key != ESC:    
    others()
    event = win.getch()
    key = event

    detect_am = detect_amm()
    if detect_am == 1:
        ammocurrent = ammomax
    detect_am = 0

    detect_as = detect_ast()
    if detect_as == 1:
        score += 1
    detect_as = 0

    lagpas_amm()
    lose = lagpas_ast()

    if clock % 50 == 0:
        prev_asty = asty
        prev_astx = astx
        asty = [x + 1 for x in asty]
        asteroids()

    if clock % 15 == 0:
        prev_ammy = ammy
        prev_ammx = ammx
        ammy = [x + 1 for x in ammy]
        ammosys()

    if clock % 2 == 0:
        prev_buly = init_buly
        prev_bulx = init_bulx
        if init_buly != []:
            if init_buly[-1] != 1:
                init_buly = [x - 1 for x in init_buly]
            else:
                win.addch(init_buly[-1], init_bulx[-1], ' ')
                init_buly.remove(init_buly[-1])
                init_bulx.remove(init_bulx[-1])
                init_buly = [x - 1 for x in init_buly]
    if init_buly != []:
            if init_buly[-1] == 0:
                win.addch(init_buly[-1], init_bulx[-1], ' ')
                init_buly.remove(init_buly[-1])
                init_bulx.remove(init_bulx[-1])
    
    if clock % 2 == 0: bullet()
    
    if key not in buttons:
        key = -1
    if key == curses.KEY_LEFT and shipx > 1:
        win.addch(shipy, shipx, ' ')
        shipx -= 1
    if key == curses.KEY_RIGHT and shipx < width-2:
        win.addch(shipy, shipx, ' ')
        shipx += 1
    if key == curses.KEY_UP and ammocurrent > 0:
        ammocurrent -= 1
        win.addch(shipy-1, shipx, '+')
        init_bulx.insert(0, shipx)
        init_buly.insert(0, shipy-1)

    win.timeout(1)
    win.refresh()
    if lose == 1: break
    if ammocurrent == 0 and init_buly == []: break
    if clock == 1500: clock = 0
    else: clock += 1   

# end
print(f"score = {score}")
curses.endwin()

# project started on 04/04/2021
import pygame
import os
pygame.font.init()

WIDTH, HEIGHT = 1200, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('boobs')


yoshi_width = 70
yoshi_size = (yoshi_width, round(yoshi_width*1.25))

yoshi_speed = 4

yoshi_jump = False
ascending = False
descending = False

jump_speed = 3
grav = 3
jump_interv = 80

yoshi_y_init = round(HEIGHT - HEIGHT*.109943 - yoshi_size[1])

bg_speed = 1

FPS = 60

DARK_BLUE = (26, 50, 145)
CLEAR_BLUE = (59, 91, 219)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


yoshi_img = pygame.transform.scale(pygame.image.load(resource_path(os.path.join('assets', 'yoshi.png'))), yoshi_size)

bg_img = pygame.transform.scale(pygame.image.load(resource_path(os.path.join('assets', 'bg.jpg'))), (WIDTH, HEIGHT))

main_menu_img = pygame.transform.scale(pygame.image.load(resource_path(os.path.join('assets', 'main_menu.jpg'))), (WIDTH, HEIGHT))

pause_menu_img = pygame.transform.scale(pygame.image.load(resource_path(os.path.join('assets', 'pause_menu.png'))), (WIDTH, HEIGHT))

pause_font = pygame.font.SysFont('impact', 40)

button_font = pygame.font.SysFont('impact', 20)
class Button():
    def __init__(self, x, y, w, h, text: str, funct:callable =lambda: print('undefined function')):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.y = y
        self.x = x
        self.w = w
        self.h = h
        self.funct = funct
    
    def draw(self, color=DARK_BLUE, wind=win):
        pygame.draw.rect(wind, color, self.rect)
        draw_text = button_font.render(self.text, 1, (255, 255, 255))
        wind.blit(draw_text, (self.x + self.w//2 - draw_text.get_width()//2, self.y + self.h//2 - draw_text.get_height()//2)) 


def draw_stuff(yoshi, bgs: list):
    win.blit(bg_img, (0, 0))    

    for i in bgs:
        win.blit(bg_img, (i.x, i.y))

    win.blit(yoshi_img, (yoshi.x, yoshi.y))

    pygame.display.update()


def movement_yoshi(keys, yoshi):
    global yoshi_jump, ascending, descending
    if keys[pygame.K_SPACE] and not yoshi_jump:
        yoshi_jump = True
    

    if yoshi_jump:
        if not descending:
            ascending = True
            yoshi.y -= jump_speed
        
        if ascending and yoshi.y < yoshi_y_init - jump_interv:
            ascending = False
            descending = True

        if descending:
            yoshi.y += grav

        if descending and yoshi_y_init - jump_speed < yoshi.y < yoshi_y_init  + grav:
            descending = False
            yoshi_jump = False
            yoshi.y = yoshi_y_init


def movement_bg(bg1, bg2):

    for i in [bg1, bg2]:
        if i.x - bg_speed <= -WIDTH:
            i.x = WIDTH
        
        i.x -= bg_speed
        

def main():

    yoshi = pygame.Rect(60, yoshi_y_init, yoshi_size[0], yoshi_size[1])
    clock = pygame.time.Clock()

    bg1 = pygame.Rect(0, 0, WIDTH, HEIGHT)
    bg2 = pygame.Rect(WIDTH, 0, WIDTH, HEIGHT)

    while True:
        clock.tick(FPS)

        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE]:
                    pause_menu()

        movement_yoshi(keys_pressed, yoshi)
        movement_bg(bg1, bg2)
        draw_stuff(yoshi, [bg1, bg2])

current = -1

def draw_menu(buttons, mx, my, click, enter):
    global current
    win.blit(main_menu_img, (0, 0))

    i = 0
    for b in buttons:
        r = b.rect
        if r.collidepoint((mx, my)):
            current = -1
            b.draw(CLEAR_BLUE)
            if click:
                b.funct()
                click = False
                return False
        elif i == current:
            b.draw(CLEAR_BLUE)
            if enter:
                b.funct()
                click = False
                return False
        else:
            b.draw(DARK_BLUE)
        i += 1

    pygame.display.update()
    return True


def main_menu():
    global current
    current = -1
    clock = pygame.time.Clock()

    buttons = [Button(160, 300, 300, 75, 'Play', main), Button(160, 390, 300, 75, 'Exit', pygame.quit)]
    run = True

    while run:
        clock.tick(FPS)
        mx, my = pygame.mouse.get_pos()
        enter = False
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            else:
                click = False

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_z]:
                    current -= 1
                    if current < 0:
                        current = len(buttons) - 1
                
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    current += 1
                    if current >= len(buttons):
                        current = 0

                if event.key == pygame.K_RETURN:
                    enter = True    
        
        run = draw_menu(buttons, mx, my, click, enter)


def draw_pause(buttons, mx, my, click, enter):
    global current

    i = 0
    for b in buttons:
        r = b.rect
        if r.collidepoint((mx, my)):
            current = -1
            b.draw(CLEAR_BLUE)
            if click:
                b.funct()
                click = False
                return False
        elif i == current:
            b.draw(CLEAR_BLUE)
            if enter:
                b.funct()
                click = False
                return False
        else:
            b.draw(DARK_BLUE)
        i += 1

    pygame.display.update()
    return True


def pause_menu():
    global current
    current = -1
    clock = pygame.time.Clock()

    buttons = [Button(453, 268, 300, 70, 'Resume', lambda: ...), Button(453, 456, 300, 70, 'Main Menu', main_menu), Button(453, 362, 300, 70, 'Exit', pygame.quit)]

    win.blit(pause_menu_img, (0, 0))

    draw_text = pause_font.render('Pause Menu', 1, (255, 255, 255))
    win.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, 40))
    pygame.display.update()

    run = True
    while run:
        clock.tick(30)

        mx, my = pygame.mouse.get_pos()
        click = False
        enter = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            else:
                click = False

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_z]:
                    current -= 1
                    if current < 0:
                        current = len(buttons) - 1
                
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    current += 1
                    if current >= len(buttons):
                        current = 0

                if event.key == pygame.K_RETURN:
                    enter = True    
        
        run = draw_pause(buttons, mx, my, click, enter)
    


if __name__ == '__main__':
    main_menu()


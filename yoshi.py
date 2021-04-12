
# project started on 04/04/2021
import pygame
import os

WIDTH, HEIGHT = 900, 596
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('boobs')


yoshi_width = 150
yoshi_size = (yoshi_width, round(yoshi_width*.8111))

yoshi_speed = 4

bg_speed = 1

FPS = 60

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


def draw_stuff(yoshi, bgs: list):
    win.blit(bg_img, (0, 0))    

    for i in bgs:
        win.blit(bg_img, (i.x, i.y))

    win.blit(yoshi_img, (yoshi.x, yoshi.y))

    pygame.display.update()


def movement_yoshi(keys, yoshi):
    ...


def movement_bg(bg1, bg2):

    for i in [bg1, bg2]:
        if i.x - bg_speed <= -WIDTH:
            i.x = WIDTH
        
        i.x -= bg_speed
        


def main():

    yoshi = pygame.Rect(60, HEIGHT - 39 - yoshi_size[1], yoshi_size[0], yoshi_size[1])
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

        movement_yoshi(keys_pressed, yoshi)
        movement_bg(bg1, bg2)
        draw_stuff(yoshi, [bg1, bg2])


if __name__ == '__main__':
    main()


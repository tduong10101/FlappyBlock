import pygame
import random
import time
pygame.init()
clock = pygame.time.Clock()
white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
main_width = 800
main_height = 600
gameDisplay = pygame.display.set_mode((main_width,main_height))
pygame.display.set_caption("FlappyBlock")

def main_block(pos_x,pos_y,width,height):
    pygame.draw.rect(gameDisplay,black,[pos_x,pos_y,width,height])

def high_block(pos_x,width,height):
    pygame.draw.rect(gameDisplay,green,[pos_x,0,width,height])

def low_block(pos_x,pos_y,width,height):
    pygame.draw.rect(gameDisplay,green,[pos_x,pos_y,width,height])

def create_obstruction(obj_x,obj_y,obj_width):
    obs_l_block_y = 150 + obj_y
    obs_l_block_height = main_height - obs_l_block_y
    high_block(obj_x,obj_width,obj_y)
    low_block(obj_x,obs_l_block_y,obj_width,obs_l_block_height)
    return obs_l_block_y

def score_update(count):
    font = pygame.font.SysFont(None,25)
    text = "Score: " + str(count)
    message_display(text,50,20,font,black)

def crash():
    message_display('You Crashed')
    time.sleep(1)
    game_loop()

def text_objects(text,font,color):
    textsurface = font.render(text, True, color)
    return textsurface, textsurface.get_rect()

def message_display(text,x_pos=main_width*0.5,y_pos=main_height*0.5,font=pygame.font.Font('freesansbold.ttf',115),color=red):
    TextSurf, TextRect = text_objects(text, font, color)
    TextRect.center = ((x_pos),(y_pos))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

def game_loop():
    count = 0
    pos_x = -40
    pos_y = main_height*0.5
    gravity = 0
    fly_x = 2.5
    speed = -4


    obj1 = {'x': 1000, 'width': 70, 'y': random.randrange(0,400), 'count':False,'l_y':main_height}
    obj2 = {'x': 1500, 'width': 70, 'y': random.randrange(0,400),'count':False,'l_y':main_height}
    objs = [obj1,obj2]

    block_width = block_height = 25


    while True:
        gravity = 3.5
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                gravity = -75

        if pos_x + fly_x < main_width/3:
            pos_x += fly_x
        else:
            pos_y += gravity
            for obj in objs:
                obj['x']  += speed

        for obj in objs:
            if obj['x'] <= -obj['width']:
                obj['x'] = main_width + obj['width']
                obj['y'] = random.randrange(0,400)
                obj['count']=False
            if obj['x']+obj['width'] < pos_x and obj['count']==False:
                count += 1
                obj['count']=True


        gameDisplay.fill(white)

        for obj in objs:
            obj['l_y'] = create_obstruction(obj['x'],obj['y'],obj['width'])
        score_update(count)



        if pos_y + block_height >= main_height:
            pos_y = main_height - block_height
            main_block(pos_x,pos_y,block_width,block_height)
            crash()

        for obj in objs:
            if pos_y < obj['y'] or pos_y + block_height > obj['l_y']:
                if pos_x + block_width >= obj['x'] and pos_x <= obj['x'] + obj['width']:
                    if obj['y']-pos_y <= block_height and obj['y']-pos_y >0:
                        pos_y = obj['y']
                    main_block(pos_x,pos_y,block_width,block_height)
                    crash()

        main_block(pos_x,pos_y,block_width,block_height)
        pygame.display.update()
        clock.tick(60)

game_loop()

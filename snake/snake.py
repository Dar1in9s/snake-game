import pygame
from pygame.locals import *
import random
import sys
                     #窗口大小和蛇的大小
windows_width=800
windows_height=600
snake_size=20

white = (255, 255, 255)      #可能用到的颜色
black = (0, 0, 0)
gray = (230, 230, 230)
dark_gray = (40, 40, 40)
DARKGreen = (0, 155, 0)
Green = (0, 255, 0)
Red = (255, 0, 0)
blue = (0, 0, 255)
dark_blue =(0,0, 139)
                      #上下左右
UP=1
DOWN=2
LEFT=3
RIGHT=4
               #游戏结束后在来一次
AGAIN=5

def wellcom(screen):          #游戏初始界面
    image_wellcome=pygame.image.load("./wellcome.jpg")
    screen.blit(image_wellcome, (0, 0))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                sys.exit()
            elif event.type==KEYDOWN:
                pygame.time.wait(100)
                return
def game_over(screen):          #游戏结束界面
    game_over_sound=pygame.mixer.Sound("./game_over .wav")
    game_over_sound.play()
    image_gameover=pygame.image.load("./gameover.jpg")
    screen.blit(image_gameover,(0,0))
    pygame.display.update()
def snake_draw(screen,snake_body):        #画蛇
    for body in snake_body:
        x=body["x"]*20
        y=body["y"]*20
        pygame.draw.rect(screen,blue,(x,y,snake_size,snake_size))
        pygame.draw.rect(screen,dark_blue,(x+4,y+4,snake_size-8,snake_size-8))
def snake_move(snake_body,derection):         #通过增加头节点和删除尾节点来实现移动
    if derection==RIGHT:
        snake_head = {"x": snake_body[0]["x"] + 1, "y": snake_body[0]["y"]}
    elif derection==LEFT:
        snake_head = {"x": snake_body[0]["x"] - 1, "y": snake_body[0]["y"]}
    elif derection==UP:
        snake_head = {"x": snake_body[0]["x"], "y": snake_body[0]["y"] - 1}
    elif derection==DOWN:
        snake_head = {"x": snake_body[0]["x"], "y": snake_body[0]["y"] + 1}
    snake_body.insert(0,snake_head)  #增加头节点
    snake_body_num=0
    for body in snake_body:
        snake_body_num+=1      #得到有多少个节点
    snake_body.pop(snake_body_num-1)     #删除尾节点
def food(screen,x,y):            #画食物
    pygame.draw.rect(screen,blue,(x*20,y*20,snake_size,snake_size))
    pygame.display.update()
def if_eat(food_x,food_y,snake_body):        #判断是否吃到了食物
    if snake_body[0]["x"]==food_x and snake_body[0]["y"]==food_y:
        snake_body.insert(0,{"x":food_x,"y":food_y})
        return True
def if_eatself(snake_body):         #判断是否咬到了自己
    snake_head=snake_body[0]
    node=0
    for body in snake_body:
        if(snake_head==body and node>1):
            return True
        node+=1
def if_Hit_wall(snake_body):      #判断是否撞墙了
    if(snake_body[0]["x"]>windows_width/snake_size-1 or snake_body[0]["x"]<0 or snake_body[0]["y"]>windows_height/snake_size-1 or snake_body[0]["y"]<0):
        return True
def score(screen,snake_body):   #成绩
    scroe_=-3
    for body in snake_body:
        scroe_+=1
    myfont=pygame.font.Font("./myfont.ttf",60)
    Difficulty_level = int(scroe_ / 5) + 1
    my_scroe=myfont.render("成绩：{}".format(scroe_),True,dark_blue)
    my_level=myfont.render("难度：{}".format(Difficulty_level),True,dark_blue)

    screen.blit(my_scroe,(570,40))
    screen.blit(my_level,(570,100))
    pygame.display.update()
    return  Difficulty_level
def game_run(screen,snake_body,derection):      #游戏进行过程
    food_x = random.randint(0, windows_width / snake_size-1)
    food_y = random.randint(0, windows_height / snake_size-1)
    image_background=pygame.image.load("./backgrand.jpg")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT and derection!=RIGHT:
                    derection = LEFT
                elif event.key == K_RIGHT and derection!=LEFT:
                    derection = RIGHT
                elif event.key == K_UP and derection!=DOWN:
                    derection = UP
                elif event.key == K_DOWN and derection!=UP:
                    derection = DOWN
        snake_move(snake_body,derection)
        screen.blit(image_background,(0,0))
        snake_draw(screen, snake_body)
        if (if_Hit_wall(snake_body) or if_eatself(snake_body)):
            pygame.mixer.music.stop()
            game_over(screen)          #游戏结束
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        sys.exit()
                    elif event.type==KEYDOWN:
                        if event.key==K_ESCAPE:
                            sys.exit()
                        else:
                            return AGAIN

        food(screen,food_x,food_y)       #生成食物
        Difficulty_level=score(screen, snake_body)
        pygame.display.update()
        if(100-20*Difficulty_level>0):
            speed=100-20*Difficulty_level
        else:
            speed=0
        pygame.time.wait(speed)
        if(if_eat(food_x,food_y,snake_body)):     #判断是否吃到食物
            return derection
def main():      #游戏主循环
    pygame.init()
    screen=pygame.display.set_mode((windows_width,windows_height))
    pygame.display.set_caption("snake!")
    wellcom(screen)
    while True:
        start_x = random.randint(8, windows_width / snake_size - 8)
        start_y = random.randint(8, windows_height / snake_size - 8)
        snake_body = [{"x": start_x, "y": start_y}, {"x": start_x - 1, "y": start_y}, {"x": start_x - 2, "y": start_y}]
        derection = RIGHT
        pygame.mixer.music.load("./backgrand.mp3")
        pygame.mixer.music.play(-1)
        while True:
            derection=game_run(screen,snake_body,derection)
            if(derection==AGAIN):
                break

if __name__ == '__main__':
    try:
        main()
    except:
        sys.exit()




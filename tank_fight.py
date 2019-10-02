import pygame,sys
import time
from pygame.locals import *
from random import randint
MOVE_SLEEP=0.01

class TankMain():
    width=600
    height=500
    desTime=0
    grade=0
    myShells = []
    life=3
    enemyList = pygame.sprite.Group()
    def setLife(self,live=3):
        self.life=int(live)
    def getGrade(self):#创建字体
        text = pygame.font.Font("font/msyh.ttc", 20).render("分数:{}  生命值:{}".format(self.grade,self.life), True, (0, 255, 0))
        return text
    #开始游戏
    def startGame(self):
        try:
            pygame.init()#加载操作系统资源
            self.screen=pygame.display.set_mode((self.width,self.height),0,32)#窗口大小
            pygame.display.set_caption("打坦克")#窗口标题
            self.myTank=MyTank(self.screen)
            for i in range(6):
                self.enemyList.add(BnemyTank(self.screen))
            # 窗口更新
            while True:
                if len(self.enemyList)<6:
                    if time.time()-self.desTime>1:
                        self.enemyList.add(BnemyTank(self.screen))
                self.screen.fill((0, 0, 0))  # 窗口背景色
                #监听事件
                key = pygame.key.get_pressed()
                if key[K_LEFT]:
                    self.myTank.move('L')
                elif key[K_RIGHT]:
                    self.myTank.move('R')
                elif key[K_UP]:
                    self.myTank.move('U')
                elif key[K_DOWN]:
                    self.myTank.move('D')
                else:
                    pass
                self.get_event()
                #敌方tank移动
                [enemy.moveMore() for enemy in self.enemyList]
                #显示所有
                self.myTank.display()
                [enemy.display() for enemy in self.enemyList]
                [shell.move() for shell in self.myShells]
                for shell in self.myShells:
                    b = shell.move()
                    if b == True:
                        self.myShells.remove(shell)
                        b = 0
                    a=shell.hitTank()
                    if a==True:
                        self.myShells.remove(shell)
                        self.grade+=1
                        self.desTime=time.time()
                        a=0
                if self.myTank.live==True:
                    a = self.myTank.hitTank()
                    if a == True:
                        self.life-=1
                        if self.life<=0:
                            self.myTank.live=False
                        else:self.myTank=MyTank(self.screen)
                [shell.display() for shell in self.myShells]
                self.screen.blit(self.getGrade(), (5, 5))  # 添加文字块
                if self.myTank.live==False:
                    self.stopGamePrint()
                # 刷新窗口
                pygame.display.update()
                time.sleep(MOVE_SLEEP)
        except Exception as e:
            print(e)
    #结束游戏说明
    def stopGamePrint(self):
        text=pygame.font.Font("font/msyh.ttc", 70).render("game over!", True, (0, 255, 0))
        self.screen.blit(text, (100, 200))
    #结束游戏
    def stopGame(self):
        sys.exit()
    #事件监听设置
    def get_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.stopGame()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.myShells.append(self.myTank.fire())
                if event.key == K_ESCAPE:
                    self.stopGame()


#坦克大战所有对象的基类
class BaseItem(pygame.sprite.Sprite):
    def __init__(self,screen):
        self.screen=screen
        pygame.sprite.Sprite.__init__(self)

#坦克类
class Tank(BaseItem):
    width=50
    height=50
    time=0
    direction='U'
    images={}
    def __init__(self,screen,left,top):
        super().__init__(screen)
        self.screen=screen
        self.speed=2
        self.images['L'] = pygame.image.load("images/04.jpg")
        self.images['R'] = pygame.image.load("images/02.jpg")
        self.images['U'] = pygame.image.load("images/01.jpg")
        self.images['D'] = pygame.image.load("images/03.jpg")
        self.image=self.images[self.direction]
        self.rect=self.image.get_rect()
        self.rect.left=left
        self.rect.top=top
        self.live=True#坦克是否被消灭
    #显示tank
    def display(self):
        self.time+=1
        if self.live==True:
            self.image=self.images[self.direction]
            self.screen.blit(self.image,self.rect)
    def isObstacle(self):#判断障碍物
        tag=''
        if self.rect.left<=0:tag+='L'
        if self.rect.left>=TankMain.width-self.width:tag+='R'
        if self.rect.top<=0:tag+='U'
        if self.rect.top>=TankMain.height-self.height:tag+='D'
        return tag
    def fire(self):#创建子弹对象
        m=Shell(self.screen,self)
        return m
    def move(self,direction):
        if self.live==True:
            if self.time>1/MOVE_SLEEP:
                if direction==self.direction:
                    obstacle=self.isObstacle()
                    if self.direction=='L' and ('L' not in obstacle):
                        self.rect.left-=self.speed
                    elif self.direction=='R' and ('R' not in obstacle):
                        self.rect.left+=self.speed
                    elif self.direction=='U' and ('U' not in obstacle):
                        self.rect.top-=self.speed
                    elif self.direction=='D' and ('D' not in obstacle):
                        self.rect.top+=self.speed
                    else:pass
                else:
                    self.direction=direction
                #time.sleep(MOVE_SLEEP)

class MyTank(Tank):
    images={}
    live=True
    def __init__(self,screen):
        super().__init__(screen,275,450)
        self.images['L'] = pygame.image.load("images/4.jpg")
        self.images['R'] = pygame.image.load("images/2.jpg")
        self.images['U'] = pygame.image.load("images/1.jpg")
        self.images['D'] = pygame.image.load("images/3.jpg")
        self.image = self.images[Tank.direction]
        self.screen=screen
        self.rect = self.image.get_rect()
        self.rect.left = 275
        self.rect.top = 450
    #重载
    def display(self):
        self.time+=1
        self.image=self.images[self.direction]
        self.screen.blit(self.image,self.rect)
    #判断碰撞
    def hitTank(self):
        hitList=pygame.sprite.spritecollide(self, TankMain.enemyList,False)
        for e in hitList:
            self.live=False
            return True
        return False



class BnemyTank(Tank):
    def __init__(self,screen):
        super().__init__(screen,randint(1,5)*100,0)
        self.getDirection()#初始化方向
        self.step=0#连续移动步数
        self.speed=1
    def getDirection(self):#获取随机方向
        self.direction = ['L', 'R', 'U', 'D'][randint(0, 3)]  # 初始化敌方tank方向
    def moveMore(self):#地方坦克连续移动
        if self.live==True:
            if self.step==0 or (self.direction in self.isObstacle()):
                self.getDirection()
                self.step=randint(0,200)
            else:
                self.move(self.direction)
                self.step-=1
            #time.sleep(MOVE_SLEEP)

class Shell(BaseItem):
    width=12
    height=12
    def __init__(self,screen,tank):
        super().__init__(screen)
        self.screen=screen
        self.image=pygame.image.load("images/3.png")
        self.direction=tank.direction
        self.rect=self.image.get_rect()
        self.rect.left=tank.rect.left+(tank.width-self.width)/2.0
        self.rect.top=tank.rect.top+(tank.height-self.height)/2.0
        self.speed=3
        self.live=True
    def isObstacle(self):#判断障碍物
        tag=''
        if self.rect.left<=0:tag+='L'
        if self.rect.left>=TankMain.width-self.width:tag+='R'
        if self.rect.top<=0:tag+='U'
        if self.rect.top>=TankMain.height-self.height:tag+='D'
        return tag
    def move(self):
        if self.live == True:
            obstacle=self.isObstacle()
            if self.direction=='L' and ('L' not in obstacle):
                self.rect.left-=self.speed
            elif self.direction=='R' and ('R' not in obstacle):
                self.rect.left+=self.speed
            elif self.direction=='U' and ('U' not in obstacle):
                self.rect.top-=self.speed
            elif self.direction=='D' and ('D' not in obstacle):
                self.rect.top+=self.speed
            else:return True
        else:pass
        #time.sleep(MOVE_SLEEP)
    def display(self):
        if self.live==True or self.live==False:
            self.screen.blit(self.image,self.rect)
    def hitTank(self):
        hitList=pygame.sprite.spritecollide(self, TankMain.enemyList,False)
        for e in hitList:
            e.live=False
            TankMain.enemyList.remove(e)
            self.live=False
            return True
        return False

class Blast(BaseItem):
    def __init__(self,screen,rect):
        super().__init__(screen)
        self.rect=rect


if __name__ == '__main__':
    try:
        live=input("设置生命数 按回车键跳过 默认为3\n")
        print("碰到坦克失去一条生命 坦克出现时有冷却时间 按回车键开始游戏")
        input()
        game = TankMain()
        if live=='':
            pass
        elif live.isdigit():
            game.setLife(live)
        else:
            print("生命值设置错误，3后按默认设置开始游戏")
            time.sleep(3)
        game.startGame()
    except Exception as e:
        print(str(e))
        input()
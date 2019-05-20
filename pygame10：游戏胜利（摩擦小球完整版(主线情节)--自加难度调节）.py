from pygame.locals import *
from random import *
import traceback
import tkinter as tk
import pygame
import math
import sys

class Ball(pygame.sprite.Sprite) :  #继承动画精灵基类
    def __init__ (self,grayball_image,greenball_image,position,speed,bg_size,target) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(grayball_image).convert_alpha()   
        self.grayball_image = grayball_image
        self.greenball_image = greenball_image
        self.rect = self.image.get_rect()   #获得球的尺寸
        self.rect.left , self.rect.top = position   #将出现的位置赋给球
        self.direction = [ speed[0]/abs(speed[0]) , speed[1]/abs(speed[1]) ]  #小球当前运动的方向
        self.speed = [ abs(speed[0]) , abs(speed[1]) ]  #设置速度大小
        self.colide = False #设置是否发生碰撞属性
        self.hole = False #设置是否进黑洞
        self.target = target    #设置一个使小球变为可控的目标
        self.control = False    #小球是否人为可控的标志
        self.width , self.height = bg_size[0] , bg_size[1]  #获得活动边界，就是背景的边界
    
    def drawball(self):
        if self.control :   #如果小球可用，control=1
            self.image = pygame.image.load(self.greenball_image)     #重新绘制小球为绿色的小球
        else :  #否则绘制灰色小球
            self.image = pygame.image.load(self.grayball_image)
    
    def move(self):
        if not self.hole :  #如果小球没有进过黑洞
            if self.control:    #如果小球被控制
                self.rect = self.rect.move(self.speed)          #根据自己的速度移动
            else:
                self.rect = self.rect.move((self.direction[0] * self.speed[0],\
                                                        self.direction[1] * self.speed[1]))         #没被控制的小球则要乘上方向

            if self.rect.right < 0:    #图片的右边已经超出边界的左边，即整个球已经出界
                self.rect.left = self.width    #让他从右边界回来
            if self.rect.bottom < 0:    #图片的底已经超出边界的上面
                self.rect.top = self.height   #让他从底部回来
            if self.rect.left > self.width:   #图片的左边已经超出边界的右边
                self.rect.right = 0     #让他从左边回来
            if self.rect.top > self.height:  #如果图片的顶部已经超出边界的底部
                self.rect.bottom = 0    #让他从顶部回来

    def check(self,motion):     #检查鼠标移动的频率是否打到控制小球的目标值
        if self.target*2 < motion < self.target*2 + 10 :
            self.control = True #小球可控标志设为1
            return True
        else :
            return False

#判断碰撞检测函数
def collide_check(item,target):
    col_balls = []      #添加碰撞小球
    for each in target:     #对 target 中所有的目标小球进行检测
        #两个球心之间的距离
        distance = math.sqrt( math.pow( (item.rect.center[0] - each.rect.center[0]) , 2 )  + \
                                        math.pow( (item.rect.center[1] - each.rect.center[1]) , 2) )
        if distance <= ( item.rect.width + each.rect.width ) / 2:   #如果距离小于等于两者间的半径之和也就是两个直径之和的一半
            col_balls.append(each)  #将这个发生碰撞的小球添加到列表中
    
    return col_balls


def main() :
    pygame.init()   #初始化

    #将所有图片的路径写入
    bg_image = r"D:\Code\Python\Pygame\pygame10：游戏胜利\background.png"    #背景图
    grayball_image = r"D:\Code\Python\Pygame\pygame10：游戏胜利\gray_ball.png"   #灰小球的图片
    greenball_image = r"D:\Code\Python\Pygame\pygame10：游戏胜利\green_ball.png"     #绿小球的图片
    galss_image = r"D:\Code\Python\Pygame\pygame10：游戏胜利\glass.png"      #玻璃板图片
    hand_image = r"D:\Code\Python\Pygame\pygame10：游戏胜利\hand.png"    #鼠标在玻璃板上的样子
    hand1_image = r"D:\Code\Python\Pygame\pygame10：游戏胜利\hand1.png"      #鼠标在其他地方的样子
    beijing1_image = r"D:\Code\Python\Pygame\pygame10：游戏胜利\beijing1.png"   #第一张背景
    beijing2_image = r"D:\Code\Python\Pygame\pygame10：游戏胜利\beijing2.png"   #第二章背景
    beijing3_image = r"D:\Code\Python\Pygame\pygame10：游戏胜利\beijing3.png"   #第三章背景
    beijing4_image = r"D:\Code\Python\Pygame\pygame10：游戏胜利\beijing4.png"   #第四章背景


    running = True  #为了以后而已有多种方法退出程序

     # 存放要打印的消息
    msgs = []

    #加载背景音乐
    pygame.mixer.music.load(r"D:\Code\Python\Pygame\pygame10：游戏胜利\bg_music.ogg")
    pygame.mixer.music.set_volume(0.2)  #设置音量

    #设置一个背景音乐完毕之后的结束事件
    GAMEOVER = USEREVENT
    pygame.mixer.music.set_endevent(GAMEOVER)   #当音乐播完后，发送一个GAMEOVER事件

    #加载四个音效
    hole_music = pygame.mixer.Sound(r"D:\Code\Python\Pygame\pygame10：游戏胜利\hole.wav")
    laugh_music = pygame.mixer.Sound(r"D:\Code\Python\Pygame\pygame10：游戏胜利\laugh.wav")    
    winner_music = pygame.mixer.Sound(r"D:\Code\Python\Pygame\pygame10：游戏胜利\winner.wav")
    loser_music = pygame.mixer.Sound(r"D:\Code\Python\Pygame\pygame10：游戏胜利\loser.wav")
    dazi_music = pygame.mixer.Sound(r"D:\Code\Python\Pygame\pygame10：游戏胜利\dazi.wav")

    #设置背景
    bg_size = width , height = 1024 , 681       #背景大小
    screen = pygame.display.set_mode(bg_size) # 设置背景大小
    background = pygame.image.load(bg_image).convert_alpha()       #画背景
    
    #加载故事背景图
    beijing1 = pygame.image.load(beijing1_image).convert_alpha()  
    beijing2 = pygame.image.load(beijing2_image).convert_alpha()  
    beijing3 = pygame.image.load(beijing3_image).convert_alpha()  
    beijing4 = pygame.image.load(beijing4_image).convert_alpha()  
    beijing = [beijing1,beijing2,beijing3,beijing4]

    #绘制用于摩擦的玻璃板，要花在小球前面，不然的话，后面小球会从玻璃板的下方划过
    galss = pygame.image.load(galss_image).convert_alpha()  #画玻璃板
    galss_rect = galss.get_rect()   #获得玻璃板的尺寸
    galss_rect.left , galss_rect.top = ((width-galss_rect[2])/2 , (height-galss_rect[3]))      #玻璃板的位置
    balls = []
    group = [] #会发生碰撞的小球

    clock = pygame.time.Clock()    #生成刷新帧率控制器

    #加载鼠标图片
    hand = pygame.image.load(hand_image).convert_alpha()   #画玻璃版内鼠标
    hand1 = pygame.image.load(hand1_image).convert_alpha()  #画平常鼠标
    flag = False    #设置一个变量，用来表示鼠标是否进入玻璃板范围

    #设置响应键盘连续输入
    pygame.key.set_repeat(100,100)

    #用来计数一秒钟内移动的次数
    motion = 0  
    #设置一个自定义事件，用来检测鼠标移动的值是否符合控制小球的目标值
    MYTIMER = USEREVENT + 1     #因为之前已经定义了一个自定义事件，所以根据之前说的这个自定义事件应该是之前的加1
    pygame.time.set_timer(MYTIMER,1000)     #计时器事件为1s  
    # 创建五个小球
    BALL_NUM = 5

    #地图上的黑洞的坐标,因为 100% 命中太难，所以只要在范围内即可
    # 每个元素：(x1, x2, y1, y2)
    hole = [(117, 119, 199, 201), (225, 227, 390, 392), \
            (503, 505, 320, 322), (698, 700, 192, 194), \
            (906, 908, 419, 421)]

    screen.blit(background, (0, 0)) #将背景画到screen上
    screen.blit(galss,(galss_rect.left , galss_rect.top))    #将玻璃板绘制在screen上
    pygame.display.flip()

    #循环绘制故事背景图
    for i in range (len(beijing)):
        screen.blit(background, (0, 0)) #将背景画到screen上
        screen.blit(galss,(galss_rect.left , galss_rect.top))    #将玻璃板绘制在screen上
        pygame.display.flip()
        screen.blit(beijing[i],(50,50))   #画第一张故事背景
        dazi_music.play()   #播放打字特效
        pygame.time.delay(1000) #延时1s
        pygame.display.flip()
        pygame.time.delay(1000) #延时2s
        if i == 3:
            screen.blit(beijing[i],(50,50))   #画第一张故事背景
            pygame.time.delay(1000) #延时1s
            pygame.display.flip()

    #设立难度等级
    global grade
    grade = 5

    #调节游戏难度
    root = tk.Tk()  #窗口初始化
    root.title('Game difficulty setting')   #设置标题
    root.geometry('400x350')    #设置大小
    label1= tk.Label(root,text = '请调节您想要的游戏的难度',font = ('华文行楷','15'))   #显示label框
    label1.pack(padx=5,pady=10)
    label2 = tk.Label(root,bg = 'yellow',text ='当前的游戏难度为：'+ str(grade),font = ('华文行楷','13'))
    label2.pack(padx=1,pady=1)
    frame1 = tk.Frame(height=4, bd=4, relief="sunken")  #使用Frame分割
    frame1.pack(fill="x", padx=5, pady=5)
    

    #快速调节难度等级：
    labelframe1 = tk.LabelFrame(root,text = '快速选择:',font = ('华文行楷','10')) 
    labelframe1.pack(fill='x',padx=20,pady=10)
    #自动调节难度函数
    def changegrade_zidong():
        global grade
        grade = var.get()
        label2.config(text='当前的游戏难度已改为：' + str(grade))#让对象显示括号里的内
    #创建label组件
    var = tk.IntVar()
    label3 = tk.Radiobutton(labelframe1,text ='1',variable=var, value=1,command = changegrade_zidong)
    label3.pack()
    label4 = tk.Radiobutton(labelframe1,text ='5',variable=var, value=5,command = changegrade_zidong)
    label4.pack()
    label5 = tk.Radiobutton(labelframe1,text ='9',variable=var, value=9,command = changegrade_zidong)
    label5.pack()

    #手动调节难度等级:
    labelframe2 = tk.LabelFrame(root,text = '手动调节s:',font = ('华文行楷','10'))
    labelframe2.pack(fill='x',padx=20,pady=10)
    #手动调节难度函数
    def changegrade_shoudongadd():
        global grade
        grade += 1
        label2.config(text='当前的游戏难度已改为：' + str(grade))#让对象显示括号里的内
    def changegrade_shoudongsub():
        global grade
        grade -= 1
        label2.config(text='当前的游戏难度已改为：' + str(grade))#让对象显示括号里的内
    def makesure():
        root.destroy()
    button1 = tk.Button(labelframe2,text='难度 + 1',command=changegrade_shoudongadd)
    button1.pack()
    button2 = tk.Button(labelframe2,text='难度 - 1 ',command=changegrade_shoudongsub)
    button2.pack()
    button3 = tk.Button(root,text='确定',command=makesure)
    button3.pack()

    root.mainloop()

    pygame.mixer.music.play()   #调节好游戏难度后播放背景音乐


    for i in range (BALL_NUM) :    #生成5个球
        position = randint (0,width-100) ,  randint(0,height-100)   #要减去100是因为球图片尺寸的大小为100，随机生成位置
        #speed  = [ randint (-10,10) , randint(-10,10) ]    因为这种方法会生成新bug有的时候速度生成值为0所以使用新的方法
        speed = [choice([-1,1])*randint(1,10),choice([-1,1])*randint(1,10)]   #随机生成速度
        ball  = Ball(grayball_image,greenball_image,position,speed,bg_size,grade*(i+1))  #生成球的对象
        while collide_check(ball,balls):    #如果生成的小球和之前的球发生碰撞，那么重新在随机位置生成小球
            ball.rect.left , ball.rect.top = randint (0,width-100) ,  randint(0,height-100)     
        balls.append(ball)  #将所有的球对象添加到列表中，方便管理
        group.append(ball)  #将所有的球对象添加到会碰撞的小球中，方便管理

    while running :
        for event in pygame.event.get():

            if event.type == QUIT:  #如果事件类型是退出
                sys.exit()

            elif event.type == GAMEOVER:      #如果音乐结束事件类型为其返回的自定义事件游戏结束
                loser_music.play()  #播放失败的音乐
                pygame.time.delay(2000) #延时2s
                laugh_music.play()  #播放大笑音效
                running = False

            elif event.type == MOUSEMOTION:   #如果事件类型为鼠标移动
                mouse_x , mouse_y = pygame.mouse.get_pos()    #获取鼠标移动的当前位置
                if (galss_rect.left <= mouse_x <= galss_rect.right) \
                                and  (galss_rect.top <= mouse_y <= galss_rect.bottom):   #如果鼠标在玻璃板内，那么flag=1
                    motion += 1     #如果鼠标在玻璃版内滑动，那么motion+1
                    flag = True 
                else :  #不再范围内鼠标可见
                    flag = False
            
            elif event.type == MYTIMER:     #如果事件类型为自己的定义的定时器事件
                for each in balls : #遍历所有的球
                    if each.check(motion):  #调用他们各自的check()函数，看是否打到控制要求的目标,如果达到要求，即返回值为真
                        each.drawball()    #调用球类中的画图方法将灰色球划成绿色球
                        each.speed = [0,0]  #将他们的速度设为0，等待人类的控制
                motion = 0    #等到所有的球都进行判断之后将motion重新设为0，进行下一秒的循环

            elif event.type == KEYDOWN :    #如果时间类型是键盘上的键按下
                if event.key == K_UP or event.key == K_w :    #如果按下的键是向上键或者w键
                    for each in balls :     #遍历所有的小球 查看他们的control属性
                        if each.control :   #如果control属性为真，即小球可控
                            each.speed[1] -= 1  #每按一下就减一 营造加速度的效果 下面的类似
                if event.key == K_DOWN or event.key == K_s :   #如果按下的键是向下键或者s键
                    for each in balls :     #遍历所有的小球 查看他们的control属性
                        if each.control :   #如果control属性为真，即小球可控
                            each.speed[1] += 1
                if event.key == K_LEFT or event.key == K_a :   #如果按下的键是向左键或者a键
                    for each in balls :     #遍历所有的小球 查看他们的control属性
                        if each.control :   #如果control属性为真，即小球可控
                            each.speed[0] -= 1
                if event.key == K_RIGHT or event.key == K_d :  #如果按下的键是向右键或者d键
                    for each in balls :     #遍历所有的小球 查看他们的control属性
                        if each.control :   #如果control属性为真，即小球可控
                            each.speed[0] += 1
                if event.key == K_SPACE :    #如果按下的是键盘上的空格键
                    for each in group :     
                        if each.control :       #遍历所有小球中被人为控制的球
                            for i in hole : #遍历所有黑洞
                                #如果被控制的小球位置在黑洞运行的范围内
                                if ((i[0] <= each.rect.left <= i[1]) and (i[2] <= each.rect.top <= i[3])) :         
                                    #播放黑洞音效
                                    hole_music.play()
                                    #小球速度变为0
                                    each.speed = [0,0]
                                    #进黑洞属性变为True
                                    each.hole = True
                                    #将这个小球从碰撞组中删除，这样其他球就不会撞他
                                    group.remove(each)
                                    #并将这个小球从之前的balls列表中删除，然后插到列表的最前面，这样其他球就会在他的上面飘过
                                    temp = balls.pop(balls.index(each))
                                    balls.insert(0,temp)
                                    # 一个坑一个球
                                    hole.remove(i)
                            # 坑都补完了，游戏结束
                            if not hole:
                                pygame.mixer.music.stop()
                                winner_music.play()
                                pygame.time.delay(3000)
                                # 打印“然并卵”
                                
                                msg = pygame.image.load(r"D:\Code\Python\Pygame\pygame10：游戏胜利\win.png").convert_alpha()
                                msg_pos = (width - msg.get_width()) // 2, \
                                          (height - msg.get_height()) // 2
                                msgs.append((msg, msg_pos))
                                laugh_music.play()

        screen.blit(background, (0, 0)) #将背景画到screen上
        screen.blit(galss,(galss_rect.left , galss_rect.top))    #将玻璃板绘制在screen上

        if  flag :  #如果鼠标进入玻璃板
            #设置鼠标不可见
            mouse_x , mouse_y = pygame.mouse.get_pos()    #获取鼠标移动的当前位置
            pygame.mouse.set_visible(False) #原鼠标不可见
            screen.blit(hand,(mouse_x,mouse_y))   #画上我们玻璃版内鼠标
        else :  #如果鼠标没进入玻璃板
            pygame.mouse.set_visible(False) #原鼠标不可见
            screen.blit(hand1,(mouse_x,mouse_y))   #画上我们自己的平常鼠标

        for each in balls:  #每个球进行移动并重新绘制
            each.move()    
            if each.colide :    #如果这个小球刚发生过碰撞
                each.speed = [randint(3,10),randint(3,10)]    #改变速度
                each.colide = False
            screen.blit(each.image, each.rect)
        
        for i in range (len(group)) : #循环5个小球，分别判断这个小球有没有和另外四个小球发生碰撞
            item = group.pop(i)    #因为是判断和其他四个小球，所以需要先将这个小球取出
            if collide_check( item , group ):  #调用碰撞检测的函数，如果结果为真，也就是有发生碰撞的小球
                item.colide = True  #小球碰撞属性设为真
                item.direction[0] = - item.direction[0] #小球的运动方向反向，然后速度随机
                item.direction[1] = - item.direction[1] 
                if item.control:
                    item.direction[0] = -1 
                    item.direction[1] = -1 
                    item.control = False
                    item.drawball()    #调用小球的绘制函数，重新把小球画成灰色
            group.insert(i, item)  #最后不要忘记把这个小球放回原位

        #画上文字
        for msg in msgs:
            screen.blit(msg[0], msg[1])
            #延时5秒关闭
            pygame.time.delay(5000)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    # 这样做的好处是双击打开时如果出现异常可以报告异常，而不是一闪而过！
    try:
        main()
    except SystemExit: #这是按下 × 的异常，直接忽略
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
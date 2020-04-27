import cv2 as cv
import numpy as np
from numba import jit
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from random import *

class Ant:
    def __init__(self,Pos,Dir,img):
        self.pos=Pos #蚂蚁位置(y,x)
        self.dir=Dir #蚂蚁移动方向（true为向左，false为向右）
        self.hp=2*img.shape[1]
        self.delta_phero=1
        self.img = img

        self.itaList=[]
   
    def Predict(self,phero):

        #判断当前是否在边界处：
        #若在上下边界处，判定蚂蚁死亡
        #若在左右边界处，恢复蚂蚁生命力并改变其移动方向
        Pos=self.pos
        itaList=[]
        alpha=0.2
        beta=0.8
        img=self.img

        if self.dir:
        #蚂蚁右移
            for j in range(0,2):
                for i in range(-1,2):
                    G=img.item(Pos[0]+i,Pos[1]+j)-img.item(Pos[0],Pos[1])
                    if i is 0 and j is 0:
                        continue
                    else:
                        if abs(G)<1:
                            itaList.append(((i,j),1))
                        elif G<=-1:
                            itaList.append(((i,j),abs(G)))
                        else:
                            itaList.append(((i,j),1/G))

                        #将移动概率分布添加到itaList中
            S=0
            for x in itaList:
                S+=phero[Pos[0]+x[0][0],Pos[1]+x[0][1]]**alpha*x[1]**beta

            temp=[[x[0],x[1],phero[Pos[0]+x[0][0],Pos[1]+x[0][1]]**alpha*x[1]**beta/S] for x in itaList]
            self.itaList=temp#能见度列表,每项元素为[(x,y),ita,prob],即坐标变化量、能见度大小、移动概率
        else:
            #蚂蚁左移
            for j in range(-1,1):
                for i in range(-1,2):
                    G=img.item(Pos[0]+i,Pos[1]+j)-img.item(Pos[0],Pos[1])
                    if i is 0 and j is 0:
                        continue
                    else:
                        if abs(G)<1:
                            itaList.append([(i,j),1])
                        elif G<=-1:
                            itaList.append([(i,j),abs(G)])
                        else:
                            itaList.append([(i,j),1/G])
            S=0
            for x in itaList:
                S+=phero[Pos[0]+x[0][0],Pos[1]+x[0][1]]**alpha*x[1]**beta

            temp=[[x[0],x[1],phero[Pos[0]+x[0][0],Pos[1]+x[0][1]]**alpha*x[1]**beta/S] for x in itaList]
            self.itaList=temp 

    def __del__(self):
        pass

    def Next(self,phero):
        self.Predict(phero)
        img=self.img
        #按概率选择下一步的移动方向
        prob=[x[2] for x in self.itaList]
        idx=np.random.choice(len(prob),1,p=prob)
        idx=idx[0]
        (delta_y,delta_x)=self.itaList[idx][0]

        self.pos=(self.pos[0]+delta_y,self.pos[1]+delta_x)

        #counts, N = plt.hist(phero,256)

        # compute threshold
        T0 = sum(sum(phero))/(phero.shape[0]*phero.shape[1])
        #gL = phero.copy()
        #hL = phero.copy()
        #gU = phero.copy()
        #hU = phero.copy()

        #gL[gL>T0] = 0
        #hL[hL<=T0] = 1
        #hL[hL>T0] = 0

        #gU[gU<T0] = 0
        #hU[hU>=T0] = 1
        #hU[hU<T0] = 0

        #mL = sum(sum(gL))/sum(sum(hL))
        #mU = sum(sum(gU))/sum(sum(hU))

        #T1 = (mL+mU)/2
        #while abs(T1-T0)>0.1:
        #    T0 = T1
        #    gL = phero.copy()
        #    hL = phero.copy()
        #    gU = phero.copy()
        #    hU = phero.copy()

        #    gL[gL>T0] = 0
        #    hL[hL<=T0] = 1
        #    hL[hL>T0] = 0

        #    gU[gU<T0] = 0
        #    hU[hU>=T0] = 1
        #    hU[hU<T0] = 0

        #    mL = sum(sum(gL))/sum(sum(hL))
        #    mU = sum(sum(gU))/sum(sum(hU))

        #    T1 = (mL+mU)/2

        ObjectArea = phero.copy()
        ObjectArea[ObjectArea<T0] = 0
        ObjectArea[ObjectArea>T0] = 1


        if ObjectArea[self.pos[0],self.pos[1]]==0:
            self.hp-=60
        else:
            self.hp+=20

        if self.pos[0]==img.shape[0]-1 or self.pos[0]==0:
        #蚂蚁在上下边界处，判定死亡
            self.hp=0
        elif self.pos[1]==img.shape[1]-1 or self.pos[1]==0:
            #蚂蚁在左右边界处，恢复生命力并改变移动方向
            self.dir=not self.dir
            self.hp= 2*self.img.shape[1]
            #改变移动方向时横坐标要移动一个单位，防止在边界继续停留继续改变移动方向
            if self.pos[1]==img.shape[1]-1:
                #到达右边界，向左弹回一个单位
                self.pos=(self.pos[0],self.pos[1]-1)
            else:
                #到达左边界，向右弹回一个单位
                self.pos=(self.pos[0],self.pos[1]+1)
        else:
            #print(img.shape[0]-1)
            pass

def InitAnts(img):
    interval = 3
    if img.shape[0]%interval==0:
        row=int(img.shape[0]/interval)-1
    else:
        row=int(img.shape[0]/interval)

    if img.shape[1]%interval==0:
        col=int(img.shape[1]/interval)-1
    else:
        col=int(img.shape[1]/interval)

    InitPoints=[]
    for i in range(col):
        for j in range(row):
            p=random()
            if p<0.5:
                InitPoints.append(Ant(((j+1)*interval-1,(i+1)*interval-1),True,img))
            else:
                InitPoints.append(Ant(((j+1)*interval-1,(i+1)*interval-1),False,img))
    return InitPoints

def RunAntColony(Mat):
    img = cv.GaussianBlur(Mat,(5,5),1)
    phero = np.zeros(img.shape)+20 #信息素分布
    Acc = np.zeros(img.shape) #累加器平面
    tempMat = np.zeros(img.shape)
    Ants = InitAnts(img)

    single_step = np.zeros(img.shape)
    is_start = False

    rho = 0.1
    phi = 0.05
    for t in range(int(img.shape[1])):
        #更新信息素分布
        if t>int(0.5*img.shape[1]):
            is_start=True
        for m in Ants:
            if m.hp>0:
                m.Next(phero)
                single_step[m.pos[0],m.pos[1]]+=1
                if is_start:
                    Acc[m.pos[0],m.pos[1]]+=1

        phero = (1-rho)*phero + 20*single_step

    #plt.imshow(phero,cmap='gray')  #将像素转换为单通道照片，照片一般是3通道的rgb模式
    #plt.show()

    #plt.imshow(Acc,cmap='gray')  #将像素转换为单通道照片，照片一般是3通道的rgb模式
    #plt.show()
    phero = np.array(phero)
    phero = (phero-phero.min())/(phero.max()-phero.min())
    phero = 255*phero
    phero = phero.astype(np.uint8)

    Acc = np.array(Acc)
    Acc = (Acc-Acc.min())/(Acc.max()-Acc.min())
    Acc = 255*Acc
    Acc = Acc.astype(np.uint8)

    #kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32) #定义一个核
    #dst = cv.filter2D(Acc, -1, kernel=kernel)

    T0 = np.sum(Acc)/(Acc.shape[0]*Acc.shape[1])
    gL = Acc.copy()
    hL = Acc.copy()
    gU = Acc.copy()
    hU = Acc.copy()

    gL[gL>T0] = 0
    hL[hL>T0] = 0
    hL[hL<=T0] = 1

    gU[gU<T0] = 0
    hU[hU<T0] = 0
    hU[hU>=T0] = 1

    mL = sum(sum(gL))/sum(sum(hL))
    mU = sum(sum(gU))/sum(sum(hU))

    T1 = (mL+mU)/2
    while abs(T1-T0)>1:
        T0 = T1
        gL = Acc.copy()
        hL = Acc.copy()
        gU = Acc.copy()
        hU = Acc.copy()

        gL[gL>T0] = 0      
        hL[hL>T0] = 0
        hL[hL<=T0] = 1

        gU[gU<T0] = 0      
        hU[hU<T0] = 0
        hU[hU>=T0] = 1

        mL = sum(sum(gL))/sum(sum(hL))
        mU = sum(sum(gU))/sum(sum(hU))

        T1 = (mL+mU)/2

    ret, th = cv.threshold(Acc, T1, 255, cv.THRESH_BINARY)

    return phero,Acc,th

    cv.namedWindow('phero', cv.WINDOW_AUTOSIZE)
    cv.imshow('phero', phero)

    cv.namedWindow('Acc', cv.WINDOW_AUTOSIZE)
    cv.imshow('Acc', Acc) 

    cv.namedWindow('th', cv.WINDOW_AUTOSIZE)
    cv.imshow('th', th)    
    cv.waitKey(0)
    cv.destroyAllWindows()
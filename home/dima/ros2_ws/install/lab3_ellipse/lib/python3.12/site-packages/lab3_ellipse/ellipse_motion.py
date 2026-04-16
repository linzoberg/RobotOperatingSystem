#!/usr/bin/env python3
import math

class EllipseMotion:
    def __init__(self, a, b, speed):
        self.a=a; self.b=b; self.speed=speed
        self.wp=[]; self.i=0

    def start(self,x,y,yaw):
        self.wp=[]; self.i=0
        c=math.cos(yaw); s=math.sin(yaw)
        # центр эллипса - ВПЕРЕДИ робота на 'a' метров
        # робот стоит точно на первой точке (t=π)
        cx=x+self.a*c; cy=y+self.a*s
        N=400
        for k in range(N):
            t=math.pi+2*math.pi*k/N
            lx=self.a*math.cos(t); ly=self.b*math.sin(t)
            gx=cx+lx*c-ly*s; gy=cy+lx*s+ly*c
            self.wp.append((gx,gy))

    def compute(self,cur_x,cur_y,cur_yaw):
        if not self.wp: return 0.0,0.0,False
        look=0.18
        # ищем точку впереди
        for _ in range(150):
            tx,ty=self.wp[self.i]
            if math.hypot(tx-cur_x,ty-cur_y)>look: break
            self.i=(self.i+1)%len(self.wp)
        ang=math.atan2(ty-cur_y,tx-cur_x)
        err=math.atan2(math.sin(ang-cur_yaw),math.cos(ang-cur_yaw))
        v=self.speed
        w=2.8*err
        w=max(-2.0,min(2.0,w))
        if abs(err)>1.4: v=0.05
        return v,w,False  # False = никогда не останавливаемся

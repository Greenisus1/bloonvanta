#!/usr/bin/env python3
"""Original offline balloon-path tower defense, waves and upgrades."""
import curses,math,time
from ui import put,run
VERSION='1.0.0'
PATH=[(x,3) for x in range(2,18)]+[(17,y) for y in range(4,11)]+[(x,10) for x in range(16,2,-1)]+[(3,y) for y in range(11,16)]+[(x,15) for x in range(4,23)]
class Defense:
 def __init__(self):self.money=100;self.lives=20;self.wave=0;self.towers={};self.balloons=[];self.remaining=0;self.timer=0;self.active=False;self.won=False
 def build(self,p,kind):
  if p in PATH or p in self.towers or not(0<=p[0]<25 and 0<=p[1]<18):return False
  cost=35 if kind==1 else 55
  if kind not in (1,2) or self.money<cost:return False
  self.money-=cost;self.towers[p]={'kind':kind,'level':1,'cooldown':0.};return True
 def upgrade(self,p):
  t=self.towers.get(p)
  if not t or t['level']>=3:return False
  cost=30*t['level']
  if self.money<cost:return False
  self.money-=cost;t['level']+=1;return True
 def start(self):
  if self.active or self.won or self.lives<=0:return False
  self.wave+=1;self.remaining=6+self.wave*2;self.timer=0;self.active=True;return True
 def step(self,dt):
  if not self.active:return
  dt=max(0,min(.1,dt));self.timer-=dt
  if self.remaining and self.timer<=0:self.balloons.append({'pos':0.,'hp':1+self.wave//3});self.remaining-=1;self.timer=.65
  for b in self.balloons:b['pos']+=(1.8+self.wave*.22)*dt
  for p,t in self.towers.items():
   t['cooldown']-=dt
   if t['cooldown']>0:continue
   reach=3+t['level'];targets=[b for b in self.balloons if b['hp']>0 and b['pos']<len(PATH) and math.dist(p,PATH[int(b['pos'])])<=reach]
   if targets:
    target=max(targets,key=lambda b:b['pos']);target['hp']-=t['level'];t['cooldown']=.6/t['level'] if t['kind']==1 else 1.
    if t['kind']==2:
     point=PATH[int(target['pos'])]
     for b in targets:
      if b is not target and math.dist(point,PATH[int(b['pos'])])<=2:b['hp']-=1
  alive=[]
  for b in self.balloons:
   if b['hp']<=0:self.money+=5
   elif b['pos']>=len(PATH):self.lives-=1
   else:alive.append(b)
  self.balloons=alive
  if self.lives<=0:self.active=False
  elif not self.remaining and not alive:self.active=False;self.money+=20;self.won=self.wave>=10

def loop(s):
 s.timeout(50);g=Defense();cursor=(5,5);paused=False;message='1 dart tower35 | 2 splash tower55 | Enter starts wave';last=time.monotonic()
 while True:
  h,w=s.getmaxyx();key=s.getch();now=time.monotonic();dt=now-last;last=now
  if key in (27,ord('q')):return
  if key==ord('r'):g=Defense();message='New defense.'
  if key in (ord('p'),ord(' ')):paused=not paused
  moves={curses.KEY_UP:(0,-1),curses.KEY_DOWN:(0,1),curses.KEY_LEFT:(-1,0),curses.KEY_RIGHT:(1,0),ord('w'):(0,-1),ord('s'):(0,1),ord('a'):(-1,0),ord('d'):(1,0)}
  if key in moves:dx,dy=moves[key];cursor=max(0,min(24,cursor[0]+dx)),max(0,min(17,cursor[1]+dy))
  if key in (ord('1'),ord('2')):message='Built.' if g.build(cursor,key-ord('0')) else 'Cannot build here or insufficient coins.'
  if key==ord('u'):message='Upgraded.' if g.upgrade(cursor) else 'Cannot upgrade (max3 or need coins).'
  if key in (10,13):message='Wave started.' if g.start() else 'Finish current wave first.'
  if w>=52 and h>=24 and not paused:g.step(dt)
  s.erase();put(s,0,1,f'BLOONVANTA  wave {g.wave}/10  lives {g.lives} coins {g.money}',curses.A_BOLD)
  if w<52 or h<24:put(s,3,1,'Resize to52x24. Defense paused.')
  else:
   cw=max(2,(w-2)//25);rh=max(1,(h-6)//18);left=(w-cw*25)//2
   ballooncells={PATH[min(len(PATH)-1,int(b['pos']))] for b in g.balloons}
   for y in range(18):
    for x in range(25):
     p=x,y;t=g.towers.get(p);v='O' if p in ballooncells else ('D' if t['kind']==1 else 'S')+str(t['level']) if t else '·' if p in PATH else '░'
     for n in range(rh):put(s,3+y*rh+n,left+x*cw,v.center(cw) if t or p in ballooncells else v*cw,curses.A_REVERSE if p==cursor else (curses.color_pair(3)|curses.A_BOLD) if p in ballooncells else (curses.color_pair(4)|curses.A_BOLD) if t else curses.color_pair(2))
   put(s,h-3,1,'ALL10 WAVES CLEARED! R retry' if g.won else 'DEFENSE LOST. R retry' if g.lives<=0 else 'PAUSED' if paused else message)
  put(s,h-1,1,'Arrows/WASD cursor |1/2 build | U upgrade | Enter wave | P pause | R reset | Esc/q exit');s.refresh()
if __name__=='__main__':
 import sys
 if '--version' in sys.argv:print(VERSION)
 else:raise SystemExit(run(loop))

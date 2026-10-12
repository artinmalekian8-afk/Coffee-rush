import os
os.makedirs("assets",exist_ok=True)
from PIL import Image, ImageDraw, ImageFilter
import math
S=2048
img=Image.new("RGB",(S,S))
d=ImageDraw.Draw(img)
top=(104,58,31); bot=(43,24,14)
for y in range(S):
    t=y/(S-1)
    d.line([(0,y),(S,y)],fill=tuple(int(top[i]+(bot[i]-top[i])*t) for i in range(3)))
glow=Image.new("RGBA",(S,S),(0,0,0,0))
ImageDraw.Draw(glow).ellipse([S*0.2,S*0.28,S*0.8,S*0.88],fill=(240,148,77,70))
glow=glow.filter(ImageFilter.GaussianBlur(120))
img=Image.alpha_composite(img.convert("RGBA"),glow)
cx=S//2
CREAM=(250,244,234,255); SHADE=(226,214,198,255)
def layer():
    l=Image.new("RGBA",(S,S),(0,0,0,0)); return l,ImageDraw.Draw(l)
l,ld=layer()
ld.ellipse([cx+250,960,cx+640,1360],fill=CREAM)
hole=Image.new("L",(S,S),0); ImageDraw.Draw(hole).ellipse([cx+350,1050,cx+540,1270],fill=255)
a=l.split()[3]; a=Image.composite(Image.new("L",(S,S),0),a,hole); l.putalpha(a)
img=Image.alpha_composite(img,l)
l,ld=layer()
ld.ellipse([cx-560,1450,cx+560,1610],fill=SHADE)
ld.ellipse([cx-560,1420,cx+560,1560],fill=CREAM)
img=Image.alpha_composite(img,l)
pts=[(cx-420,900),(cx+420,900),(cx+340,1250)]
for i in range(0,101):
    ang=math.radians(i*1.8)
    pts.append((cx+340*math.cos(ang), 1250+230*math.sin(ang)))
pts.append((cx-340,1250))
l,ld=layer(); ld.polygon(pts,fill=CREAM)
sh=Image.new("RGBA",(S,S),(0,0,0,0)); sd=ImageDraw.Draw(sh)
sd.polygon([(cx+250,880),(cx+440,880),(cx+440,1500),(cx+170,1500)],fill=SHADE)
m=l.split()[3]; sh.putalpha(Image.composite(sh.split()[3],Image.new("L",(S,S),0),m))
img=Image.alpha_composite(img,l); img=Image.alpha_composite(img,sh)
d=ImageDraw.Draw(img)
d.ellipse([cx-420,860,cx+420,960],fill=(214,200,182,255))
d.ellipse([cx-385,872,cx+385,948],fill=(90,49,24,255))
d.ellipse([cx-300,885,cx+300,935],fill=(201,138,78,255))
l,ld=layer()
def steam(x,y0,h,amp,w=24):
    for i in range(400):
        t=i/399
        px=x+math.sin(t*math.pi*2)*amp; py=y0-t*h
        ld.ellipse([px-w,py-w,px+w,py+w],fill=(255,236,214,255))
steam(cx-190,800,420,45); steam(cx,760,500,-50); steam(cx+190,800,420,45)
img=Image.alpha_composite(img,l)
img=img.convert("RGB").resize((1024,1024),Image.LANCZOS)
img.save("assets/icon-only.png")

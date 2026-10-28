from pathlib import Path
import fitz, math, json, shutil
from PIL import Image
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'output'; OUT.mkdir(exist_ok=True)
A=ROOT/'input'; D=ROOT.parents[2]/'deliverables'; B=D/'board-assets-20261026'; G=ROOT/'assets'
W,H=297*72/25.4,420*72/25.4; SX,SY=W/587,H/887
BLACK=(.012,.015,.012); Y=(1,.90,0); GOLD=(.77,.62,.29); CREAM=(1,.96,.82); WHITE=(.97,.96,.90)
COLS=[(.12,.72,.88),(.98,.40,.60),(.92,.12,.20),(.98,.76,.18),(.34,.66,.36)]
PALE=[(.82,.95,.99),(1,.87,.91),(1,.88,.80),(1,.95,.77),(.88,.96,.81)]
ROLES=['sheng','dan','jing','mo','chou']; NAMES=['生','旦','净','末','丑']; FONTS={'sans':str(G/'sans-sub.ttf'),'bold':str(G/'bold-sub.ttf'),'brush':str(G/'brush-sub.otf'),'serif':str(G/'serif-sub.ttf')}
doc=fitz.open(); SRC={}; audit=[]
def rr(x,y,w,h):return fitz.Rect(x*SX,y*SY,(x+w)*SX,(y+h)*SY)
def pt(x,y):return fitz.Point(x*SX,y*SY)
def rect(p,x,y,w,h,fill=BLACK,stroke=None,lw=.5,radius=None):p.draw_rect(rr(x,y,w,h),fill=fill,color=stroke,width=lw*SY,radius=radius)
def line(p,x1,y1,x2,y2,c=GOLD,lw=.5):p.draw_line(pt(x1,y1),pt(x2,y2),color=c,width=lw*SY)
def txt(p,x,y,s,size=8,c=WHITE,font='sans',center=None):
 if center is not None:
  ff=fitz.Font(fontfile=FONTS[font]);x=center-ff.text_length(s,fontsize=size*SY)/SX/2
 p.insert_text(pt(x,y),s,fontname=font,fontfile=FONTS[font],fontsize=size*SY,color=c)
def circle(p,x,y,r,fill=None,stroke=GOLD,lw=.5):p.draw_oval(rr(x-r,y-r,2*r,2*r),color=stroke,fill=fill,width=lw*SY)
def ellipse(p,x,y,w,h,fill=None,stroke=GOLD,lw=.5):p.draw_oval(rr(x,y,w,h),color=stroke,fill=fill,width=lw*SY)
def poly(p,pts,c=GOLD,lw=.5,fill=None,closed=False):p.draw_polyline([pt(x,y) for x,y in pts],color=c,width=lw*SY,fill=fill,closePath=closed)
def img(p,path,x,y,w,h,clip=None,trim=False,stretch=False):
 path=Path(path);key=str(path)
 if key not in SRC:
  im=Image.open(path); iw,ih=im.size; box=im.getchannel('A').point(lambda v: 255 if v>40 else 0).getbbox() if im.mode=='RGBA' else (0,0,iw,ih)
  if box: box=(max(0,box[0]-12),max(0,box[1]-12),min(iw,box[2]+12),min(ih,box[3]+12))
  sd=fitz.open();sp=sd.new_page(width=iw,height=ih);sp.insert_image(sp.rect,filename=key);SRC[key]=(sd,iw,ih,box)
 sd,iw,ih,box=SRC[key]; crop=fitz.Rect(clip or (box if trim else (0,0,iw,ih)))
 p.show_pdf_page(rr(x,y,w,h),sd,clip=crop,keep_proportion=not stretch)
 visible_w=rr(x,y,w,h).width;visible_h=rr(x,y,w,h).height
 scale=min(visible_w/crop.width,visible_h/crop.height)
 audit.append({'page':p.number+1,'asset':key,'source_px':[iw,ih],'placed_box':[x,y,w,h],'effective_ppi':round(72/scale)})
def bar(p,x,y,w,title,num):
 bw=max(91,33+len(title)*7.6);rect(p,x,y,bw,17,Y,radius=.45)
 txt(p,x+8,y+12.4,num,10.5,BLACK,'bold');txt(p,x+32,y+12.2,title,8.7,BLACK,'bold')
 line(p,x+bw+5,y+8.5,x+w,y+8.5,Y,.55)
def micro(p,x,y,s):txt(p,x,y,s,6.6,CREAM)
def cloud(p,x,y,w,h,fill=None,stroke=GOLD,lw=.8):
 # Gold-outline ruyi cloud, scalable vector artwork.
 P=lambda a,b:pt(x+a*w,y+b*h)
 sh=p.new_shape();sh.draw_bezier(P(.12,.74),P(-.08,.5),P(.07,.18),P(.30,.32));sh.draw_bezier(P(.30,.32),P(.29,-.05),P(.76,-.08),P(.74,.31));sh.draw_bezier(P(.74,.31),P(1.04,.12),P(1.14,.76),P(.83,.80));sh.draw_bezier(P(.83,.80),P(.60,.98),P(.25,.95),P(.12,.74));sh.finish(color=stroke,fill=fill,width=lw*SY,closePath=True);sh.commit()
 sh=p.new_shape();sh.draw_bezier(P(.24,.55),P(.40,.27),P(.59,.45),P(.49,.65));sh.draw_bezier(P(.49,.65),P(.40,.8),P(.36,.55),P(.44,.53));sh.finish(color=stroke,width=lw*SY);sh.commit()
def peony(p,x,y,r):
 for k in range(8):
  t=k*math.pi/4;cx=x+math.cos(t)*r*.49;cy=y+math.sin(t)*r*.49
  circle(p,cx,cy,r*.47,(1,.42,.58),(.99,.87,.64),.5)
 for k in range(6):
  t=k*math.pi/3;circle(p,x+math.cos(t)*r*.22,y+math.sin(t)*r*.22,r*.30,(1,.65,.72),CREAM,.4)
 circle(p,x,y,r*.18,(.46,.77,.51),CREAM,.3)
def waves(p,x,y,w,h):
 for j in range(4):
  pts=[]
  for k in range(61):
   xx=k/60; yy=.18+j*.18+math.sin(xx*math.pi*3+j*.6)*.11;pts.append((x+xx*w,y+yy*h))
  poly(p,pts,CREAM,.8)
def lantern(p,x,y,r):
 ellipse(p,x-r*.7,y-r,r*1.4,r*1.6,(.90,.10,.14),GOLD,.5)
 for off in [-.33,0,.33]:ellipse(p,x+off*r-r*.23,y-r,r*.46,r*1.6,None,GOLD,.45)
 line(p,x-r*.36,y-r,x+r*.36,y-r,GOLD,2);line(p,x-r*.30,y+r*.6,x+r*.30,y+r*.6,GOLD,2)
 for off in [-.16,0,.16]:line(p,x+off*r,y+r*.66,x+off*r,y+r*1.23,(.92,.24,.16),.8)
def motif(p,kind,x,y,s):
 if kind==0:peony(p,x,y,s*.42)
 elif kind==1:cloud(p,x-s*.46,y-s*.3,s*.92,s*.62,(.08,.42,.68),CREAM,.8)
 elif kind==2:
  cloud(p,x-s*.43,y-s*.32,s*.86,s*.65,(.12,.48,.69),GOLD,.7);circle(p,x,y,s*.18,(.95,.34,.15),GOLD,.6);circle(p,x,y,s*.09,(.98,.80,.24),CREAM,.5)
 elif kind==3:
  line(p,x,y+s*.12,x,y+s*.48,GOLD,1.5);circle(p,x,y-s*.04,s*.32,(.98,.92,.77),GOLD,.7);peony(p,x,y-s*.04,s*.18)
 elif kind==4:
  ellipse(p,x-s*.47,y-s*.28,s*.94,s*.62,(.10,.45,.65),GOLD,.5);waves(p,x-s*.38,y-s*.22,s*.76,s*.50)
 elif kind in [5,6]:lantern(p,x,y,s*.35)
def pagoda(p,x,y,w,h):
 for k in range(6):
  yy=y+h*(1-k/7);ww=w*(1-k*.10);xx=x+(w-ww)/2
  poly(p,[(xx,yy),(xx+ww*.18,yy-h*.045),(xx+ww*.82,yy-h*.045),(xx+ww,yy)],GOLD,.55)
  line(p,xx+ww*.18,yy-h*.045,xx+ww*.20,yy-h*.105,GOLD,.45);line(p,xx+ww*.82,yy-h*.045,xx+ww*.80,yy-h*.105,GOLD,.45)
  for n in [0.35,.5,.65]:line(p,xx+ww*n,yy-h*.04,xx+ww*n,yy-h*.10,GOLD,.35)
 line(p,x+w*.5,y,x+w*.5,y+h*.12,GOLD,.7)
def deco(p,x,y,w):
 cloud(p,x,y,w*.19,17,None,GOLD,.6);cloud(p,x+w*.75,y-3,w*.23,22,None,GOLD,.6)
 for i in range(3):poly(p,[(x+w*.12,y+13+i*2),(x+w*.36,y+18+i),(x+w*.57,y+11+i),(x+w*.85,y+16+i)],GOLD,.45)
def newpage():
 p=doc.new_page(width=W,height=H);rect(p,0,0,587,887,BLACK);return p

def board1():
 p=newpage();img(p,G/'hero-1.png',0,0,587,344,stretch=True)
 bar(p,15,350,557,'设计理念','01')
 lines=['以泉州布袋戏为灵感，将生、旦、净、末、丑五个行当', '转化为鲜活可亲的角色。提取戏服纹样、花冠、脸谱', '与古厝意象，以青、粉、红、黄、绿建立角色识别。', '让指尖上的传统好戏，成为可收藏、可互动的日常。']
 for j,s in enumerate(lines):txt(p,20,379+j*10.3,s,6.7,WHITE)
 img(p,G/'culture.png',274,371,297,47,clip=(0,175,2184,520),stretch=True)
 for x,s in zip([321,421,523],['偶艺传承','戏服纹样','古厝意象']):txt(p,0,429,s,6.7,CREAM,center=x)
 bar(p,15,432,557,'角色设定','02')
 desc=[('文雅仁厚','才情风度','书生｜正直｜才气'),('婉约灵动','聪慧柔丽','花旦｜灵秀｜机敏'),('刚正勇猛','忠义豪情','武将｜勇猛｜忠义'),('睿智稳重','德高望重','老生｜智慧｜仁德'),('诙谐机智','幽默可爱','丑角｜幽默｜灵动')]
 for i,r in enumerate(ROLES):
  x=16+i*112.8;rect(p,x,453,105,192,PALE[i],COLS[i],.65,radius=.035)
  cloud(p,x+2,459,24,19,None,COLS[i],.45);cloud(p,x+79,560,25,18,None,COLS[i],.4)
  txt(p,0,477,NAMES[i],26,BLACK,'brush',center=x+52.5)
  txt(p,0,489,desc[i][0],8,BLACK,'serif',center=x+52.5);txt(p,0,500,desc[i][1],8,BLACK,'serif',center=x+52.5)
  img(p,A/'5角IP'/f'role-{r}.png',x+2,503,101,126,trim=True)
  rect(p,x+1,629,103,15,BLACK);txt(p,0,639.5,desc[i][2],6.4,WHITE,center=x+52.5)
 micro(p,17,658,'IP 主色彩体系');line(p,110,654,270,654,GOLD,.45)
 for i,c in enumerate(COLS):circle(p,29+i*44,678,15,c,c,.5)
 micro(p,285,658,'元素提取');line(p,332,654,572,654,GOLD,.45)
 for i,label in enumerate(['牡丹花','如意云纹','戏服纹样','团扇纹样','海浪纹','灯穗纹','灯笼纹']):
  cx=304+i*43;motif(p,i,cx,677,32);txt(p,0,701,label,5.7,WHITE,center=cx)
 bar(p,15,706,557,'表情延展','03')
 ex=[['01-生-收到.png','06-生-啊.png','11-生-困了.png'],['02-旦-爱你.png','07-旦-委屈.png','12-旦-害羞.png'],['03-净-气炸了.png','08-净-冲鸭.png','13-净-不服.png'],['04-末-稳住.png','09-末-淡定.png','14-末-妙啊.png'],['05-丑-哈哈哈.png','10-丑-溜了.png','15-丑-略略略.png']]
 for i,r in enumerate(ROLES):
  x=16+i*112.8;rect(p,x,727,105,51,PALE[i],COLS[i],.6,radius=.08);rect(p,x,727,105,12,COLS[i]);txt(p,0,736.5,NAMES[i],10,BLACK,'brush',center=x+52.5)
  for j,f in enumerate(ex[i]):img(p,D/'puppet-stickers-complete'/f,x+2+j*34,739,33,37,trim=True)
 bar(p,15,785,557,'角色海报 / 系列画面','04')
 posters=sorted((A/'邮票海报').glob('*.png'))
 for i,r in enumerate(ROLES):
  x=16+i*112.8;rect(p,x,806,105,76,PALE[i],COLS[i],.5,radius=.03)
  img(p,posters[i],x+1,807,49,74)
  txt(p,0,839,NAMES[i],30,BLACK,'brush',center=x+77)
  for j,s in enumerate(['五角成戏','一角一世界']):txt(p,0,853+j*9,s,6.5,BLACK,center=x+77)
  line(p,x+57,871,x+97,871,COLS[i],1.2)
 return p

def board2():
 p=newpage();img(p,G/'hero-2.png',0,0,587,340,stretch=True)
 bar(p,14,345,285,'品牌视觉系统','01');bar(p,312,345,261,'辅助图形与纹样','02')
 txt(p,15,405,'掌上乾坤',39,CREAM,'brush');txt(p,28,424,'五角成戏 · 泉州布袋戏',7.3,CREAM,'serif')
 for i,c in enumerate(COLS):circle(p,178+i*26,380,9,c,c)
 for j,s in enumerate(['QUANZHOU','GLOVE PUPPET','IP DESIGN']):txt(p,169,414+j*10,s,6.7,CREAM)
 pagoda(p,255,396,31,56);pagoda(p,80,438,23,26);deco(p,16,443,276)
 line(p,304,369,304,464,GOLD,.4)
 for i,label in enumerate(['牡丹纹样','如意云纹','戏服纹样','团扇纹样','海浪纹']):
  x=315+i*52;rect(p,x,369,46,50,[COLS[1],(.05,.43,.64),COLS[2],(.99,.94,.81),(.10,.45,.65)][i],GOLD,.4)
  img(p,G/'patterns.png',x,369,46,50,clip=[(7,131,440,564),(446,131,869,564),(875,131,1299,564),(1304,131,1728,564),(1734,131,2165,564)][i]);txt(p,0,432,label,6.5,WHITE,center=x+23)
 deco(p,316,443,255)
 bar(p,14,469,559,'文创应用 · 日常好物','03')
 img(p,A/'新建文件夹'/'文具系列.png',15,491,322,136)
 img(p,A/'新建文件夹'/'包袋系列.png',344,491,228,136)
 for x,y,s in [(17,491,'文具周边'),(346,491,'随身包袋')]:
  rect(p,x,y,54,14,BLACK,CREAM,.35);txt(p,x+5,y+10,s,7,WHITE)
 micro(p,83,634,'笔记本 · 书签 · 胶带 · 纸品');micro(p,401,634,'帆布包 · 手提袋')
 items=[(15,184,B/'08-product-mockups'/'10-phones.png','数码周边'),(207,184,B/'08-product-mockups'/'07-badges.png','徽章与收藏'),(399,173,A/'新建文件夹'/'家居用品系列.png','家居日用品')]
 for x,w,path,label in items:
  img(p,path,x,642,w,98);rect(p,x+2,644,62,14,BLACK,CREAM,.35);txt(p,x+7,654,label,7,WHITE)
 bar(p,14,748,325,'APP 界面设计','04');bar(p,350,748,223,'品牌包装系统','05')
 app=A/'展板'/'ChatGPT 图像 2026年10月28日 13_11_11.png'
 # Complete phone silhouettes, separated from the supplied presentation background.
 xs=[(17,139,374,856),(377,139,715,856),(718,139,1052,856),(1056,139,1396,856),(1399,139,1758,856)]
 rect(p,17,768,45,98,CREAM,CREAM,.7,radius=.12);rect(p,30,771,19,3,BLACK,radius=.45)
 txt(p,0,809,'掌上',16,BLACK,'brush',center=39.5);txt(p,0,828,'乾坤',16,BLACK,'brush',center=39.5)
 cloud(p,25,837,29,17,None,GOLD,.7)
 txt(p,0,879,'启动页',6.2,WHITE,center=39.5)
 labels=['首页','角色介绍','角色详情','戏台互动','我的收藏']
 for i,crop in enumerate(xs):
  x=69+i*54;img(p,app,x,768,47,98,clip=crop);txt(p,0,879,labels[i],6.2,WHITE,center=x+23.5)
 img(p,G/'packaging.png',350,769,223,111)
 return p

def board3():
 p=newpage();img(p,G/'hero-3.png',0,0,587,357,stretch=True)
 bar(p,10,359,563,'盲盒手办系列','01');txt(p,146,373,'五款角色 · 匠心打造 · 收藏经典',7,CREAM)
 img(p,G/'keychains.png',5,383,189,126,trim=True)
 bar(p,202,390,370,'文创周边','02')
 panels=[(203,123,A/'新建文件夹'/'包袋系列.png','随行包袋'),(333,114,B/'08-product-mockups'/'07-badges.png','金属徽章'),(454,118,D/'ip-complete'/'03-magnets.png','角色冰箱贴')]
 for x,w,path,label in panels:
  img(p,path,x,412,w,82);txt(p,0,505,label,7,WHITE,center=x+w/2)
 bar(p,10,516,254,'手工 DIY 礼盒','03');bar(p,275,516,298,'贴纸与纸制品','04')
 img(p,A/'展板'/'ChatGPT 图像 2026年10月28日 13_00_25.png',10,537,254,153)
 img(p,A/'展板'/'ChatGPT 图像 2026年10月28日 12_38_06.png',275,540,298,149)
 # Short readable labels replace the low-resolution placeholder copy in reference.
 txt(p,0,702,'布袋戏手作套装 · 一起动手做场好戏',7,CREAM,center=137)
 for x,s in zip([313,422,535],['贴纸套装','明信片','收藏卡']):txt(p,0,702,s,7,CREAM,center=x)
 bar(p,10,711,563,'线下体验装置 · 泉州古城闪现','05')
 img(p,A/'展板'/'03-商场中庭.png',10,733,286,129)
 img(p,A/'展板'/'04-滨水夜游.png',304,733,269,129)
 # Condensed captions sit directly below the full scenes, without covering any subject.
 rect(p,10,865,286,21,BLACK);rect(p,304,865,269,21,BLACK)
 txt(p,13,874,'城市会客厅 · 主题互动装置',7,CREAM);txt(p,13,884,'让非遗走进生活，与更多人相遇。',6.1,WHITE)
 txt(p,307,874,'滨水夜游 · 沉浸式打卡体验',7,CREAM);txt(p,307,884,'在光影与戏韵中，感受泉州的温度。',6.1,WHITE)
 return p

if __name__=='__main__':
 board1();board2();board3()
 doc.rewrite_images(dpi_threshold=450,dpi_target=400,quality=96);pdf=OUT/'五角成戏-A3三张展板-模板重排.pdf';doc.save(pdf,garbage=4,deflate=True)
 for i,p in enumerate(doc):
  name=f'0{i+1}-'+['掌上乾坤','好戏入日常','把好戏带回家'][i]
  pix=p.get_pixmap(matrix=fitz.Matrix(300/72,300/72),alpha=False);pix.set_dpi(300,300);pix.save(OUT/(name+'-A3.png'))
  pix=p.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False);pix.save(OUT/(name+'-预览.png'))
  print(name,'A3',p.rect,flush=True)
 (OUT/'素材清晰度记录.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
 print('PDF MB',pdf.stat().st_size/1024**2)

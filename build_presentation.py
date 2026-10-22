from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_THEME_COLOR
from PIL import Image


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets'
OUT = ROOT / 'quanzhou_puppet_show.pptx'
TOTAL = 35
CHAR = ASSETS / 'ip_sheng.png'
ROLE_FILES = [
    ASSETS / 'ip_sheng.png',
    ASSETS / 'ip_dan.png',
    ASSETS / 'ip_jing.png',
    ASSETS / 'ip_mo.png',
    ASSETS / 'ip_chou.png',
]
MOTIFS = ASSETS / '01_role_motifs.png'
CITY = ASSETS / '02_quanzhou_cityscape.png'
PAPER = ASSETS / '03_full_bookmarks.png'
STAMPS = ASSETS / '08_full_stamps.png'
ACCESSORIES = ASSETS / '04_full_keychains.png'
SACHETS = ASSETS / '09_costume_sachets.png'
MIRRORS = ASSETS / '10_costume_mirrors.png'
FIGURINES = ASSETS / '05_figurines.png'
BAGS = ASSETS / '06_full_tote_bags.png'
EXHIBIT = ASSETS / '07_exhibition_mockup.png'
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
W, H = 13.333, 7.5

BG = '#08090D'
PINK = '#FF4B9E'
TEAL = '#4CE3D0'
YELLOW = '#FFE46A'
PURPLE = '#A064FF'
BLUE = '#58A9FF'
ORANGE = '#FF954C'
WHITE = '#F8F6F6'
MUTED = '#A7A6AF'
CARD = '#14151E'
STROKE = '#393844'
ROLE_NAMES = ['生', '旦', '净', '末', '丑']
ROLE_COLOR = [TEAL, PINK, ORANGE, BLUE, YELLOW]
ROLE_EN = ['SHENG', 'DAN', 'JING', 'MO', 'CHOU']
FONT = 'Noto Sans CJK SC'


def I(n): return Inches(n)
def C(h): return RGBColor.from_string(h.replace('#', ''))


def slide(bg=BG):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = C(bg)
    return s


def box(s, x, y, w, h, fill=CARD, line=None, radius=False, lw=1):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE, I(x), I(y), I(w), I(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = C(fill)
    if line:
        sh.line.color.rgb = C(line); sh.line.width = Pt(lw)
    else: sh.line.fill.background()
    if radius:
        try: sh.adjustments[0] = 0.09
        except Exception: pass
    return sh


def circle(s,x,y,d,fill,line=None,lw=1):
    sh=s.shapes.add_shape(MSO_SHAPE.OVAL,I(x),I(y),I(d),I(d))
    sh.fill.solid(); sh.fill.fore_color.rgb=C(fill)
    if line: sh.line.color.rgb=C(line); sh.line.width=Pt(lw)
    else: sh.line.fill.background()
    return sh


def txt(s, text, x,y,w,h, size=20, color=WHITE, bold=False, align='left', font=FONT, valign='mid', margin=0.02, spacing=1.0):
    sh=s.shapes.add_textbox(I(x),I(y),I(w),I(h))
    tf=sh.text_frame; tf.clear(); tf.word_wrap=True
    tf.margin_left=tf.margin_right=I(margin); tf.margin_top=tf.margin_bottom=I(margin)
    tf.vertical_anchor={'top':MSO_ANCHOR.TOP,'mid':MSO_ANCHOR.MIDDLE,'bottom':MSO_ANCHOR.BOTTOM}[valign]
    for j,line in enumerate(text.split('\n')):
        p=tf.paragraphs[0] if j==0 else tf.add_paragraph()
        p.text=line
        p.alignment={'left':PP_ALIGN.LEFT,'center':PP_ALIGN.CENTER,'right':PP_ALIGN.RIGHT}[align]
        p.space_before=Pt(0); p.space_after=Pt(0)
        p.line_spacing=spacing
        for r in p.runs:
            r.font.name=font; r.font.size=Pt(size); r.font.bold=bold; r.font.color.rgb=C(color)
    return sh


def rule(s,x,y,w,color=PINK,h=0.025): box(s,x,y,w,h,color)


def flower(s,cx,cy,r=0.34,color=PINK,center=YELLOW,petals=8):
    import math
    for j in range(petals):
        a=2*math.pi*j/petals
        px=cx+math.cos(a)*r*.62-r*.28
        py=cy+math.sin(a)*r*.62-r*.28
        sh=s.shapes.add_shape(MSO_SHAPE.OVAL,I(px),I(py),I(r*.56),I(r*.56))
        sh.fill.solid(); sh.fill.fore_color.rgb=C(color); sh.line.fill.background()
    circle(s,cx-r*.2,cy-r*.2,r*.4,center)


def medallion(s,cx,cy,d=1.05,colors=(PINK,TEAL,YELLOW)):
    circle(s,cx-d/2,cy-d/2,d,BG,colors[0],2)
    flower(s,cx,cy,d*.32,colors[0],colors[2])
    circle(s,cx-d*.23,cy-d*.23,d*.46,BG,colors[1],1.5)
    circle(s,cx-d*.055,cy-d*.055,d*.11,colors[2])


def role(s,idx,x,y,w,h):
    # Complete, separate cutouts avoid clipping sleeves and props at the
    # boundaries of the five-character source strip.
    return photo(s,ROLE_FILES[idx],x,y,w,h)


def photo(s,path,x,y,w,h):
    """Place an image inside a box without distorting or cropping its design."""
    iw,ih=Image.open(path).size
    ar=iw/ih
    ww=min(w,h*ar); hh=ww/ar
    if hh>h: hh=h; ww=h*ar
    return s.shapes.add_picture(str(path),I(x+(w-ww)/2),I(y+(h-hh)/2),I(ww),I(hh))


def photo_crop(s,path,x,y,w,h,left=0,top=0,right=0,bottom=0):
    pic=s.shapes.add_picture(str(path),I(x),I(y),I(w),I(h))
    pic.crop_left=left; pic.crop_top=top; pic.crop_right=right; pic.crop_bottom=bottom
    return pic


def motif(s,idx,x,y,w,h):
    """Editable symbols redrawn from marks on the five characters' garments."""
    d=min(w,h)*.66; cx=x+w/2; cy=y+h/2
    fills=[TEAL,PINK,PURPLE,BLUE,'#51B85C']
    circle(s,cx-d/2,cy-d/2,d,fills[idx],YELLOW,2)
    if idx in (0,2,3):
        # Scrolled clouds on Sheng's robe, Jing's apron and Mo's hem.
        cc=[YELLOW,ORANGE,TEAL][[0,2,3].index(idx)]
        for dx,dy,r in [(-.21,.01,.30),(0,-.10,.39),(.22,.01,.30)]:
            circle(s,cx+d*dx-d*r/2,cy+d*dy-d*r/2,d*r,cc)
        for dx,dy,r in [(-.20,.035,.17),(0,-.065,.22),(.22,.035,.17)]:
            circle(s,cx+d*dx-d*r/2,cy+d*dy-d*r/2,d*r,fills[idx])
        rule(s,cx-d*.29,cy+d*.17,d*.58,cc,d*.045)
    else:
        import math
        petal=YELLOW if idx==4 else '#FFE2EA'
        for j in range(5):
            a=2*math.pi*j/5-math.pi/2
            circle(s,cx+math.cos(a)*d*.21-d*.15,cy+math.sin(a)*d*.21-d*.15,d*.30,petal)
        circle(s,cx-d*.11,cy-d*.11,d*.22,ORANGE if idx==4 else PINK)


def costume_detail(s,idx,region,x,y,w,h):
    """Crop only in PowerPoint: preserve the supplied complete role image file."""
    p=ROLE_FILES[idx]; iw,ih=Image.open(p).size
    x0,y0,x1,y1=region
    pic=s.shapes.add_picture(str(p),I(x),I(y),I(w),I(h))
    pic.crop_left=x0/iw; pic.crop_top=y0/ih
    pic.crop_right=(iw-x1)/iw; pic.crop_bottom=(ih-y1)/ih
    return pic


def base(title,num,tag=None):
    s=slide()
    rule(s,.42,.30,12.49,'#49444F',.012)
    txt(s,title,.43,.42,10.7,.46,22,WHITE,True)
    rule(s,.43,1.03,.32,PINK,.055); rule(s,.79,1.03,.2,TEAL,.055)
    if tag: txt(s,tag,9.4,.45,3.4,.3,9,MUTED,align='right')
    txt(s,f'{len(prs.slides):02d} / {TOTAL}',11.82,7.07,1.05,.22,9,MUTED,align='right')
    return s


def divider(n,title,subtitle,idx,color):
    s=slide(); rule(s,.42,.32,12.5,'#46414B',.012)
    txt(s,f'{n:02d}',.43,.62,2.4,1.4,66,color,True)
    txt(s,title,2.05,1.49,8.9,1.6,37,WHITE,True,spacing=1.14)
    txt(s,subtitle,2.1,3.23,7.2,.45,12,MUTED)
    role(s,idx,.47,3.47,2.56,3.65)
    medallion(s,10.84,1.23,1.25,(color,TEAL,YELLOW))
    medallion(s,11.64,5.66,.95,(PINK,PURPLE,YELLOW))
    medallion(s,8.36,6.64,1.2,(TEAL,ORANGE,YELLOW))
    return s


def card(s,x,y,w,h,title,body,color=PINK,icon=None):
    box(s,x,y,w,h,CARD,STROKE,True)
    rule(s,x+.19,y+.18,.45,color,.06)
    if icon: txt(s,icon,x+w-.86,y+.08,.65,.6,32,color,True,align='center')
    txt(s,title,x+.2,y+.46,w-.4,.48,19,color,True)
    txt(s,body,x+.2,y+1.06,w-.4,h-1.20,14,WHITE,valign='top',spacing=1.20)


# 01 Cover
s=slide()
medallion(s,.72,.36,1.1,(PINK,TEAL,YELLOW))
medallion(s,12.25,.51,.92,(PURPLE,ORANGE,YELLOW))
medallion(s,11.55,6.42,1.28,(TEAL,PINK,YELLOW))
txt(s,'掌上乾坤',2.3,.47,8.7,.83,44,YELLOW,True,align='center')
txt(s,'泉州布袋戏',2.13,1.28,9.1,.85,46,PINK,True,align='center')
txt(s,'QUANZHOU GLOVE PUPPET THEATRE · CULTURAL CREATIVE DESIGN',2.1,2.13,9.2,.3,12,WHITE,align='center')
rule(s,5.42,2.52,2.5,TEAL,.04)
for i in range(5): role(s,i,.24+i*2.61,2.98,2.55,3.82)
txt(s,'生',.34,6.73,2.15,.45,23,TEAL,True,align='center')
for i,c in enumerate([PINK,ORANGE,BLUE,YELLOW],1): txt(s,ROLE_NAMES[i],.34+i*2.61,6.73,2.15,.45,23,c,True,align='center')

# 02 Contents
s=slide(); txt(s,'目录',.5,.47,2.1,.6,31,PINK,True)
txt(s,'CONTENTS',2.18,.56,3.0,.32,19,'#393942',True)
rule(s,.5,1.12,12.2,'#3E3B46',.015)
sections=[('01','创意溯源','与文化背景',PINK),('02','核心视觉设计','与规范',TEAL),('03','文创衍生品','开发应用',PURPLE),('04','展板设计','与成果展示',BLUE)]
for i,(n,a,b,c) in enumerate(sections):
    x=.58+i*3.12
    txt(s,n,x,2.32,2.8,.9,42,c,True)
    txt(s,a+'\n'+b,x,3.5,2.7,1.2,22,WHITE,True,spacing=1.2)
    rule(s,x,5.18,2.48,c,.025)
for i in range(5): role(s,i,.55+i*.92,5.55,.94,1.45)
medallion(s,11.82,5.53,.8,(PINK,TEAL,YELLOW))

# 03 Divider
divider(1,'创意溯源\n与文化背景','FROM FOLK STAGE TO CONTEMPORARY DESIGN',1,PINK)

# 04 Historical overview
s=base('历史背景介绍',4,'01 / 文化脉络')
txt(s,'一方小戏台，一手演乾坤',.6,1.36,6.7,.65,29,PINK,True)
txt(s,'布袋木偶戏流传于闽南地区。艺人将手伸入布偶的衣身，以手指操控头部与双臂，让木刻偶头、布制服饰和细腻动作在小戏台上相遇。',.64,2.18,6.15,1.32,18,WHITE,valign='top',spacing=1.22)
txt(s,'演出常以闽南语唱白、锣鼓节奏与戏曲程式推进情节，既能表现忠义豪情，也能讲述市井生活与民间趣事。',.64,3.78,6.15,1.21,18,WHITE,valign='top',spacing=1.22)
box(s,.63,5.48,6.18,.8,'#1F1624',PINK,True)
txt(s,'设计切入点：以五个行当角色与泉州城市意象，构成“掌中戏”的年轻表达。',.84,5.65,5.75,.46,15,PINK,True)
role(s,2,8.0,1.45,3.35,5.24)
medallion(s,11.62,2.03,.82,(PINK,TEAL,YELLOW))

# How a glove puppet is operated: a conceptual diagram, not a historic replica.
s=base('布袋偶操演方式',5,'01 / 文化依据')
txt(s,'一只手，带动一出戏',.58,1.30,7.6,.64,29,PINK,True)
txt(s,'操演原理示意 · 非传统戏偶实物复原',.60,1.97,7.0,.35,14,MUTED)
box(s,.58,2.47,6.18,3.92,CARD,STROKE,True)
circle(s,2.62,2.68,1.68,'#F7E4CF',YELLOW,2)
box(s,2.31,4.21,2.29,1.70,PINK,YELLOW,True,1.5)
box(s,1.50,4.50,.95,.69,PINK,YELLOW,True,1.3)
box(s,4.45,4.50,.95,.69,PINK,YELLOW,True,1.3)
circle(s,1.30,4.42,.54,'#F7E4CF')
circle(s,5.18,4.42,.54,'#F7E4CF')
circle(s,3.16,5.66,.56,TEAL)
txt(s,'食指 → 偶头',.79,2.85,1.65,.40,16,YELLOW,True)
txt(s,'拇指 → 左臂',.72,5.43,1.72,.40,16,TEAL,True)
txt(s,'中指 → 右臂',4.70,5.43,1.80,.40,16,TEAL,True)
txt(s,'手掌进入衣身',2.28,6.01,2.55,.29,13,WHITE,align='center')
box(s,7.09,2.47,5.62,3.92,CARD,STROKE,True)
for j,(a,b,c) in enumerate([
    ('结构','偶头、衣身和双臂构成可操控的表演体。',PINK),
    ('动作','手指驱动转头、挥袖与举手等动作。',TEAL),
    ('转译','IP 保留冠帽、脸谱与衣纹，展示为完整角色。',YELLOW)]):
    yy=2.77+j*1.13
    circle(s,7.38,yy,.53,c)
    txt(s,str(j+1),7.39,yy+.02,.50,.43,16,BG,True,align='center')
    txt(s,a,8.12,yy-.02,1.08,.38,18,c,True)
    txt(s,b,9.10,yy-.06,3.24,.78,15,WHITE,valign='top')
txt(s,'本项目是泉州城市文创概念设计；角色插画不指代具体传统剧目或馆藏戏偶。',.70,6.69,11.80,.33,12,MUTED,align='center')

# 05 Concept
s=base('选题介绍',5,'01 / 项目背景')
card(s,.53,1.55,3.9,4.46,'项目背景','城市文化与文旅体验不断融合，传统戏曲需要更鲜明、轻盈的视觉入口，让初次接触的观众愿意驻足与了解。',PINK,'01')
card(s,4.71,1.55,3.9,4.46,'设计说明','提取木偶的冠帽、脸谱、衣饰和表演姿态，转化为五位可辨认的国潮角色，并延展到日常文创载体。',TEAL,'02')
card(s,8.89,1.55,3.9,4.46,'设计理念','以“五角成戏”为核心，让收藏、使用和分享成为走近掌中戏文化的连续体验。',YELLOW,'03')
txt(s,'文化识别 → 角色共鸣 → 场景使用 → 自发传播',2.24,6.38,8.87,.45,17,WHITE,True,align='center')

# 06 Audience
s=base('受众人群与使用场景',6,'01 / 目标人群')
card(s,.53,1.58,3.9,4.64,'泉州游客','希望带走轻便、具有地方辨识度的纪念品。\n\n场景：景区、博物馆、古城街巷。',PINK)
card(s,4.71,1.58,3.9,4.64,'青年与亲子','偏好角色故事、成套收藏和互动体验。\n\n场景：研学课堂、社交分享、礼赠。',TEAL)
card(s,8.89,1.58,3.9,4.64,'文旅机构','需要能够代表在地文化、方便陈列与传播的系列礼品。\n\n场景：展演活动、城市礼物、公共教育。',PURPLE)
txt(s,'接触戏偶 → 认识行当 → 收集角色 → 分享泉州故事',1.73,6.55,9.9,.38,16,WHITE,True,align='center')

# 07 Reference style
s=base('参考风格',7,'01 / 风格定位')
txt(s,'统一新中式国潮风格',.57,1.48,7.1,.65,31,WHITE,True)
txt(s,'高饱和撞色 · 扁平插画 · 戏台层次 · 纹样点缀',.58,2.18,9.7,.39,17,TEAL,True)
box(s,.53,2.91,12.28,3.64,CARD,STROKE,True)
for i in range(5):
    x=.79+i*2.42
    role(s,i,x,3.15,1.9,2.85)
    txt(s,ROLE_NAMES[i],x,6.04,1.9,.32,18,ROLE_COLOR[i],True,align='center')

# 08 Inspirations
s=base('灵感创意来源',8,'01 / 元素提取')
sources=[('冠帽','角色身份的第一眼线索',PINK),('脸谱','净角的性格张力',ORANGE),('衣纹','闽南戏曲的装饰节奏',TEAL),('戏台','框景与层叠的表演空间',PURPLE)]
for i,(a,b,c) in enumerate(sources):
    x=.57+(i%2)*6.2; y=1.54+(i//2)*2.44
    box(s,x,y,5.94,2.12,CARD,STROKE,True)
    medallion(s,x+.72,y+1.06,.9,(c,TEAL,YELLOW))
    txt(s,a,x+1.45,y+.43,4.1,.5,22,c,True)
    txt(s,b,x+1.45,y+1.07,4.04,.5,15,WHITE)
txt(s,'不是复制传统戏偶，而是将其可识别的视觉语言转化为当代设计。',1.65,6.72,10.2,.38,15,MUTED,align='center')

# 09 Divider
divider(2,'核心视觉设计\n与规范','CHARACTER SYSTEM · COLOR · ORNAMENT',2,TEAL)

# 10 Core characters
s=base('核心主体视觉元素设计',10,'02 / 五角成戏')
for i in range(3):
    x=.58+i*4.27
    box(s,x,1.39,3.79,5.50,CARD,STROKE,True)
    role(s,i,x+.14,1.59,3.52,4.15)
    box(s,x+.34,5.73,3.11,.53,ROLE_COLOR[i],None,True)
    txt(s,ROLE_NAMES[i]+'  '+ROLE_EN[i],x+.35,5.80,3.08,.35,17,BG,True,align='center')
    desc=['文雅机敏，启幕引戏','柔美灵动，以情动人','浓墨重彩，气势如虹'][i]
    txt(s,desc,x+.24,6.46,3.35,.31,14,WHITE,align='center')

# Full figures enlarged on two consecutive slides while retaining all five.
s=base('核心主体视觉元素设计（续）',11,'02 / 五角成戏')
for j,i in enumerate([3,4]):
    x=1.13+j*6.05
    box(s,x,1.41,5.05,5.48,CARD,STROKE,True)
    role(s,i,x+.30,1.56,4.45,4.25)
    box(s,x+.83,5.77,3.38,.52,ROLE_COLOR[i],None,True)
    txt(s,ROLE_NAMES[i]+'  '+ROLE_EN[i],x+.85,5.82,3.34,.36,18,BG,True,align='center')
    txt(s,['沉稳慈和，阅尽世情','诙谐俏皮，点亮戏台'][j],x+.38,6.47,4.30,.31,15,WHITE,align='center')

# 11 Colors
s=base('色彩搭配',11,'02 / 角色色谱')
colors=[('#FF4B9E','胭脂粉'),('#4CE3D0','海丝青'),('#FFE46A','戏台金'),('#A064FF','华彩紫'),('#58A9FF','靛蓝'),('#FF954C','朱橘'),('#F8F6F6','纸白'),('#14151E','幕黑')]
for i,(c,n) in enumerate(colors):
    x=.52+i*1.55
    box(s,x,1.71,1.30,3.58,c)
    txt(s,c,x,5.40,1.3,.35,12,WHITE,True,align='center')
    txt(s,n,x,5.87,1.3,.37,15,WHITE,align='center')
txt(s,'从戏服与脸谱提取高饱和色彩，以黑色戏幕衬托角色；色彩随角色切换，系统保持统一。',.63,6.61,11.77,.44,15,MUTED)

# 12 Motifs
s=base('辅助图形设计',12,'02 / 纹样系统')
txt(s,'五角五纹 · 只从五位人物的衣服图案提取',.61,1.35,11.68,.5,19,PINK,True)
for i,(a,b) in enumerate([('青衣云纹','生'),('粉袖花纹','旦'),('紫袍云纹','净'),('蓝袍云浪','末'),('绿衣团花','丑')]):
    x=.43+i*2.56
    motif(s,i,x,2.09,2.43,3.61)
    txt(s,a,x+.04,5.70,2.34,.47,17,ROLE_COLOR[i],True,align='center')
    txt(s,b,x+.34,6.17,1.74,.35,13,WHITE,align='center')
txt(s,'纹样可独立用于印章、挂件、香囊与包装，也可与人物形象组合。',.75,6.72,11.85,.35,14,MUTED,align='center')

# Evidence of the actual costume-to-graphic extraction.
s=base('衣纹提取过程',14,'02 / 图形推导')
txt(s,'从衣服局部到可复用的辅助图形',.63,1.29,9.3,.55,26,PINK,True)
txt(s,'原服饰局部',.86,1.98,2.15,.37,15,WHITE,True,align='center')
txt(s,'提炼动作',4.50,1.98,2.0,.37,15,WHITE,True,align='center')
txt(s,'辅助图形',8.97,1.98,2.2,.37,15,WHITE,True,align='center')
regions=[(400,895,790,1105),(395,725,605,900),(525,855,795,1085),(270,1000,560,1185),(305,655,475,830)]
steps=['保留金色三瓣云头','提炼五瓣花心与瓣形','简化裙甲上的团云','抽取下摆云浪曲线','保留绿衣上的五瓣花']
for i in range(5):
    yy=2.43+i*.79
    box(s,.66,yy,12.0,.73,CARD,STROKE,True)
    box(s,.83,yy+.07,1.28,.59,'#22232B',ROLE_COLOR[i],True)
    costume_detail(s,i,regions[i],.84,yy+.075,1.25,.58)
    txt(s,ROLE_NAMES[i],2.28,yy+.17,.43,.34,17,ROLE_COLOR[i],True,align='center')
    txt(s,'→',3.46,yy+.13,.5,.39,20,TEAL,True,align='center')
    txt(s,steps[i],4.04,yy+.13,3.47,.42,17,WHITE,align='center')
    txt(s,'→',7.56,yy+.13,.5,.39,20,TEAL,True,align='center')
    motif(s,i,8.14,yy+.02,1.02,.69)
    txt(s,['青衣云纹','粉袖花纹','紫袍云纹','蓝袍云浪','绿衣团花'][i],9.46,yy+.15,2.78,.37,16,ROLE_COLOR[i],True)
txt(s,'取形、简线、统一边框；不使用扇面竹叶、头饰或手持道具作为衣纹来源。',.73,6.64,11.93,.34,13,MUTED,align='center')

# 13 Auxiliary elements
s=base('辅助元素展示',13,'02 / 版式语言')
for x,w in [(.51,3.85),(4.48,5.25),(9.85,2.97)]: box(s,x,1.62,w,3.97,'#101117',STROKE,False)
txt(s,'掌上乾坤',.70,2.25,3.47,.78,32,YELLOW,True,align='center')
txt(s,'泉州布袋戏',.69,3.15,3.5,.71,29,PINK,True,align='center')
rule(s,1.26,4.19,2.38,TEAL,.07)
photo(s,CITY,4.55,2.0,5.1,3.23)
box(s,10.47,2.3,1.71,1.71,BG,PINK,False,2.3)
box(s,10.62,2.45,1.41,1.41,BG,PINK,False,1.1)
txt(s,'泉州\n布袋',10.73,2.69,1.19,.99,23,PINK,True,align='center',spacing=.92)
for x,a,c in [(.74,'主标题',YELLOW),(5.85,'泉州城市插画',TEAL),(10.2,'篆刻印章',PINK)]: txt(s,a,x,5.84,2.5,.44,17,c,True,align='center')
txt(s,'字体与标识保持可编辑；城市插画融合东西塔、红砖古厝、海丝帆船与戏台。',.69,6.62,11.93,.52,15,WHITE,align='center')

# 14 Divider
divider(3,'文创衍生品\n开发应用','FROM CHARACTER TO EVERYDAY OBJECT',0,PURPLE)

# 15 Product map
s=base('产品延展',15,'03 / 文创矩阵')
items=[('纸品系列','书签 / 明信片 / 邮票','轻便收藏，传递角色故事',PINK),('随身系列','钥匙扣 / 香囊 / 帆布袋','让戏偶融入日常出行',TEAL),('收藏系列','角色摆件 / 盲盒包装','建立五角成套的收藏体验',PURPLE),('展陈系列','角色立牌 / 展板 / 礼盒','适用于文旅空间与研学活动',YELLOW)]
for i,(a,b,c,d) in enumerate(items):
    x=.58+(i%2)*6.18; y=1.56+(i//2)*2.44
    box(s,x,y,5.92,2.19,CARD,STROKE,True)
    txt(s,a,x+.24,y+.28,5.25,.42,22,d,True)
    txt(s,b,x+.24,y+.9,5.25,.36,16,WHITE,True)
    txt(s,c,x+.24,y+1.51,5.32,.38,14,MUTED)

# 16 Bookmarks and postcards
s=base('设计延展 —— 角色书签',16,'03 / 纸品系列')
photo(s,PAPER,.66,1.47,12.0,5.16)
txt(s,'一角一签：完整人物与衣饰纹样组合成系列纸品，可独立收藏，也可成套陈列。',.79,6.63,11.75,.35,15,WHITE,align='center')

# 17 Sachet
s=base('设计延展 —— 香囊设计',17,'03 / 随身系列')
photo_crop(s,SACHETS,.66,1.60,12.0,4.85,top=.12,bottom=.16)
txt(s,'香囊展示五角色系列配色；量产图形以衣纹提取页的五款辅助图形为准。',1.0,6.51,11.33,.40,16,WHITE,align='center')

# 18 Stamps
s=base('设计延展 —— 邮票设计',18,'03 / 纸品系列')
photo(s,STAMPS,.65,1.47,12.05,5.13)
txt(s,'五枚邮票均保留人物从冠帽到鞋履的完整形象，并以衣饰纹样作边框。',.95,6.63,11.36,.35,15,WHITE,align='center')

# 19 Display figurines
s=base('设计延展 —— 桌面角色摆件',19,'03 / 收藏系列')
photo(s,FIGURINES,.53,1.40,12.24,5.57)
txt(s,'五角成套收藏，底座延续各角色的专属辅助纹样。',1.43,6.76,10.57,.35,14,MUTED,align='center')

# 20 Keychains
s=base('设计延展 —— 角色钥匙扣',20,'03 / 随身系列')
photo(s,ACCESSORIES,.67,1.47,12.0,5.16)
txt(s,'完整人物挂件配套衣饰纹样小牌与流苏，适合单件购买或成套礼赠。',.82,6.62,11.8,.35,15,WHITE,align='center')

# 21 Tote bags
s=base('设计延展 —— 帆布袋',21,'03 / 随身系列')
photo(s,BAGS,.67,1.43,12.0,5.14)
txt(s,'五款帆布袋完整呈现人物，从帽饰、衣袖到鞋履均保留在图案内。',1.16,6.61,11.0,.34,15,WHITE,align='center')

# 22 Collection
s=base('设计延展 —— 随身镜与系列礼盒',22,'03 / 礼赠系列')
photo_crop(s,MIRRORS,.64,1.72,12.0,4.46,top=.14,bottom=.20)
txt(s,'随身镜外壳使用五款衣饰辅助纹样；可与书签、挂件组合为「五角成戏」礼盒。',.80,6.38,11.76,.51,16,WHITE,align='center')

# Specifications for two products that can be quoted and prototyped.
s=base('重点文创打样规范',24,'03 / 工艺方案')
txt(s,'从效果图进入打样：先确认尺寸、材质与图案边界',.59,1.34,11.82,.51,24,PINK,True)
specs=[
    ('角色书签','55 × 160 mm','350 g 铜版卡 / 哑膜','四色印刷、圆角、4 mm 穿孔','人物完整留边 ≥ 5 mm；检查挂绳与孔位',TEAL),
    ('衣纹香囊','85 × 110 mm','棉布外袋 / 独立内袋','数码印花、车缝、抽绳封口','衣纹居中；先做洗涤与色牢度样',PINK),
]
for i,(name,dim,mat,craft,note,color) in enumerate(specs):
    x=.62+i*6.18
    box(s,x,2.08,5.88,4.62,CARD,color,True,1.4)
    txt(s,name,x+.27,2.35,5.31,.53,27,color,True)
    for j,(k,v) in enumerate([('建议尺寸',dim),('材料',mat),('制作工艺',craft),('打样检查',note)]):
        yy=3.10+j*.78
        txt(s,k,x+.30,yy,1.30,.38,14,MUTED,True)
        txt(s,v,x+1.54,yy-.03,3.99,.55,16,WHITE)
txt(s,'以上为设计规格建议，尚未取得供应商报价或实物打样；产品页为效果图。',.79,6.88,11.65,.27,12,MUTED,align='center')

# 23 Exhibition overview
s=base('展板设计',23,'03 / 空间展示')
for i,(title,color) in enumerate([('文化溯源',PINK),('五角成戏',TEAL),('文创应用',PURPLE)]):
    x=.52+i*4.24
    box(s,x,1.58,3.82,5.15,BG,color,False,1.3)
    rule(s,x+.21,1.87,3.40,color,.06)
    txt(s,title,x+.22,2.08,3.33,.48,23,color,True)
    if i==0:
        photo(s,CITY,x+.15,2.81,3.50,1.52)
        txt(s,'指尖之间，山海入戏',x+.28,4.52,3.22,.46,17,WHITE,True,align='center')
        role(s,0,x+1.13,5.04,1.53,1.41)
    elif i==1:
        for j in range(5): role(s,j,x+.12+j*.71,2.92,.70,2.18)
        for j in range(5): motif(s,j,x+.18+j*.69,5.09,.68,.98)
        txt(s,'人物 × 衣饰纹样',x+.28,6.20,3.20,.30,14,WHITE,align='center')
    else:
        photo(s,PAPER,x+.12,2.75,3.59,1.76)
        photo(s,SACHETS,x+.12,4.51,3.59,1.75)
        txt(s,'从戏台走入生活',x+.21,6.24,3.40,.30,14,WHITE,align='center')

# 24 Divider
divider(4,'展板设计\n与成果展示','EXHIBITION · PRESENTATION · APPLICATION',4,YELLOW)

# 25 Board one
s=slide(); rule(s,.55,.42,12.24,PINK,.045)
txt(s,'掌上乾坤  /  泉州布袋戏',.60,.62,7.8,.43,18,PINK,True)
txt(s,'掌中有戏，指尖传情',.61,1.31,7.29,.78,36,WHITE,True)
txt(s,'布袋木偶由偶头、织物衣身与双臂组成；艺人以手指驱动转头、挥袖和举手，让小戏台容纳鲜活的故事。',.65,2.34,5.18,1.29,19,WHITE,valign='top',spacing=1.2)
rule(s,.66,4.11,4.86,TEAL,.045)
for j,(a,b) in enumerate([('一只手','操演动作'),('一方台','凝聚故事'),('一座城','展开想象')]):
    x=.67+j*1.87
    txt(s,a,x,4.35,1.69,.39,20,TEAL,True)
    txt(s,b,x,4.80,1.69,.34,14,MUTED)
photo(s,CITY,5.52,1.69,7.13,3.65)
role(s,0,9.12,4.12,3.10,2.77)
txt(s,'泉州城市意象：东西塔 · 红砖古厝 · 海丝帆船',.68,6.45,8.47,.37,15,YELLOW,True)
txt(s,'城市文创概念设计 · 非传统戏偶实物复原',.67,6.95,8.49,.27,10,MUTED)

# 26 Board two
s=slide(); rule(s,.55,.42,12.24,TEAL,.045)
txt(s,'掌上乾坤  /  五角成戏',.60,.62,7.8,.43,18,TEAL,True)
txt(s,'一眼识五角',.61,1.26,4.86,.76,36,WHITE,True)
txt(s,'生 · 旦 · 净 · 末 · 丑',8.21,1.48,4.43,.45,18,YELLOW,True,align='right')
for i in range(5):
    x=.37+i*2.59
    box(s,x,2.15,2.43,4.50,CARD,ROLE_COLOR[i],True,.9)
    role(s,i,x+.04,2.29,2.35,2.77)
    motif(s,i,x+.65,5.00,1.13,1.11)
    txt(s,ROLE_NAMES[i],x+.54,6.20,1.37,.32,17,ROLE_COLOR[i],True,align='center')
txt(s,'五位人物均以完整形象展示；下方图形只从各自的衣服纹样提炼。',.62,6.94,12.06,.32,13,MUTED,align='center')

# 27 Product wall
s=slide(); rule(s,.55,.42,12.24,PURPLE,.045)
txt(s,'掌上乾坤  /  文创应用',.60,.62,7.8,.43,18,PURPLE,True)
txt(s,'从舞台到日常',.61,1.22,6.3,.76,36,WHITE,True)
txt(s,'五角色系列文创 · 产品效果图',8.08,1.47,4.51,.40,15,MUTED,align='right')
for i,(p,label,color) in enumerate([(PAPER,'书签与邮票',PINK),(SACHETS,'衣纹香囊',TEAL),(FIGURINES,'桌面摆件',PURPLE),(MIRRORS,'衣纹随身镜',YELLOW)]):
    x=.62+(i%2)*6.19; y=2.19+(i//2)*2.34
    box(s,x,y,5.92,2.17,CARD,color,True,1.0)
    photo(s,p,x+.12,y+.10,5.68,1.59)
    txt(s,label,x+.14,y+1.75,5.63,.33,17,color,True,align='center')
txt(s,'人物与图形可分别应用；制作规格以打样页为准。',.70,7.03,11.97,.25,11,MUTED,align='center')

# 28 Scene
s=base('成果展示 —— 展板空间效果',28,'04 / 场景应用')
photo(s,EXHIBIT,.56,1.38,12.20,5.56)
txt(s,'空间效果为氛围示意；正式展示内容以三张展板设计稿为准。',.72,6.93,10.9,.25,11,MUTED)

# Print guidance, tied to the actual three-panel PDF exported with the deck.
s=base('三联展板输出规范',33,'04 / 落地说明')
txt(s,'三张横向展板 · 统一尺寸与阅读层级',.60,1.31,11.7,.55,26,YELLOW,True)
for i,(head,body,col) in enumerate([
    ('01 版面','单板成品 900 × 506 mm；四周各留 3 mm 出血。',PINK),
    ('02 阅读','标题、导语、图注三级；重点文字在 1 m 外可辨。',TEAL),
    ('03 输出','文字保持矢量；图片按实际版面核对有效分辨率。',PURPLE)]):
    yy=2.17+i*1.30
    box(s,.64,yy,12.05,1.03,CARD,col,True,1.2)
    txt(s,head,.96,yy+.17,2.33,.58,20,col,True)
    txt(s,body,3.14,yy+.18,9.16,.58,17,WHITE)
txt(s,'另附三联展板 PDF 方案稿。正式大幅面印刷前，请按输出设备要求完成 CMYK 色彩、图片清晰度与实物打样检查。',.83,6.40,11.63,.47,14,MUTED,align='center')

# 29 Entire set
s=base('成果展示 —— 系列总览',29,'04 / 设计成果')
txt(s,'五位角色 · 五套纹样 · 多元文创 · 三组展板',.59,1.43,11.66,.64,28,WHITE,True,align='center')
for i,(p,a,c) in enumerate([(PAPER,'纸品',PINK),(SACHETS,'衣纹香囊',TEAL),(FIGURINES,'角色摆件',PURPLE),(MIRRORS,'衣纹随身镜',YELLOW)]):
    x=.52+i*3.18
    box(s,x,2.33,2.92,3.81,CARD,c,True,1.2)
    photo(s,p,x+.08,2.40,2.76,3.13)
    box(s,x+.32,5.60,2.27,.45,c,None,True)
    txt(s,a,x+.33,5.64,2.24,.33,14,BG,True,align='center')

# 30 Back cover
s=slide()
medallion(s,.9,.69,1.18,(PINK,TEAL,YELLOW))
medallion(s,11.85,.64,.98,(PURPLE,PINK,YELLOW))
txt(s,'掌上乾坤',2.2,1.13,8.9,.92,48,YELLOW,True,align='center')
txt(s,'泉州布袋戏',2.23,2.19,8.85,.88,46,PINK,True,align='center')
txt(s,'让一出掌中戏，走进更多人的生活',2.47,3.24,8.4,.52,20,WHITE,align='center')
rule(s,5.14,4.0,3.05,TEAL,.055)
for i in range(5): role(s,i,2.06+i*1.89,4.58,1.84,2.43)
txt(s,'QUANZHOU GLOVE PUPPET THEATRE · CULTURAL CREATIVE DESIGN',2.17,7.08,9.0,.24,10,MUTED,align='center')

# Product renderings predate the vector garment marks; make their status clear.
for sl in prs.slides:
    title=' '.join(sh.text for sh in sl.shapes if getattr(sh,'has_text_frame',False) and sh.text)
    if '设计延展 ——' in title:
        txt(sl,'概念效果图 · 实物图案以衣纹提取规范为准',.50,7.08,6.75,.23,9,MUTED)

assert len(prs.slides)==TOTAL, (len(prs.slides), TOTAL)
prs.save(OUT)
print(OUT)

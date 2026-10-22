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
MOTIFS = ASSETS / '11_floral_costume_motifs.png'
CITY = ASSETS / '02_quanzhou_cityscape.png'
PAPER = ASSETS / '12_floral_bookmarks.png'
STAMPS = ASSETS / '14_floral_stamps.png'
ACCESSORIES = ASSETS / '16_floral_keychains.png'
SACHETS = ASSETS / '13_floral_sachets.png'
MIRRORS = ASSETS / '18_floral_mirrors.png'
FIGURINES = ASSETS / '15_floral_figurines.png'
BAGS = ASSETS / '17_floral_totes.png'
EXHIBIT = ASSETS / '19_floral_exhibition_mockup.png'
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
W, H = 13.333, 7.5

BG = '#0D1019'
PINK = '#E85B85'
TEAL = '#52D1C3'
YELLOW = '#F2CF76'
PURPLE = '#AC90E9'
BLUE = '#76B3EA'
ORANGE = '#F2A46E'
WHITE = '#F5F0E7'
MUTED = '#B5ADAA'
CARD = '#181C29'
STROKE = '#494657'
GOLD = '#D8AA68'
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
    """Place one flower-and-costume emblem from the transparent system sheet."""
    d=min(w,h); px=x+(w-d)/2; py=y+(h-d)/2
    regions=[(0,120,430,570),(430,120,873,570),(873,120,1305,570),
             (1305,120,1740,570),(1740,120,2172,570)]
    x0,y0,x1,y1=regions[idx]
    pic=s.shapes.add_picture(str(MOTIFS),I(px),I(py),I(d),I(d))
    pic.crop_left=x0/2172; pic.crop_right=(2172-x1)/2172
    pic.crop_top=y0/724; pic.crop_bottom=(724-y1)/724
    return pic


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
    rule(s,.52,.25,12.29,GOLD,.018)
    txt(s,title,.56,.42,10.45,.50,26,WHITE,True)
    rule(s,.57,1.06,.58,PINK,.052); rule(s,1.18,1.06,.27,TEAL,.052)
    if tag: txt(s,tag,9.14,.48,3.48,.27,10,GOLD,align='right')
    txt(s,f'{len(prs.slides):02d} / {TOTAL}',11.84,7.07,1.0,.23,9,MUTED,align='right')
    return s


def divider(n,title,subtitle,idx,color):
    s=slide(); rule(s,.58,.44,12.18,GOLD,.018)
    txt(s,'CHAPTER  /  掌上乾坤',.66,.67,5.7,.34,12,GOLD,True)
    txt(s,f'{n:02d}',.57,1.40,2.3,1.4,83,color,True)
    txt(s,title,.72,3.16,7.6,1.57,40,WHITE,True,spacing=1.15)
    rule(s,.73,5.20,4.40,color,.055)
    txt(s,subtitle,.75,5.48,7.6,.43,13,MUTED)
    motif(s,idx,9.25,.98,2.74,2.74)
    role(s,idx,8.14,3.03,4.55,4.22)
    return s


def card(s,x,y,w,h,title,body,color=PINK,icon=None):
    box(s,x,y,w,h,CARD,STROKE,True)
    rule(s,x+.19,y+.18,.45,color,.06)
    if icon: txt(s,icon,x+w-.86,y+.08,.65,.6,32,color,True,align='center')
    txt(s,title,x+.2,y+.46,w-.4,.48,19,color,True)
    txt(s,body,x+.2,y+1.06,w-.4,h-1.20,14,WHITE,valign='top',spacing=1.20)


def product_spread(title,tag,image_path,index,summary,color):
    """Editorial product layout with a stable image scale and motif anchor."""
    s=base(title,0,tag)
    box(s,.59,1.45,3.14,5.35,CARD,STROKE,True)
    txt(s,f'{index+1:02d}',.84,1.73,2.0,.83,48,color,True)
    motif(s,index%5,.85,2.74,2.55,2.55)
    rule(s,.87,5.39,2.49,color,.047)
    txt(s,summary,.88,5.63,2.47,.84,16,WHITE,True,valign='top',spacing=1.16)
    box(s,4.00,1.45,8.72,5.35,'#101218',STROKE,True)
    photo(s,image_path,4.13,1.59,8.46,4.78)
    txt(s,'设计概念效果图  /  五角成戏系列',4.23,6.47,8.22,.26,11,MUTED,align='right')
    return s


# 01 Cover
s=slide()
rule(s,.65,.49,12.08,GOLD,.021)
txt(s,'泉州 · 掌中戏文化创意设计',.71,.77,7.3,.36,14,GOLD,True)
txt(s,'掌上乾坤',.67,1.50,7.78,.91,52,YELLOW,True)
txt(s,'泉州布袋戏',.67,2.50,7.92,.89,48,WHITE,True)
rule(s,.71,3.66,5.62,PINK,.060)
txt(s,'五角成戏  ×  花与衣纹',.72,3.94,6.84,.51,23,PINK,True)
txt(s,'QUANZHOU GLOVE PUPPET THEATRE',.73,4.55,6.8,.32,13,MUTED)
motif(s,2,9.51,.65,3.22,3.22)
role(s,2,8.37,2.10,4.71,4.83)
for i in range(5):
    role(s,i,.72+i*1.27,5.22,1.21,1.46)
    txt(s,ROLE_NAMES[i],.83+i*1.27,6.70,.98,.27,14,ROLE_COLOR[i],True,align='center')
txt(s,'CULTURAL CREATIVE DESIGN  /  2026',.73,7.09,6.7,.22,9,MUTED)

# 02 Contents
s=slide(); txt(s,'目录',.60,.52,2.1,.62,33,WHITE,True)
txt(s,'CONTENTS',2.39,.66,3.0,.32,16,GOLD,True)
rule(s,.60,1.25,12.05,GOLD,.022)
sections=[('01','创意溯源','与文化背景',PINK),('02','核心视觉设计','与规范',TEAL),('03','文创衍生品','开发应用',PURPLE),('04','展板设计','与成果展示',BLUE)]
for i,(n,a,b,c) in enumerate(sections):
    x=.62+i*3.12
    box(s,x,1.63,2.85,4.64,CARD,STROKE,True)
    txt(s,n,x+.18,1.90,2.5,.95,49,c,True)
    txt(s,a+'\n'+b,x+.18,3.18,2.46,1.28,21,WHITE,True,spacing=1.22)
    rule(s,x+.18,4.79,2.31,c,.035)
    motif(s,i if i<3 else 4,x+.82,5.05,1.15,1.15)
txt(s,'从文化依据走向完整的角色、图形、文创与展陈系统',.69,6.69,11.72,.37,16,MUTED,align='center')

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
for j,idx in enumerate([1,2,4]):
    motif(s,idx,1.71+j*4.18,4.65,1.49,1.21)
txt(s,'文化识别 → 角色共鸣 → 场景使用 → 自发传播',2.24,6.38,8.87,.45,17,WHITE,True,align='center')

# 06 Audience
s=base('受众人群与使用场景',6,'01 / 目标人群')
card(s,.53,1.58,3.9,4.64,'泉州游客','希望带走轻便、具有地方辨识度的纪念品。\n\n场景：景区、博物馆、古城街巷。',PINK)
card(s,4.71,1.58,3.9,4.64,'青年与亲子','偏好角色故事、成套收藏和互动体验。\n\n场景：研学课堂、社交分享、礼赠。',TEAL)
card(s,8.89,1.58,3.9,4.64,'文旅机构','需要能够代表在地文化、方便陈列与传播的系列礼品。\n\n场景：展演活动、城市礼物、公共教育。',PURPLE)
for j,idx in enumerate([0,4,3]):
    role(s,idx,1.53+j*4.18,4.55,1.81,1.50)
txt(s,'接触戏偶 → 认识行当 → 收集角色 → 分享泉州故事',1.73,6.55,9.9,.38,16,WHITE,True,align='center')

# 07 Reference style
s=base('版式与视觉策略',7,'01 / 风格定位')
txt(s,'从戏台到展场：清晰的叙事秩序',.57,1.48,10.8,.65,31,WHITE,True)
txt(s,'一页一重点 · 大标题 · 五色分角 · 金线花纹',.58,2.18,10.7,.39,17,TEAL,True)
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
s=base('花与衣纹辅助图形',12,'02 / 纹样系统')
txt(s,'五角五纹 · 衣纹骨架 × 花卉意象',.61,1.35,11.68,.5,20,PINK,True)
for i,(a,b) in enumerate([('青云梅花','生'),('牡丹衣纹','旦'),('赤焰花云','净'),('海潮白梅','末'),('绿衣团花','丑')]):
    x=.43+i*2.56
    motif(s,i,x,2.09,2.43,3.61)
    txt(s,a,x+.04,5.70,2.34,.47,17,ROLE_COLOR[i],True,align='center')
    txt(s,b,x+.34,6.17,1.74,.35,13,WHITE,align='center')
txt(s,'统一金线与花瓣节奏，让五种角色服饰图形形成同一品牌家族。',.75,6.72,11.85,.35,14,MUTED,align='center')

# Evidence of the actual costume-to-graphic extraction.
s=base('花与衣纹的生成过程',14,'02 / 图形推导')
txt(s,'衣服局部 → 纹样骨架 → 花卉延展',.63,1.29,9.3,.55,26,PINK,True)
txt(s,'原服饰局部',.86,1.98,2.15,.37,15,WHITE,True,align='center')
txt(s,'提炼动作',4.50,1.98,2.0,.37,15,WHITE,True,align='center')
txt(s,'辅助图形',8.97,1.98,2.2,.37,15,WHITE,True,align='center')
regions=[(400,895,790,1105),(395,725,605,900),(525,855,795,1085),(270,1000,560,1185),(305,655,475,830)]
steps=['三瓣云头 + 梅花','粉袖花心 + 金蔓','裙甲团云 + 焰花','蓝袍云浪 + 白梅','绿衣五瓣花放大']
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
    txt(s,['青云梅花','牡丹衣纹','赤焰花云','海潮白梅','绿衣团花'][i],9.46,yy+.15,2.78,.37,16,ROLE_COLOR[i],True)
txt(s,'衣服提供结构与主色；花卉提供统一的生长感与礼赠气质。',.73,6.64,11.93,.34,14,MUTED,align='center')

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
product_spread('角色书签','03 / 纸品系列',PAPER,0,'完整人物与花云边饰\n组合成可收藏纸品',PINK)

# 17 Sachet
product_spread('衣纹香囊','03 / 随身系列',SACHETS,1,'花与衣纹并置\n形成五款随身香囊',TEAL)

# 18 Stamps
product_spread('五角纪念邮票','03 / 纸品系列',STAMPS,2,'五角成组\n延展成轻量纪念品',ORANGE)

# 19 Display figurines
product_spread('桌面角色摆件','03 / 收藏系列',FIGURINES,3,'完整人物成套\n建立桌面收藏场景',BLUE)

# 20 Keychains
product_spread('角色钥匙扣','03 / 随身系列',ACCESSORIES,4,'完整人物挂件\n配同色花云徽章',YELLOW)

# 21 Tote bags
product_spread('五角帆布袋','03 / 随身系列',BAGS,5,'全身角色置于中央\n花云图形构成边框',TEAL)

# 22 Collection
product_spread('衣纹随身镜','03 / 礼赠系列',MIRRORS,6,'独立纹样做镜面\n与纸品组合成礼盒',PINK)

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
txt(s,'五位人物均以完整形象展示；下方图形由各自衣纹与花卉意象组合。',.62,6.94,12.06,.32,13,MUTED,align='center')

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
rule(s,.63,.48,12.08,GOLD,.021)
txt(s,'掌上乾坤  /  泉州布袋戏',.70,.74,7.50,.37,16,GOLD,True)
txt(s,'戏在掌中，也在日常。',.66,1.53,11.60,.88,45,WHITE,True)
txt(s,'让一出掌中戏，走进更多人的生活',.70,2.52,9.63,.52,22,PINK,True)
rule(s,.70,3.20,11.90,TEAL,.052)
for i in range(5):
    x=.55+i*2.57
    role(s,i,x,3.59,2.42,2.83)
    txt(s,ROLE_NAMES[i],x+.77,6.45,.91,.33,18,ROLE_COLOR[i],True,align='center')
txt(s,'QUANZHOU GLOVE PUPPET THEATRE  ·  CULTURAL CREATIVE DESIGN',.69,7.10,10.84,.24,10,MUTED)

assert len(prs.slides)==TOTAL, (len(prs.slides), TOTAL)
prs.save(OUT)
print(OUT)

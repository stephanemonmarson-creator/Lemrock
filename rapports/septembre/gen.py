from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
O=RGBColor(0xEE,0x6A,0x2C);K=RGBColor(0x11,0x11,0x11);G=RGBColor(0x55,0x5B,0x66);LG=RGBColor(0x8A,0x93,0xA6)
GR=RGBColor(0x1E,0x7B,0x34);RD=RGBColor(0xB0,0x48,0x37);BG=RGBColor(0xF8,0xF6,0xF2);W=RGBColor(255,255,255);BOX=RGBColor(0xF1,0xEF,0xEA)
import json,sys
D=json.load(open(sys.argv[1]))
p=Presentation();p.slide_width=Emu(12192000);p.slide_height=Emu(6858000)
s=p.slides.add_slide(p.slide_layouts[6])
X=lambda v:Emu(int(v*12192000/2000))  # coords in 2000-wide px space
def rect(x,y,w,h,fill,line=None):
    r=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,X(x),X(y),X(w),X(h));r.fill.solid();r.fill.fore_color.rgb=fill
    if line: r.line.color.rgb=line;r.line.width=Pt(.75)
    else: r.line.fill.background()
    r.shadow.inherit=False;return r
def txt(x,y,w,h,runs,size=12,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP):
    tb=s.shapes.add_textbox(X(x),X(y),X(w),X(h));tf=tb.text_frame;tf.word_wrap=True;tf.vertical_anchor=anchor
    for m in ('margin_left','margin_right','margin_top','margin_bottom'):setattr(tf,m,0)
    lines=runs if isinstance(runs[0],list) else [runs]
    for i,line in enumerate(lines):
        para=tf.paragraphs[0] if i==0 else tf.add_paragraph();para.alignment=align
        for t,c,sz,b,it in line:
            r=para.add_run();r.text=t;f=r.font;f.size=Pt(sz);f.bold=b;f.italic=it;f.color.rgb=c;f.name='Arial'
    return tb
R=lambda t,c=K,sz=12,b=False,it=False:(t,c,sz,b,it)
rect(0,0,2000,1125,BG);rect(15,20,1905,14,O)
txt(87,80,1200,30,[R('RAPPORT DE PERFORMANCE · 01/09/2026 → 30/09/2026',O,13,True)])
txt(87,105,1200,80,[R(D['client'],K,36,True)])
txt(1300,97,542,25,[R('COMPARAISON',LG,12,True)],align=PP_ALIGN.RIGHT)
txt(1300,128,542,30,[R('vs 01/08/2026 → 31/08/2026',K,15,True)],align=PP_ALIGN.RIGHT)
for x,t in((87,'DIFFUSION'),(392,'ENGAGEMENT'),(1002,'CONVERSION')):txt(x,210,400,30,[R(t,O,14,True)])
kp=[tuple(k[:3])+(GR if k[3]=='up' else RD if k[3]=='down' else G,k[4]) for k in D['kpis']]
for i,(l,v,d,dc,y) in enumerate(kp):
    x=87+i*305;rect(x,252,228,185,W,RGBColor(0xE4,0xE2,0xDC));rect(x,252,8,185,O)
    txt(x+22,265,200,20,[R(l,G,10,True)]);txt(x+22,310,200,45,[R(v,K,22,True)])
    txt(x+22,368,200,18,[R(d,dc,10,True)]);txt(x+22,390,200,15,[R('vs période préc.',G,7)]);txt(x+22,410,200,15,[R(y,G,8,False,True)])
txt(87,545,1200,30,[R('INSIGHTS QUALITATIFS · ANALYSE DES RECHERCHES',O,14,True)])
for x in(87,688,1289):rect(x,588,558,420,W,RGBColor(0xE4,0xE2,0xDC))
# champ lexical
txt(127,618,480,25,[R('CHAMP LEXICAL',G,13,True)]);txt(127,655,480,20,[R('Termes les plus fréquents',LG,10,False,True)])
words=[[R(t,{'O':O,'K':K,'G':G}[c],sz,bold) for t,c,sz,bold in line] for line in D['words']]
tb=txt(127,695,490,300,words)
for para in tb.text_frame.paragraphs: para.space_after=Pt(5)
for i in range(1,len(words)):pass
# requetes
txt(728,618,480,25,[R('EXEMPLES DE REQUÊTES',G,13,True)]);txt(728,655,480,20,[R('Questions posées aux IA',LG,10,False,True)])
qs=D['queries']
for i,q in enumerate(qs):
    y=700+i*60;rect(728,y,478,50,BOX);txt(748,y,30,50,[R('🔍',G,9)],anchor=MSO_ANCHOR.MIDDLE);txt(786,y,410,50,[R(q,K,9)],anchor=MSO_ANCHOR.MIDDLE)
# categories
txt(1329,618,480,25,[R('CATÉGORIES DE PRODUITS',G,13,True)]);txt(1329,655,480,20,[R('Répartition des requêtes',LG,10,False,True)])
PAL=[RGBColor(0x1C,0x7C,0x8C),RGBColor(0x7A,0x4E,0x96),RGBColor(0xEB,0x9A,0x5E),O,RGBColor(0x3E,0x5A,0x78),RGBColor(0xA0,0x92,0x78)]
cats=[(c[0],c[1],PAL[i],c[2] if len(c)>2 else f'{c[1]} %') for i,c in enumerate(D['cats'])]
txt(1740,685,85,20,[R('100%',K,11,True)],align=PP_ALIGN.RIGHT)
y0=730;H=220
for i,(n,v,c,lab) in enumerate(cats):
    yy=715+i*44;rect(1325,yy+8,20,20,c);txt(1361,yy+5,340,25,[R(n if (i==0 and v>=25) else f'{n} · {lab}',K,10)])
for n,v,c,lab in cats:
    h=H*v/100;b=rect(1733,y0,78,h,c)
    if v>=25:txt(1733,y0,78,h,[R(f'{v} %',W,10,True)],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    y0+=h
s=p.slides.add_slide(p.slide_layouts[6])
rect(0,0,2000,1125,BG);rect(15,20,1905,14,O)
txt(95,70,1200,30,[R('INSIGHTS QUALITATIFS · SEPTEMBRE 2026',O,13,True)])
txt(95,100,1200,80,[R(D['client'],K,36,True)])
txt(1500,82,310,30,[R('Lemrock',K,15,True)],align=PP_ALIGN.RIGHT)
txt(95,200,1500,30,[R('OBJECTIF   ',O,13,True),R('À définir',K,13)])
txt(95,250,800,30,[R('INSIGHTS QUALITATIFS',G,14,True)])
ins=D['insights']
for i,(t,b,r) in enumerate(ins):
    x=95+(i%2)*888;y=298+(i//2)*380
    rect(x,y,832,348,RGBColor(0xF6,0xF7,0xF9),RGBColor(0xE4,0xE2,0xDC))
    txt(x+42,y+35,80,40,[R(f'0{i+1}',O,20,True)])
    txt(x+132,y+38,660,60,[R(t,K,14,True)])
    txt(x+42,y+130,750,120,[R(b,G,11)])
    txt(x+42,y+245,750,80,[R('→  '+r,G,9,True)])

p.save(D['out'])

from PIL import Image, ImageDraw, ImageFilter
import math
SK=(238,200,172); SKD=(214,170,142); SKL=(246,214,190)
HAIR=(30,24,26); HAIRL=(66,54,56); SHIRT=(26,26,30); SHIRTL=(48,48,54)
IMG=[None]
def bez(p0,p1,p2,p3,n=24):
    return [((1-t)**3*p0[0]+3*(1-t)**2*t*p1[0]+3*(1-t)*t*t*p2[0]+t**3*p3[0],
             (1-t)**3*p0[1]+3*(1-t)**2*t*p1[1]+3*(1-t)*t*t*p2[1]+t**3*p3[1]) for t in [i/n for i in range(n+1)]]
def path(*segs):
    pts=[]
    for s in segs: pts+=bez(*s)
    return pts
def head(d,cx,cy,s,smile=1.0,look=0.0,blink=False):
    T=lambda pts:[(cx+x*s,cy+y*s) for x,y in pts]
    def poly(pts,fill): d.polygon(T(pts),fill=fill)
    def line(pts,fill,w): d.line(T(pts),fill=fill,width=max(2,int(w*s)),joint="curve")
    def ell(x0,y0,x1,y1,fill): d.ellipse([cx+x0*s,cy+y0*s,cx+x1*s,cy+y1*s],fill=fill)
    # orelhas
    for sx in (-1,1):
        ell(sx*110-20,-30,sx*110+20,40,SK) if sx==-1 else ell(110-20,-30,110+20,40,SK)
        ell(sx*113-9,-14,sx*113+9,22,SKD)
    # rosto (mandibula marcada)
    face=path(((0,-150),(-74,-150),(-120,-100),(-118,-30)),((-118,-30),(-118,40),(-104,86),(-76,118)),((-76,118),(-54,138),(-26,150),(0,152)))
    face=face+[(-x,y) for x,y in reversed(face)]
    poly(face,SK)
    # pescoço sombra sob o queixo vem do corpo
    # nariz
    line([(-6,-10),(-12,28),(-20,40)],SKD,3.5); line([(-20,40),(-6,48),(10,46),(20,40)],SKD,3.5)
    ell(-22,36,-8,46,SKD); ell(8,36,22,46,SKD)
    # sobrancelhas grossas
    for sx in (-1,1):
        pts=[(sx*20,-34),(sx*42,-48),(sx*66,-48),(sx*84,-38)]
        up=[(x,y-9) for x,y in pts]; low=[(x,y+7) for x,y in pts]
        up[0]=(sx*20,-40); 
        poly(bez(pts[0],pts[1],pts[2],pts[3],10)+list(reversed(bez((pts[0][0],pts[0][1]+8),(pts[1][0],pts[1][1]-10),(pts[2][0],pts[2][1]-12),(pts[3][0],pts[3][1]-6),10))),HAIR)
    # olhos
    for sx in (-1,1):
        ex=sx*45; ey=-12
        if blink:
            line([(ex-22,ey),(ex,ey+5),(ex+22,ey)],HAIR,4)
        else:
            eye=path(((ex-24,ey+2),(ex-14,ey-14),(ex+14,ey-14),(ex+24,ey+2)),((ex+24,ey+2),(ex+12,ey+14),(ex-12,ey+14),(ex-24,ey+2)))
            poly(eye,(250,246,240))
            ix=ex+look*6
            ell(ix-11,ey-11,ix+11,ey+11,(86,52,34)); ell(ix-6,ey-6,ix+6,ey+6,(20,14,14)); ell(ix-9,ey-9,ix-2,ey-2,(255,255,255))
            line(path(((ex-26,ey+1),(ex-14,ey-17),(ex+14,ey-17),(ex+26,ey+1))),HAIR,4.5)
    # bigode + bigode fino
    for sx in (-1,1):
        m=path(((sx*3,62),(sx*20,55),(sx*46,54),(sx*68,70)),((sx*68,70),(sx*46,64),(sx*20,64),(sx*3,66)))
        poly(m,HAIR)
    # boca
    sm=smile
    bl=Image.new('RGBA',IMG[0].size,(0,0,0,0)); bd=ImageDraw.Draw(bl)
    for sx in (-1,1): bd.ellipse([cx+(sx*58-20)*s,cy+22*s,cx+(sx*58+20)*s,cy+50*s],fill=(220,120,100,70))
    bl=bl.filter(ImageFilter.GaussianBlur(6*s)); IMG[0].paste(bl,(0,0),bl)
    lip=path(((-34,80),(-14,76+8*sm),(14,76+8*sm),(34,80)))
    line(lip,(120,60,60),4)
    line([(-36,79),(-42,72)],(120,60,60),3.5); line([(36,79),(42,72)],(120,60,60),3.5)
    if sm>1.05:
        mouth=path(((-32,80),(-18,92+10*sm),(18,92+10*sm),(32,80)))+[(32,80),(-32,80)]
        poly(mouth,(250,244,238)); line(path(((-32,80),(-18,92+10*sm),(18,92+10*sm),(32,80))),(120,60,60),3)
        line([(-30,80),(30,80)],(120,60,60),3)
    # cabelo: base + topete ondulado e laterais degradê
    lay=Image.new("RGBA",IMG[0].size,(0,0,0,0)); ld=ImageDraw.Draw(lay)
    for sx in (-1,1): poly([(sx*120,-64),(sx*108,-70),(sx*100,-20),(sx*108,-4),(sx*114,-30)],HAIR)
    top=path(((-118,-50),(-130,-130),(-90,-196),(-20,-208)),((-20,-208),(40,-216),(96,-196),(118,-146)),((118,-146),(130,-110),(124,-70),(114,-40)))
    fringe=path(((114,-40),(112,-62),(104,-66),(90,-64)),((90,-64),(40,-58),(-30,-62),(-70,-68)),((-70,-68),(-100,-70),(-112,-62),(-118,-50)))
    poly(top+fringe,HAIR)
    for xx in (-80,-45,-10,25,60,95):
        line([(xx,-120),(xx+4,-95),(xx+2,-66)],HAIRL,2.2)
    for pts in [[(-90,-160),(-40,-190),(20,-198),(80,-184)],[(-100,-130),(-50,-168),(10,-180),(70,-166)],[(-30,-120),(20,-150),(70,-156),(104,-136)]]:
        line(bez(*pts,20),HAIRL,2.6)
    # boné preto virado pra trás
    CAP=(34,34,38); CAPD=(18,18,20); CAPL=(70,70,78)
    cy-=14*s
    # aba aparecendo atrás, nas laterais
    for sx in (-1,1):
        pass
    dome=path(((-134,-84),(-140,-160),(-74,-216),(0,-220)),((0,-220),(74,-216),(140,-160),(134,-84)))
    poly(dome+path(((134,-84),(70,-72),(-70,-72),(-134,-84))),CAP)
    for pts in [[(0,-220),(-22,-180),(-30,-130),(-30,-76)],[(0,-220),(22,-180),(30,-130),(30,-76)],[(0,-220),(-60,-190),(-92,-140),(-106,-84)],[(0,-220),(60,-190),(92,-140),(106,-84)]]:
        line(bez(*pts,20),CAPL,2.4)
    ell(-9,-228,9,-212,CAPD)
    line(path(((-134,-84),(-70,-72),(70,-72),(134,-84))),CAPL,3)
    line(path(((-130,-94),(-70,-82),(70,-82),(130,-94))),CAPL,1.8)
def body(d,cx,cy,s,arm_r=None):
    T=lambda pts:[(cx+x*s,cy+y*s) for x,y in pts]
    # pescoço
    d.polygon(T([(-46,100),(46,100),(52,200),(-52,200)]),fill=SK)
    d.polygon(T([(-46,128),(46,128),(46,140),(0,150),(-46,140)]),fill=SKD)  # sombra do queixo
    # ombros / camisa preta
    sh=path(((-52,196),(-120,208),(-250,236),(-290,330)),((-290,330),(-300,420),(-300,520),(-300,620)))
    sh=sh+[(300,620),(300,620)]+[(-x,y) for x,y in reversed(sh)]
    d.polygon(T(sh),fill=SHIRT)
    # decote em V com pele + gola
    d.polygon(T([(-58,206),(58,206),(0,330)]),fill=SK)
    d.polygon(T([(-58,206),(-4,324),(-96,300),(-120,222)]),fill=SHIRTL)
    d.polygon(T([(58,206),(4,324),(96,300),(120,222)]),fill=SHIRTL)
    d.line(T([(-58,206),(-4,324)]),fill=(14,14,16),width=max(2,int(3*s)))
    d.line(T([(58,206),(4,324)]),fill=(14,14,16),width=max(2,int(3*s)))
    # botões
    for k in range(3): d.ellipse([cx+(-4)*s,cy+(350+k*70)*s-5*s,cx+(4)*s,cy+(350+k*70)*s+5*s],fill=(70,70,76))
def portrait(path_out,smile=1.0):
    SS=2; W,H=1080,1350
    im=Image.new("RGBA",(W*SS,H*SS),(244,236,224,255))
    IMG[0]=im
    d=ImageDraw.Draw(im)
    # fundo
    for y in range(H*SS):
        t=y/(H*SS); c=(int(236-30*t),int(232-26*t),int(220-24*t)); d.line([(0,y),(W*SS,y)],fill=c+(255,))
    d.ellipse([120*SS,160*SS,960*SS,1000*SS],fill=(214,206,190,255))
    body(d,540*SS,626*SS,2.3*SS)
    head(d,540*SS,566*SS,2.3*SS,smile=smile)
    im=im.resize((W,H),Image.LANCZOS).convert("RGB"); im.save(path_out,quality=94)
if __name__=="__main__":
    portrait("matheus_v5a.jpg")
    portrait("matheus_v5.jpg",smile=1.3)

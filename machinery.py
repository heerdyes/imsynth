from PIL import Image,ImageDraw,ImageFont
from math import radians,sin,cos,pi

# global symbol table
symtab={}

# functions
def readtillspace(ln):
    cmd=[]
    args=''
    if ln.startswith(' '):
        raise Exception('must begin with non-space character')
    for c in ln:
        if c==' ':
            break
        cmd.append(c)
    if len(cmd)<len(ln):
        args=ln[len(cmd)+1:]
    return ''.join(cmd),args

def imgbuild(imgnm):
    global symtab
    if 'dimension' in symtab and 'fgcolor' in symtab and 'bgcolor' in symtab and 'canvas' not in symtab:
        w,h=symtab['dimension']
        r,g,b=symtab['bgcolor']
        symtab['canvas']=Image.new('RGB',(w,h),(r,g,b))
        symtab['drawer']=ImageDraw.Draw(symtab['canvas'])
        if 'fontfile' in symtab:
            symtab['font']=ImageFont.truetype(symtab['fontfile'], size=12)
        else:
            symtab['font']=ImageFont.load_default()
        symtab['filename']=imgnm+'.jpg'
        
def imgsave():
    if 'canvas' in symtab:
        symtab['canvas'].save(symtab['filename'])
        
def cln(x1,y1,x2,y2):
    if 'canvas' not in symtab:
        raise Exception('canvas not yet created')
    symtab['drawer'].line((x1,y1,x2,y2),fill=symtab['fgcolor'],width=1)
    
def ln(x,y,r,th):
    if 'canvas' not in symtab:
        raise Exception('canvas not yet created')
    dw=symtab['drawer']
    fg=symtab['fgcolor']
    nx=x+r*cos(radians(th))
    ny=y-r*sin(radians(th))
    dw.line((x, y, nx, ny),fill=fg,width=1)
    return nx, ny
    
def dln(x,y,r,th,n):
    np=x,y
    for i in range(n):
        if i%2==0:
            symtab['fgcolor']=(0, 0, 64)
        else:
            symtab['fgcolor']=(255,255,255)
        np=ln(np[0], np[1], r/n, th)
    symtab['fgcolor']=(0, 0, 64)
    
def drawrect(x,y,w,h):
    if 'canvas' not in symtab:
        raise Exception('canvas not yet created')
    symtab['drawer'].rectangle((x,y,x+w,y+h),fill=symtab['bgcolor'],outline=symtab['fgcolor'])
    
def write(x,y,msg):
    if 'canvas' not in symtab:
        raise Exception('canvas not yet created')
    symtab['drawer'].text((x,y),msg,fill=symtab['fgcolor'],font=symtab['font'])
    
def drawtxtbox(x,y,w,h,txt):
    if 'canvas' not in symtab:
        raise Exception('canvas not yet created')
    dw=symtab['drawer']
    bg=symtab['bgcolor']
    fg=symtab['fgcolor']
    dw.rectangle((x-w/2,y-h/2,x-w/2+w,y-h/2+h),fill=bg,outline=fg)
    dw.text((x,y),txt,fill=fg,font=symtab['font'])
    
def drawarrow(x1,y1,r,th):
    dw=symtab['drawer']
    bg=symtab['bgcolor']
    fg=symtab['fgcolor']
    ath=radians(th)
    x2=x1+r*cos(ath)
    y2=y1-r*sin(ath)
    dw.line((x1,y1,x2,y2),fill=fg,width=1)
    revth=pi+ath
    rtip=15.0
    ddeg=18.0
    delta=radians(ddeg)
    dw.line((x2, y2, x2+rtip*cos(revth-delta), y2-rtip*sin(revth-delta)),fill=fg,width=1)
    dw.line((x2, y2, x2+rtip*cos(revth+delta), y2-rtip*sin(revth+delta)),fill=fg,width=1)
    
def drawnote(x,y,w,h):
    dw=symtab['drawer']
    bg=symtab['bgcolor']
    fg=symtab['fgcolor']
    dw.rectangle((x, y, x+w, y+h),fill=None,outline=fg)
    d=8.0
    dw.line((x+w-d, y, x+w, y+d),fill=fg,width=1)
    
def setfnt(fntf):
    global symtab
    symtab['fontfile']=fntf

def execinst(cmd,args):
    global symtab
    if cmd=='wh':
        w,h=[int(x) for x in args.split(' ')]
        symtab['dimension']=w,h
    elif cmd=='bg':
        r,g,b=[int(x) for x in args.split(' ')]
        symtab['bgcolor']=r,g,b
    elif cmd=='fg':
        r,g,b=[int(x) for x in args.split(' ')]
        symtab['fgcolor']=r,g,b
    elif cmd=='mk':
        imgbuild(args)
    elif cmd=='ln':
        params=[int(m) for m in args.split(' ')]
        ln(*params)
    elif cmd=='dln':
        params=[int(m) for m in args.split(' ')]
        dln(*params)
    elif cmd=='box':
        params=[int(m) for m in args.split(' ')]
        drawrect(*params)
    elif cmd=='txt':
        car,cdr=readtillspace(args)
        x=int(car)
        car,cdr=readtillspace(cdr)
        y=int(car)
        write(x,y,cdr)
    elif cmd=='fnt':
        setfnt(args)
    elif cmd=='arrow':
        params=[int(m) for m in args.split(' ')]
        drawarrow(*params)
    elif cmd=='note':
        params=[int(m) for m in args.split(' ')]
        drawnote(*params)
    elif cmd=='txtbox':
        car,cdr=readtillspace(args)
        x=int(car)
        car,cdr=readtillspace(cdr)
        y=int(car)
        car,cdr=readtillspace(cdr)
        w=int(car)
        car,cdr=readtillspace(cdr)
        h=int(car)
        drawrect(x,y,w,h)
        write(x,y,cdr)


#!/usr/bin/env python

'''
    A quick and dirty diagram-as-code toy language that generates images
'''

from PIL import Image,ImageDraw,ImageFont
import sys

# globals
fcfg='tmp.art'
symtab={}
cfglns=None


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
        
def drawline(x1,y1,x2,y2):
    if 'canvas' not in symtab:
        raise Exception('canvas not yet created')
    symtab['drawer'].line((x1,y1,x2,y2),fill=symtab['fgcolor'],width=1)
    
def drawrect(x,y,w,h):
    if 'canvas' not in symtab:
        raise Exception('canvas not yet created')
    symtab['drawer'].rectangle((x,y,w,h),fill=symtab['bgcolor'],outline=symtab['fgcolor'])
    
def write(x,y,msg):
    if 'canvas' not in symtab:
        raise Exception('canvas not yet created')
    symtab['drawer'].text((x,y),msg,fill=symtab['fgcolor'],font=symtab['font'])
    
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
        drawline(*params)
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


# flow begins
if len(sys.argv)==2:
    fcfg=sys.argv[1]

with open(fcfg) as fc:
    lns=fc.readlines()
    cfglns=[x.strip() for x in lns]

for ln in cfglns:
    if len(ln)==0:
        continue
    if ln.startswith('#'):
        continue
    cmd,args=readtillspace(ln)
    execinst(cmd,args)

imgsave()


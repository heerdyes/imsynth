#!/usr/bin/env python

'''
    A quick and dirty diagram-as-code toy language that generates images
'''

import sys
from machinery import *

# globals
fcfg='tmp.art'
cfglns=None

# flow begins
if len(sys.argv)==2:
    fcfg=sys.argv[1]

with open(fcfg) as fc:
    lns=fc.readlines()
    cfglns=[x.strip() for x in lns]

# pass 1 (label processing)
for i in range(len(cfglns)):
    ln=readtillsemicolon(cfglns[i])
    cmd,args=readtillspace(ln)
    if cmd=='lbl':
        symtab['labels'][args]=i

# pass 2 (actual execution)
while symtab['PC']<len(cfglns):
    ln=cfglns[symtab['PC']]
    if len(ln)!=0:
        cmd,args=readtillspace(ln)
        execinst(cmd,args)
    symtab['PC']+=1

imgsave()


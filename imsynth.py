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

for ln in cfglns:
    if len(ln)==0:
        continue
    if ln.startswith('#'):
        continue
    cmd,args=readtillspace(ln)
    execinst(cmd,args)

imgsave()


from copy import deepcopy
from matplotlib.pyplot import cm
import numpy as np

def generateformat(n, singlecolor=False):
    colorlist = cm.rainbow(np.linspace(0, 1, n))
    if singlecolor:
        colorlist = ["blue"]*n

    #dotformatlist
    #dotformatlist = deepcopy(colorlist)
    dotformatlist = []
    for c in colorlist:
        dotformatlist.append({"c": c})
    for f in dotformatlist:
        f["marker"] = "o"
    
    #lineformatlist
    #lineformatlist = deepcopy(colorlist)
    lineformatlist = []
    for c in colorlist:
        lineformatlist.append({"c": c})
    for f in lineformatlist:
        f["linestyle"]="-"
    
    #linedotformatlist
    linedotformatlist = deepcopy(dotformatlist)
    for f in linedotformatlist:
        f['linestyle']="-"
    
    
    assignformat = {"dot": dotformatlist, "line-dot": linedotformatlist, "line": lineformatlist}
    return assignformat

'''
colorlist = []
formatdict = {'c':"r"}
colorlist.append(formatdict)
formatdict = {'c':"c"}
colorlist.append(formatdict)
formatdict = {'c':"b"}
colorlist.append(formatdict)
formatdict = {'c':"green"}
colorlist.append(formatdict)
formatdict = {'c':"violet"}
colorlist.append(formatdict)
formatdict = {'c':"orange"}
colorlist.append(formatdict)
formatdict = {'c':"darkblue"}
colorlist.append(formatdict)
formatdict = {'c':"lime"}
colorlist.append(formatdict)
formatdict = {'c':"turquoise"}
colorlist.append(formatdict)
'''

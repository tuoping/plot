from copy import deepcopy
from matplotlib.pyplot import cm
import numpy as np

def generateformat(n, singlecolor=False):
    # colorlist = cm.rainbow(np.linspace(0, 1, n))
    if n <= 7:
        edgecolorlist = ["k", "r", "b", "g", "m", "lime","cyan"]
    else:
        # edgecolorlist = cm.rainbow(np.linspace(0, 1, n))#["k", "r", "b", "g"]
        edgecolorlist = cm.get_cmap("rainbow")#["k", "r", "b", "g"]
    #if n > 1:
    colorlist = edgecolorlist
    #else:
    # colorlist = ["w"]*n
    if singlecolor:
        colorlist = ["k"]*n
        edgecolorlist = colorlist

    #dotformatlist
    #dotformatlist = deepcopy(colorlist)
    dotformatlist = []
    for i in range(n):
        if n > 7:
            c = colorlist(float(i)/float(n))
        else:
            c = colorlist[i]
        dotformatlist.append({"c": c})
        if n > 7:
            ec = edgecolorlist(float(i)/float(n))
        else:
            ec = edgecolorlist[i]
        dotformatlist[-1]["ec"] = ec
    for f in dotformatlist:
        f["marker"] = "o"
    
    #lineformatlist
    #lineformatlist = deepcopy(colorlist)
    lineformatlist = []
    for i in range(n):
        if n > 7:
            c = edgecolorlist(float(i)/float(n))
        else:
            c = edgecolorlist[i]
        lineformatlist.append({"c": c})
    for f in lineformatlist:
        f["linestyle"]="-"
    
    #linedotformatlist
    linedotformatlist = deepcopy(dotformatlist)
    for f in linedotformatlist:
        f['linestyle']="-"
    
    
    assignformat = {"dot": dotformatlist, "line-dot": linedotformatlist, "line": lineformatlist, "hist": colorlist, "bar": colorlist}
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

from copy import deepcopy
from matplotlib.pyplot import cm
import numpy as np

def generateformat(n, singlecolor=False):
    if singlecolor:
        colorlist = ["b"]*n
        edgecolorlist = colorlist
    if n <= 4:
        edgecolorlist = ["b", "r", "k", "g"]
    else:
        # edgecolorlist = [cm.get_cmap("Dark2")(float(i)/float(n)) for i in range(n)]
        edgecolorlist = [cm.get_cmap("gist_ncar")(float(i)/float(n)) for i in range(n)]
    colorlist = deepcopy(edgecolorlist)
    colorlist[4:] = ["w"]*(n-4)
    

    #dotformatlist
    #dotformatlist = deepcopy(colorlist)
    dotformatlist = []
    for i in range(n):
        c = colorlist[i]
        dotformatlist.append({"c": c})
        ec = edgecolorlist[i]
        dotformatlist[-1]["ec"] = ec
        # dotformatlist[-1]["alpha"] = float(n-i)/n
        dotformatlist[-1]["alpha"] = 1.
        dotformatlist[-1]["size"] = float(n-i)/n*3
    for f in dotformatlist:
        f["marker"] = "o"
    
    #lineformatlist
    #lineformatlist = deepcopy(colorlist)
    lineformatlist = []
    for i in range(n):
        c = edgecolorlist[i]
        lineformatlist.append({"c": c})
        # lineformatlist[-1]["alpha"] = float(n-i)/n
        lineformatlist[-1]["alpha"] = 1
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

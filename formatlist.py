from copy import deepcopy

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

#dotformatlist
dotformatlist = deepcopy(colorlist)
for f in dotformatlist:
    f["marker"] = "o"

#lineformatlist
lineformatlist = deepcopy(colorlist)
for f in lineformatlist:
    f["linestyle"]="-"

#linedotformatlist
linedotformatlist = deepcopy(dotformatlist)
for f in linedotformatlist:
    f['linestyle']="-"


assignformat = {"dot": dotformatlist, "line-dot": linedotformatlist, "line": lineformatlist}

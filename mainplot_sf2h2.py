import matplotlib.pyplot as plt
import numpy as np
import argparse
from copy import deepcopy
import os,sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from formatlist import generateformat


def drawHist(heights,bounds=None, hnum=20,xlabel="x", ylabel="y",title=""):
    plt.hist(heights, hnum, align='mid',range=bounds)
    plt.title(title)
    plt.xlabel(xlabel, fontsize = 16)
    plt.ylabel(ylabel, fontsize = 16)
    plt.tick_params(direction="in")

def addline(x, y, form:dict, label=None, formatindicator="line-dot",c=None):
    if formatindicator == "dot":
        # plt.scatter(x,y,c=form["c"], edgecolors=form["ec"], s=10, marker=form["marker"], label=label)
        plt.scatter(x,y,c=y,cmap="jet",vmin=4.0,vmax=6.0,s=10, marker=form["marker"], label=label)
        # plt.scatter(x,y,c=y,cmap="bwr",vmin=1.5,vmax=2.5 ,s=2.5, marker=form["marker"], label=label)
    elif formatindicator == "line-dot":
        plt.plot(x,y,c=form["ec"], linestyle=form["linestyle"], marker=form["marker"], markerfacecolor=form["c"], markersize=5, label=label)
    elif formatindicator == "line":
        plt.plot(x,y,c=form["c"], linestyle=form["linestyle"], label=label)
    elif formatindicator == "hist":
	    plt.hist(x, y, align='mid',range=(0,1))
    elif formatindicator == "bar":
	    plt.bar(x, y)

def startfig(size = (5,5)):
    plt.rcParams["figure.figsize"] = size
    plt.rcParams['axes.linewidth'] =2.0
    plt.rcParams['xtick.major.width'] =2.0
    plt.rcParams['ytick.major.width'] =2.0

def setfigform_simple(xlabel, ylabel):
    plt.legend(fontsize = 16, frameon=False)
    font={'family':'serif',
          # 'style':'italic',  # 斜体
          'weight':'normal',
          # 'color':'red',
          'size': 18
    }
    plt.xlabel(xlabel, fontdict = font)
    plt.ylabel(ylabel, fontdict = font)
    plt.xticks(fontsize = font['size'], fontname = "serif")
    plt.yticks(fontsize = font['size'], fontname = "serif")
    plt.tick_params(direction="in")

def setfigform(xtickList, ytickList, xlabel, ylabel, title = "", xlimit = None, ylimit=None, legend = False):
    if legend:
        plt.legend(fontsize = 16, frameon=False)
    font={'family':'serif',
          # 'style':'italic',  # 斜体
          'weight':'normal',
          # 'color':'red',
          'size': 20
    }
    plt.title(title)
    print("labels:",xlabel,ylabel)
    plt.xlabel(xlabel, fontdict = font)
    plt.ylabel(ylabel, fontdict = font)
    xtickround = np.round(xtickList, 4)
    ytickround = np.round(ytickList, 4)
    # xtickround = xtickList
    # ytickround = ytickList
    print("ticks")
    print(xtickround)
    print(ytickround)
    plt.xticks( xtickround, fontsize = font['size'], fontname = "serif")
    plt.yticks( ytickround, fontsize = font['size'], fontname = "serif")
    if xlimit is not None:
        plt.xlim(xlimit)
    if ylimit is not None:
        plt.ylim(ylimit)
    plt.tick_params(direction="in")
    

def getmaxmin(data, dtype = float):
    tmpdata = np.copy(data)
    max_data = np.reshape(tmpdata, [-1]).max()
    min_data = np.reshape(tmpdata, [-1]).min()
    return max_data, min_data

def readcontext(context, item_col, skiprows=1):
    c_ = np.loadtxt(context, dtype="str", skiprows=skiprows)
    c = np.transpose(c_)
    x = c[item_col[0]].astype(np.float)
    y = []
    for i in item_col[1:]:
        _y = c[i].astype(np.float)
        y.append(_y)
    '''
    x = np.arange(0, len(c), 1)
    print("x = ",x)
    y = [c[x].astype(np.float)]
    print("y = ",y)
    '''
    y = np.array(y)
    y[np.isnan(y)] = 0
    y[np.isinf(y)] = 0
    return x,y

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Figure texts')
    parser.add_argument('--title', type=str, default='', help='titile of the figure')
    parser.add_argument('--skip', type=int, default=0, help='skip columes')
    parser.add_argument('--headerskip', type=int, default=0, help='skip columes')
    parser.add_argument('--skiprows', type=int, default=1, help="skip rows")
    parser.add_argument('--num_y', type=int, default=1, help="number of y")
    parser.add_argument('--xlabel', type=str, default="x", help="xlabel")
    parser.add_argument('--ylabel', type=str, default="y", help="ylabel")
    parser.add_argument('INPUT', type=str,
                                 help="input file")
    parser.add_argument('--format', type=str, default='line-dot', help="Format of plots: line, line-dot, dot")
    parser.add_argument("--diagonal_line", type=bool, default=False, help="Add diagonal line")
    parser.add_argument("--horizontal_line", type=float, default=None, help="Add horizontal line")
    parser.add_argument("--logx", type=bool, default=False, help="log scale of x axis")
    parser.add_argument("--logy", type=bool, default=False, help="log scale of y axis")
    parser.add_argument("--natom", type=float, default=1, help="natom")
    parser.add_argument("--xmax", type=float, default=None, help="")
    parser.add_argument("--xmin", type=float, default=None, help="")
    parser.add_argument("--ymax", type=float, default=None, help="")
    parser.add_argument("--ymin", type=float, default=None, help="")
    parser.add_argument("--singlecolor", type=bool, default=False, help="use single color")
    parser.add_argument("--item", type=str, default=None)
    parser.add_argument("--legend", type=bool, default=False)
    args = parser.parse_args()
    
    args.format="dot"
    args.headerskip=2
    args.item="time,SFpbc_h3"
    # args.item="time,sf2h2"

    formatindicator = args.format
    
    inputfile = args.INPUT
    with open(inputfile) as f:
        header = f.readline().split()
    if args.item is not None:
        items = args.item.split(",")
    else:
        items = []
    item_col = []
    for i in items:
        item_col.append( header.index(i)-args.headerskip)
    print(item_col)
    
    # num_y = args.num_y
    num_y = len(items)-1
    skiprows = args.skiprows
    skip_y = args.skip
    natom = [args.natom]*num_y
    
    
    fin = open(inputfile, "r")
    x, _y= readcontext(fin, item_col, skiprows=skiprows)

    # x = x/1000000
    y = deepcopy(_y)
    for j in range(num_y):
        for i in range(y.shape[-1]):
            y[j][i] = (_y[j][i] )/natom[j]
           

    print(x)
    print(y)

    startfig((5,5))

    assignformat = generateformat(len(y), singlecolor=args.singlecolor)
    if args.item is not None:
        num_y = len(item_col)-1
        labellist = items[1:]
    else:
        num_y = len(header)
        labellist = [" " for i in range(len(y))]
    for i in range(1):
        form = assignformat[formatindicator]
        addline(x,y[i], form[i],labellist[i],formatindicator=formatindicator)
    
    if args.logx:
        plt.semilogx()
    if args.logy:
        plt.semilogy()
    max_x, min_x = getmaxmin(x)
    max_y, min_y = getmaxmin(y)
    #max_x = max_x + (max_x - min_x)*0.5
    #min_x = min_x - (max_x - min_x)*0.5
    print((min_x, min_y))
    print((max_x, max_y))
    if args.horizontal_line is not None:
        min_y = min(min_y, args.horizontal_line)
        max_y = max(max_y, args.horizontal_line)
    if args.xmax is not None:
        max_x = args.xmax
    if args.xmin is not None:
        min_x = args.xmin
    if args.ymax is not None:
        max_y = args.ymax
    if args.ymin is not None:
        min_y = args.ymin
    max_y=8
    min_y=1.5
    print((min_x, min_y))
    print((max_x, max_y))
    xtickList = (max_x-min_x) * np.arange(-0.2, 1.4, 0.4) + min_x
    ytickList = (max_y-min_y) * np.arange(-0.2, 1.4, 0.1) + min_y

    if args.item is not None:
        setfigform(xtickList, ytickList, xlabel = items[0], ylabel = ",".join(items[1:]), xlimit=(min_x,max_x), ylimit=(min_y,max_y), title = args.title, legend = args.legend)
    # setfigform_simple(xlabel = args.xlabel, ylabel = args.ylabel)
    # add diagonal line
    if args.diagonal_line:
        plt.plot((min_x, max_x), (min_y, max_y), ls="--", c="k")
    if args.horizontal_line is not None:
        plt.plot((min_x, max_x), (args.horizontal_line, args.horizontal_line), ls="--", c="r")
    # plt.plot((min_x, max_x), (1.0, 1.0), ls="--", c="k")
    
    if args.item is not None:
        plt.savefig("-".join(items[1:])+"-"+items[0]+".png", bbox_inches = "tight")
    else:
        plt.savefig("fig")
    plt.show()
    

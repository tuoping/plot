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

def addline(x, y, yerr, form:dict, label=None, formatindicator="line-dot", ecolor = "grey"):
    lines = {'linestyle': 'None'}
    plt.rc('lines', **lines)
    print(form)
    plt.errorbar(x,y,yerr=yerr, marker = form["marker"], c=form["c"], markersize=5., label=label, ecolor=ecolor, capsize=2)

def startfig(size = (5,5)):
    plt.rcParams["figure.figsize"] = size
    plt.rcParams['axes.linewidth'] =2.0
    plt.rcParams['xtick.major.width'] =2.0
    plt.rcParams['ytick.major.width'] =2.0

def setfigform(xtickList, ytickList, xlabel, ylabel, title = "", xlimit = None, ylimit=None):
    # plt.legend(fontsize = 16, frameon=False)
    font={'family':'serif',
          # 'style':'italic',  # 斜体
          'weight':'normal',
          # 'color':'red',
          'size': 18
    }
    plt.title(title)
    plt.xlabel(xlabel, fontdict = font)
    plt.ylabel(ylabel, fontdict = font)
    xtickround = np.round(xtickList, 0)
    plt.xticks(xtickround, fontsize = font['size'], fontname = "serif")
    plt.yticks(fontsize = font['size'], fontname = "serif")
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
    x = c[item_col[0]].astype(float)
    # x = np.arange(c.shape[1])
    y = []
    for i in item_col[1:]:
        _y = c[i].astype(float)
        y.append(_y)
    y = np.array(y)
    y[np.isnan(y)] = 0
    y[np.isinf(y)] = 0
    return x,y

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Figure texts')
    parser.add_argument('--title', type=str, default='', help='titile of the figure')
    parser.add_argument('--skiprows', type=int, default=0, help="skip rows")
    parser.add_argument('--headerskip', type=int, default=0, help='skip columes')
    parser.add_argument("--item", type=str, default=None)
    parser.add_argument('--xlabel', type=str, default="x", help="xlabel")
    parser.add_argument('--ylabel', type=str, default="y", help="ylabel")
    parser.add_argument("--xmax", type=float, default=None, help="")
    parser.add_argument("--xmin", type=float, default=None, help="")
    parser.add_argument("--ymax", type=float, default=None, help="")
    parser.add_argument("--ymin", type=float, default=None, help="")
    parser.add_argument('INPUT', type=str, nargs = "+",
                                 help="input file")
    parser.add_argument('--format', type=str, default='line-dot', help="Format of plots: line, line-dot, dot")
    parser.add_argument("--diagonal_line", type=bool, default=False, help="Add diagonal line")
    parser.add_argument("--logx", type=bool, default=False, help="log scale of x axis")
    parser.add_argument("--logy", type=bool, default=False, help="log scale of y axis")
    parser.add_argument("--singlecolor", type=bool, default=False, help="log scale of y axis")
    parser.add_argument("--natom", type=str, default=None, help="natom")
    args = parser.parse_args()
    
    formatindicator = args.format
    
    inputfile = args.INPUT
    if args.item is not None:
        items = args.item.split(",")
    else:
        items = []
    
    num_y = (len(items)-1)
    skiprows = args.skiprows
    
    if args.natom is not None:
        natom = [float(x) for x in args.natom.split(",")]*len(inputfile)
    else:
        natom = [1.]*num_y*len(inputfile)+[1.]
    print("natom = ", natom)
    
    skiprows = args.skiprows
    x = []
    y = []
    for f in inputfile:
        fin = open(f, "r")
        header = fin.readline().split()
        item_col = []
        for i in items:
            item_col.append( header.index(i)-args.headerskip)
        print(item_col)
        x1, y1 = readcontext(fin, item_col, skiprows = skiprows)
        x.append((x1)/natom[0])
        for i in range(len(y1[0])):
            for j in range(num_y):
                y1[j][i] = (y1[j][i])/natom[j+1]
        y.append(y1)
    
    
    maxxlist = []
    minxlist = []
    maxylist = []
    minylist = []
    for i_file in range(len(x)):
        max_x, min_x = getmaxmin(x[i_file])
        max_y, min_y = getmaxmin(y[i_file][0:int(num_y/2)])
        maxxlist.append(max_x)
        minxlist.append(min_x)
        maxylist.append(max_y)
        minylist.append(min_y)
    max_x = max(maxxlist)
    min_x = min(minxlist)
    max_y = max(maxylist)
    min_y = min(minylist)
    min_x = min_x # - 0.1 * (max_x-min_x)
    max_x = max_x # + 0.1 * (max_x-min_x)
    min_y = min_y - 1.0 * (max_y-min_y)
    max_y = max_y + 1.0 * (max_y-min_y)
    print((min_x, min_y))
    print((max_x, max_y))
    xtickList = (max_x-min_x) * np.arange(-0.2, 1.4, 0.2) + min_x
    ytickList = (max_y-min_y) * np.arange(-0.2, 1.4, 0.2) + min_y
    startfig((5,5))

    # labellist = [" " for i in range(len(y))]
    # assignformat = generateformat(len(y), singlecolor=args.singlecolor)
    # for i in range(0,num_y):
    #     form = assignformat[formatindicator]
    #     addline(x,y[i],y[i+num_y], form[i],labellist[i],formatindicator=formatindicator, ecolor = ecolor[i])
    labellist = [" " for i in range(len(x)*num_y)]
    assignformat = generateformat(len(x)*num_y, singlecolor=args.singlecolor)
    ptr = 0
    ecolor = ["grey", "pink","lightblue"]
    for i_file in range(len(inputfile)):
        for i in range(int(num_y/2)):
            form = assignformat[formatindicator]
            addline(x[i_file],y[i_file][i],y[i_file][i+int(num_y/2)], form[ptr], labellist[ptr], formatindicator=formatindicator, ecolor = ecolor[i])
            ptr += 1
    
    setfigform(xtickList, ytickList, xlabel = items[0], ylabel = ",".join(items[1:]), xlimit=(min_x,max_x), ylimit=(min_y,max_y), title = args.title)
    # add diagonal line
    if args.diagonal_line:
        plt.plot((min_x, max_x), (min_y, max_y), ls="--", c="k")
    # plt.plot((min_x, max_x), (1.0, 1.0), ls="--", c="k")
    
    if args.logx:
        plt.semilogx()
    if args.logy:
        plt.semilogy()
    
    if args.item is not None:
        plt.savefig("-".join(items[1:])+"-"+items[0]+".png", bbox_inches = "tight")
    else:
        plt.savefig("fig")
    plt.show()
    

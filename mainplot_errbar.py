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
    xtickround = np.round(xtickList, 2)
    ytickround = np.round(ytickList, 2)
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

def readcontext(context, num_y=1, skip_y=0, skiprows=0):
    c_ = np.loadtxt(context, dtype="str", skiprows=skiprows)
    c = np.transpose(c_)
    x = c[0].astype(np.float)
    y = c[skip_y+1:skip_y+num_y+1].astype(np.float)
    return x,y

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Figure texts')
    parser.add_argument('--title', type=str, default='', help='titile of the figure')
    parser.add_argument('--skip', type=int, default=0, help='skip columes')
    parser.add_argument('--skiprows', type=int, default=0, help="skip rows")
    parser.add_argument('--num_y', type=int, default=1, help="number of y")
    parser.add_argument('--xlabel', type=str, default="x", help="xlabel")
    parser.add_argument('--ylabel', type=str, default="y", help="ylabel")
    parser.add_argument('INPUT', type=str, nargs = "+",
                                 help="input file")
    parser.add_argument('--format', type=str, default='line-dot', help="Format of plots: line, line-dot, dot")
    parser.add_argument("--diagonal_line", type=bool, default=False, help="Add diagonal line")
    parser.add_argument("--logx", type=bool, default=False, help="log scale of x axis")
    parser.add_argument("--logy", type=bool, default=False, help="log scale of y axis")
    parser.add_argument("--singlecolor", type=bool, default=False, help="log scale of y axis")
    parser.add_argument("--natom", type=float, default=1, help="natom")
    args = parser.parse_args()
    
    formatindicator = args.format
    
    inputfile = args.INPUT
    
    num_y = args.num_y
    skiprows = args.skiprows
    skip_y = args.skip
    
    
    x = []
    y = []
    for f in inputfile:
        fin = open(f, "r")
        x1, y1 = readcontext(fin, num_y=num_y*2, skip_y=skip_y, skiprows = skiprows)
        x.append(x1)
        for j in range(num_y):
            for i in range(len(y1[j])):
                y1[j][i] /= args.natom
                y1[j][i] = np.abs(y1[j][i])
        y.append(y1)
    #fin = open(inputfile, "r")
    #x, y = readcontext(fin, num_y=num_y*2, skip_y=skip_y, skiprows=skiprows)

    
    print(x)
    print(y)
    for yi in y:
        print(yi)
    print("\n")
    
    
    maxxlist = []
    minxlist = []
    maxylist = []
    minylist = []
    for i_file in range(len(x)):
        max_x, min_x = getmaxmin(x[i_file])
        max_y, min_y = getmaxmin(y[i_file])
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
    min_y = min_y - 0.1 * (max_y-min_y)
    max_y = max_y + 0.1 * (max_y-min_y)
    min_y=0
    print((min_x, min_y))
    print((max_x, max_y))
    xtickList = np.arange(20,500,100)
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
        for i in range(num_y):
            form = assignformat[formatindicator]
            addline(x[i_file],y[i_file][i],y[i_file][i+num_y], form[ptr], labellist[ptr], formatindicator=formatindicator, ecolor = ecolor[i])
            ptr += 1
    
    setfigform(xtickList, ytickList, xlabel = args.xlabel, ylabel = args.ylabel, xlimit=(min_x,max_x), ylimit=(min_y,max_y), title = args.title)
    # add diagonal line
    if args.diagonal_line:
        plt.plot((min_x, max_x), (min_y, max_y), ls="--", c="k")
    # plt.plot((min_x, max_x), (1.0, 1.0), ls="--", c="k")
    
    if args.logx:
        plt.semilogx()
    if args.logy:
        plt.semilogy()
    
    plt.savefig("fig", dpi=1100, bbox_inches = "tight")
    plt.show()
    

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

def addline(x, y, form:dict, label=None, formatindicator="line-dot"):
    if formatindicator == "dot":
        plt.scatter(x,y,c=form["c"], edgecolors=form["ec"], s=50, marker=form["marker"], label=label)
    elif formatindicator == "line-dot":
        plt.plot(x,y,c=form["ec"], linestyle=form["linestyle"], marker=form["marker"], markerfacecolor=form["c"], markersize=8, label=label)
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

def setfigform(xtickList, ytickList, xlabel, ylabel, title = "", xlimit = None, ylimit=None):
    # plt.legend(fontsize = 16, frameon=False)
    font={'family':'serif',
          # 'style':'italic',  # 斜体
          'weight':'normal',
          # 'color':'red',
          'size': 16
    }
    plt.title(title)
    plt.xlabel(xlabel, fontdict = font)
    plt.ylabel(ylabel, fontdict = font)
    xtickround = np.round(xtickList, 3)
    ytickround = np.round(ytickList, 3)
    #xtickround = xtickList
    #ytickround = ytickList
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

def readcontext(context, num_y=1, skip_y=0, skiprows=0):
    c_ = np.loadtxt(context, dtype="str", skiprows=skiprows)
    c = np.transpose(c_)
    x = c[0].astype(np.float)
    y = c[skip_y+1:skip_y+num_y+1].astype(np.float)
    # y = np.array([c[1]]).astype(np.float) - np.array([c[3]]).astype(np.float)
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
    parser.add_argument("--natom", type=float, default=1, help="natom")
    parser.add_argument("--singlecolor", type=bool, default=False, help="use single color")
    args = parser.parse_args()
    
    # formatindicator = args.format
    formatindicator = "dot"
    
    inputfile = args.INPUT
    
    num_y = args.num_y
    skiprows = 1
    skip_y = args.skip
    natom=[args.natom]*len(inputfile)
    
    
    x = []
    y = []
    idx_f = 0
    for f in inputfile:
        fin = open(f, "r")
        x1, y1 = readcontext(fin, num_y=num_y, skip_y=skip_y, skiprows = skiprows)
        x.append(x1/natom[idx_f])
        for i in range(len(y1[0])):
            for j in range(num_y):
                y1[j][i] = (y1[j][i])/natom[idx_f]
        y.append(y1)
        idx_f += 1


    print(y)

    plt.figure(figsize=(5,5))
    labellist = [" " for i in range(len(x)*num_y)]
    assignformat = generateformat(len(x)*num_y)
    ptr = 0
    for i_file in range(len(x)):
        for i in range(num_y):
            form = assignformat[formatindicator]
            addline(x[i_file],y[i_file][i], form[ptr], labellist[ptr], formatindicator=formatindicator)
            ptr += 1
    
    if args.logx:
        plt.semilogx()
    if args.logy:
        plt.semilogy()
    max_x, min_x = getmaxmin(x)
    max_y, min_y = getmaxmin(y)
    #min_x = min_x - 0.1 * (max_x - min_x)
    #max_x = max_x + 0.1 * (max_x - min_x)
    min_x = min(min_x, min_y)
    max_x = max(max_x, max_y)
    min_x = min_x - 0.1 * (max_x - min_x)
    max_x = max_x + 0.1 * (max_x - min_x)
    xtickList = (max_x-min_x) * np.arange(-0.3, 1.4, 0.3) + min_x
    ytickList = xtickList
    min_y = min_x
    max_y = max_x

    setfigform(xtickList, ytickList, xlabel = args.xlabel, ylabel = args.ylabel, xlimit=(min_x,max_x), ylimit=(min_y,max_y), title = args.title)
    # setfigform_simple(xlabel = args.xlabel, ylabel = args.ylabel)
    # add diagonal line
    # if args.diagonal_line:
    plt.plot((min_x, max_x), (min_y, max_y), ls="--", c="k")
    # plt.plot((min_x, max_x), (1.0, 1.0), ls="--", c="k")
    
    plt.savefig("fig", bbox_inches = "tight")
    plt.show()
    

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
        plt.scatter(x,y,c=form["c"], s=3, marker=form["marker"], label=label)
    elif formatindicator == "line-dot":
        plt.plot(x,y,c=form["c"], linestyle=form["linestyle"], marker=form["marker"], markersize=3, label=label)
    elif formatindicator == "line":
        plt.plot(x,y,c=form["c"], linestyle=form["linestyle"], label=label)
    elif formatindicator == "hist":
	    pyplot.hist(x, y, align='mid',range=(0,1))

def startfig(size = (5,5)):
    plt.rcParams["figure.figsize"] = size
    plt.rcParams['axes.linewidth'] =2.0
    plt.rcParams['xtick.major.width'] =2.0
    plt.rcParams['ytick.major.width'] =2.0

def setfigform(xtickList, ytickList, xlabel, ylabel, title = "", xlimit = None, ylimit=None):
    #plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.15)
    plt.legend(fontsize = 16, frameon=False)
    #plt.title(title,fontsize = 16)
    #plt.xlabel(xlabel,fontsize = 18)
    #plt.ylabel(ylabel, fontsize = 18)
    font={'family':'Times New Roman',
          # 'style':'italic',  # 斜体
          'weight':'normal',
          # 'color':'red',
          'size': 16
    }
    plt.title(title)
    plt.xlabel(xlabel, fontsize = font["size"])
    plt.ylabel(ylabel, fontsize = font["size"])
    xtickround = np.round(xtickList, 3)
    ytickround = np.round(ytickList, 3)
    plt.xticks( xtickround, fontsize = font["size"])
    plt.yticks( ytickround, fontsize = font["size"])
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
    # x = c[0].astype(np.float)
    x = c[1].astype(np.float)
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
    parser.add_argument('INPUT', type=str,
                                 help="input file")
    parser.add_argument('--format', type=str, default='line-dot', help="Format of plots: line, line-dot, dot")
    parser.add_argument("--diagonal_line", type=bool, default=False, help="Add diagonal line")
    parser.add_argument("--logx", type=bool, default=False, help="log scale of x axis")
    parser.add_argument("--logy", type=bool, default=False, help="log scale of y axis")
    args = parser.parse_args()
    
    formatindicator = args.format
    
    inputfile = args.INPUT
    
    num_y = args.num_y
    skiprows = args.skiprows
    skip_y = args.skip
    
    
    fin = open(inputfile, "r")
    x, y = readcontext(fin, num_y=num_y, skip_y=skip_y, skiprows=skiprows)

    
    print(x)
    print(y)
    for yi in y:
        print(yi)
    print("\n")
    
    
    max_x, min_x = getmaxmin(x)
    max_y, min_y = getmaxmin(y)
    print((min_x, min_y))
    print((max_x, max_y))
    #xtickList = (max_x-min_x) * np.arange(-0.2, 1.2, 0.2) + min_x
    xtickList = np.arange(50, 350, 50)
    ytickList = (max_y-min_y) * np.arange(-0.2, 1.2, 0.2) + min_y
    startfig((5,5))

    labellist = [" " for i in range(len(y))]
    assignformat = generateformat(len(y))
    for i in range(num_y):
        form = assignformat[formatindicator]
        addline(x,y[i],form[i],labellist[i],formatindicator=formatindicator)
    
    setfigform(xtickList, ytickList, xlabel = args.xlabel, ylabel = args.ylabel, xlimit=(min_x,max_x), ylimit=(min_y,max_y), title = args.title)
    # add diagonal line
    if args.diagonal_line:
        plt.plot((min_x, max_x), (min_y, max_y), ls="--", c="k")
    
    if args.logx:
        plt.semilogx()
    if args.logy:
        plt.semilogy()
    
    plt.savefig("fig", dpi=1100, bbox_inches = "tight")
    plt.show()
    

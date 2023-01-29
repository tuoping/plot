import matplotlib.pyplot as plt
import numpy as np
import argparse
from copy import deepcopy
import os,sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from formatlist import generateformat
from plotfunctions import addline, setfigform, getmaxmin, readcontext, startfig


def readcontextrows(context, skip_y=0, skiprows=0):
    c_ = np.loadtxt(context, dtype="str", skiprows=skiprows)
    if len(c_.shape) == 1:
        c_ = c_[np.newaxis, :]
    y = c_[np.arange(0, len(c_), skip_y)].astype(np.float)
    return y

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Figure texts')
    parser.add_argument('--title', type=str, default='', help='titile of the figure')
    parser.add_argument('--skip', type=int, default=1, help='skip columes')
    parser.add_argument('--skiprows', type=int, default=1, help="skip rows")
    parser.add_argument('--num_y', type=int, default=1, help="number of y")
    parser.add_argument('--xlabel', type=str, default="x", help="xlabel")
    parser.add_argument('--ylabel', type=str, default="y", help="ylabel")
    parser.add_argument('INPUT', type=str, nargs = "+",
                                 help="input file")
    parser.add_argument('--format', type=str, default='line-dot', help="Format of plots: line, line-dot, dot")
    parser.add_argument("--diagonal_line", type=bool, default=False, help="Add diagonal line")
    parser.add_argument("--logx", type=bool, default=False, help="log scale of x axis")
    parser.add_argument("--logy", type=bool, default=False, help="log scale of y axis")
    parser.add_argument("--xmax", type=float, default=None, help="")
    parser.add_argument("--xmin", type=float, default=None, help="")
    parser.add_argument("--ymax", type=float, default=None, help="")
    parser.add_argument("--ymin", type=float, default=None, help="")
    args = parser.parse_args()
    
    formatindicator = args.format
    
    inputfile = args.INPUT
    
    num_y = args.num_y
    skiprows = args.skiprows
    skip_y = args.skip
    
    
    y = []
    for i in range(len(inputfile)):
       fin = open(inputfile[i], "r")
       y_ = readcontextrows(fin, skip_y=skip_y, skiprows=skiprows)
       print(y_)
       for i in range(len(y_)):
           y.append(y_[i][1:])
    x = 0.01*np.arange(len(y[0]))+3.0
    
    print("x=", x)
    #print(y)
    #print("\n")
    
    
    max_x, min_x = getmaxmin(np.array(x))
    max_y, min_y = getmaxmin(np.array(y))
    if args.xmax is not None:
        max_x = args.xmax
    if args.xmin is not None:
        min_x = args.xmin
    if args.ymax is not None:
        max_y = args.ymax
    if args.ymin is not None:
        min_y = args.ymin
    print((min_x, min_y))
    print((max_x, max_y))
    # xtickList = (max_x-min_x) * np.arange(0, 1.2, 0.2) + min_x
    xtickList = np.arange(3, max_x+0.1, (max_x-3)/10)
    ytickList = (max_y-min_y) * np.arange(0, 1.2, 0.2) + min_y
    startfig((5,5))

    labellist = [" " for i in range(len(y))]
    assignformat = generateformat(len(y))
    for i in range(len(y)):
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
    
    plt.savefig("fig", bbox_inches = "tight")
    plt.show()
    

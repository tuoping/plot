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
           y.append(y_[i][2:])
    x=[273.598,274.977,276.37,277.778,279.2,280.636,282.087,283.554,285.036,286.533,288.046,289.575,291.121,292.683,294.262,295.858,297.471,299.103,300.752,302.419,304.105,305.81,307.535,309.278,311.042,312.826,314.63,316.456,318.302,320.171,322.061,323.974,325.91,327.869,329.852,331.858,333.89,335.946,338.028,340.136,342.27,344.432,346.62,348.837,351.083,353.357,355.661,357.995,360.36,362.757,365.186,367.647,370.142,372.671,375.235,377.834,380.469,383.142,385.852,388.601,391.389,394.218,397.088,400]
    x = 0.01*np.arange(len(y[0]))+3.0
    
    print("x=", x)
    # print("y=", y)
    # print("\n")
    y = np.array(y)
    print("DIM of y =", y.shape)
    
    
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
    xtickList = (max_x-min_x) * np.arange(0, 1.2, 0.4) + min_x
    ytickList = (max_y-min_y) * np.arange(0, 1.2, 0.2) + min_y
    startfig((5,5))

    labellist = [" " for i in range(len(y))]
    assignformat = generateformat(len(y))
    for i in range(len(y)):
        print(i)
        form = assignformat[formatindicator]
        addline(x,y[i],form[i],labellist[i],formatindicator=formatindicator)
    
    setfigform(xtickList, ytickList, xlabel = "kBT", ylabel = args.ylabel, xlimit=(min_x,max_x), ylimit=(min_y,max_y), title = args.title)
    # add diagonal line
    if args.diagonal_line:
        plt.plot((min_x, max_x), (min_y, max_y), ls="--", c="k")
    
    if args.logx:
        plt.semilogx()
    if args.logy:
        plt.semilogy()
    
    plt.savefig("fig", bbox_inches = "tight")
    plt.show()
    

import matplotlib.pyplot as plt
import numpy as np
import argparse
from copy import deepcopy
import os,sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from formatlist import generateformat
from plotfunctions import addline, setfigform, getmaxmin, readcontext, drawHist, startfig
import seaborn as sns


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Figure texts')
    parser.add_argument('--title', type=str, default='', help='titile of the figure')
    parser.add_argument('--skip', type=int, default=0, help='skip columes')
    parser.add_argument('--skiprows', type=int, default=1, help="skip rows")
    parser.add_argument('--xlabel', type=str, default="x", help="xlabel")
    parser.add_argument('--ylabel', type=str, default="y", help="ylabel")
    parser.add_argument('INPUT', type=str, nargs = "+",
                                 help="input file")
    parser.add_argument('--format', type=str, default='line-dot', help="Format of plots: line, line-dot, dot")
    parser.add_argument("--diagonal_line", type=bool, default=False, help="Add diagonal line")
    parser.add_argument("--logx", type=bool, default=False, help="log scale of x axis")
    parser.add_argument("--logy", type=bool, default=False, help="log scale of y axis")
    args = parser.parse_args()
    
    formatindicator = args.format
    
    inputfile = args.INPUT
    print("Number of inputfiles = ", len(inputfile))
    
    skiprows = args.skiprows
    skip_y = args.skip
    
    
    y = []
    for inputf in inputfile:
        fin = open(inputf, "r")
        fc = np.loadtxt(fin, skiprows=skiprows).T
        if len(fc.shape) == 1:
            fc = np.reshape(fc, [1,-1])
        for i in range(skip_y, skip_y+1):
            y1 = fc[i]
            y.append(y1)
        fin.close()
    
    
    
    maxylist = []
    minylist = []
    # for i_file in range(len(inputfile)):
    for i_file in range(len(inputfile)):
        max_y, min_y = getmaxmin(y[i_file])
        maxylist.append(max_y)
        minylist.append(min_y)
    max_y = max(maxylist)
    min_y = min(minylist)
    ytickList = (max_y-min_y) * np.arange(0, 1.2, 0.2) + min_y
    startfig((5,5))

    assignformat = generateformat(len(y))
    form = assignformat["dot"]
    bounds = None
    for i in range(len(inputfile)):
        print("Averages and standard_err:: ")
        # drawHist(y[i], bounds=(min_y,max_y), hnum=50, xlabel = args.xlabel, ylabel=args.ylabel, title = args.title)
        sns.kdeplot(y[i], label=inputfile[i], color=form[i]["c"])
        print(np.average(y[i]), np.std(y[i]))
    
    #setfigform(xtickList, ytickList, xlabel = args.xlabel, ylabel = args.ylabel, ylimit=(min_y,max_y), title = args.title)
    # add diagonal line
    if args.diagonal_line:
        plt.plot((min_x, max_x), (min_y, max_y), ls="--", c="k")
    
    if args.logx:
        plt.semilogx()
    if args.logy:
        plt.semilogy()
    
    plt.savefig("distrib.png", dpi=1100, bbox_inches = "tight")
    plt.show()
    

import matplotlib.pyplot as plt
import numpy as np
import argparse
from copy import deepcopy
import os,sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from formatlist import generateformat
from plotfunctions import addline, setfigform, getmaxmin, readcontext


if __name__ == "__main__":

    labellist = [" ", " ", " ", " ", " "]
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
    
    natom = [args.natom]*len(inputfile)
    
    x = []
    y = []
    idx_f = 0
    for f in inputfile:
        fin = open(f, "r")
        x1, y1 = readcontext(fin, num_y=num_y, skip_y=skip_y, skiprows = skiprows)
        x.append(x1)
        for i in range(len(y1[0])):
            for j in range(num_y):
                y1[j][i] = (y1[j][i])/natom[idx_f]
        y.append(y1)
        idx_f += 1


    plt.figure(figsize=(5,5))
    labellist = [" " for i in range(len(x)*num_y)]
    assignformat = generateformat(len(x)*num_y)
    ptr = 0
    for i_file in range(len(x)):
        print(x[i_file])
        for yi in y[i_file]:
            print(yi)
        print("\n")
        for i in range(num_y):
            form = assignformat[formatindicator]
            addline(x[i_file],y[i_file][i], form[ptr], labellist[ptr], formatindicator=formatindicator)
            ptr += 1
    
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
    xtickList = (max_x-min_x) * np.arange(0, 1.1, 0.2) + min_x
    # xtickList = np.arange(50,500,100)
    ytickList = (max_y-min_y) * np.arange(0, 1.2, 0.1) + min_y
    # ytickList = np.arange(0.0, 1.23, 0.04)
    print(ytickList)
    
    if args.logy:
        setfigform(xtickList, ytickList, xlabel = args.xlabel, ylabel = args.ylabel, xlimit=(min_x, max_x), title = args.title)
    else:
        setfigform(xtickList, ytickList, xlabel = args.xlabel, ylabel = args.ylabel, xlimit=(min_x, max_x), ylimit=(min_y, max_y), title = args.title)
    # add diagonal line
    if args.diagonal_line:
        plt.plot((min_x, max_x), (min_y, max_y), ls="--", c="k")
    
    if args.logx:
        plt.semilogx()
    if args.logy:
        plt.semilogy()
    
    plt.savefig("fig", bbox_inches = "tight")
    plt.show()
    

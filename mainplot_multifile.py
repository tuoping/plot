import matplotlib.pyplot as plt
import numpy as np
import argparse
from copy import deepcopy
import os,sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from formatlist import generateformat
from plotfunctions import addline, setfigform, getmaxmin, readcontext, startfig


if __name__ == "__main__":

    labellist = [" ", " ", " ", " ", " "]
    parser = argparse.ArgumentParser(description='Figure texts')
    parser.add_argument('--title', type=str, default='', help='titile of the figure')
    parser.add_argument('--skip', type=int, default=0, help='skip columes')
    parser.add_argument('--headerskip', type=int, default=0, help='skip columes')
    parser.add_argument('--skiprows', type=int, default=1, help="skip rows")
    parser.add_argument('--num_y', type=int, default=1, help="number of y")
    parser.add_argument('--xlabel', type=str, default="x", help="xlabel")
    parser.add_argument('--ylabel', type=str, default="y", help="ylabel")
    parser.add_argument('INPUT', type=str, nargs = "+",
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
    args = parser.parse_args()
    
    formatindicator = args.format
    
    inputfile = args.INPUT
    if args.item is not None:
        items = args.item.split(",")
    else:
        items = []
    # with open(inputfile[0]) as f:
    #     header = f.readline().split()
    # item_col = []
    # for i in items:
    #     item_col.append( header.index(i)-args.headerskip)
    # print(item_col)
    
    num_y = args.num_y
    skiprows = args.skiprows
    skip_y = args.skip
    
    natom = [args.natom]*len(inputfile)
    
    x = []
    y = []
    idx_f = 0
    for f in inputfile:
        fin = open(f, "r")
        header = fin.readline().split()
        item_col = []
        for i in items:
            item_col.append( header.index(i)-args.headerskip)
        print(item_col)
        x1, y1 = readcontext(fin, item_col, skiprows = skiprows)
        x.append(x1)
        for i in range(len(y1[0])):
            for j in range(num_y):
                y1[j][i] = (y1[j][i])/natom[idx_f]
        y.append(y1)
        idx_f += 1

    startfig((5,5))

    assignformat = generateformat(len(x)*num_y)
    if args.item is not None:
        num_y = len(item_col)-1
        labellist = items[1:]
    else:
        num_y = len(header)
        labellist = [" " for i in range(len(y))]
    ptr = 0
    for i_file in range(len(x)):
        print(x[i_file])
        for yi in y[i_file]:
            print(yi)
        print("\n")
        for i in range(num_y):
            form = assignformat[formatindicator]
            addline(x[i_file],y[i_file][i], form[ptr], None, formatindicator=formatindicator)
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
    if min_y > 0:
        min_y = min_y*(0.95)
    else:
        min_y = min_y*(1.05)
    if max_y > 0:
        max_y = max_y*(1.05)
    else:
        max_y = max_y*(0.95)
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
    xtickList = (max_x-min_x) * np.arange(-0.2, 1.4, 0.2) + min_x
    ytickList = (max_y-min_y) * np.arange(-0.2, 1.4, 0.2) + min_y

    if args.logy:
        if args.item is not None:
            setfigform(xtickList, ytickList, xlabel = items[0], ylabel = ",".join(items[1:]), xlimit=(min_x,max_x), title = args.title)
    else:
        if args.item is not None:
            setfigform(xtickList, ytickList, xlabel = items[0], ylabel = ",".join(items[1:]), xlimit=(min_x,max_x), ylimit=(min_y,max_y), title = args.title)
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
    

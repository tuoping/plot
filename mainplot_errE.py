import matplotlib.pyplot as plt
import numpy as np
import argparse
import seaborn as sns
from copy import deepcopy
import os,sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from formatlist import assignformat
from plotfunctions import addline, setfigform, getmaxmin, readcontext, bold_axis_and_ticks, plot_error_distribution, startfig

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
    parser.add_argument('--natom', type=str, default="1.0", help='y/natom')
    args = parser.parse_args()
    
    formatindicator = args.format
    
    inputfile = args.INPUT
    
    num_y = args.num_y
    skiprows = args.skiprows
    skip_y = args.skip
    if args.natom == "1.0":
        natom=np.ones(len(inputfile))
    else:
        natom = [float(a) for a in args.natom.split(",")]
    
    
    x = []
    y = []
    for i_file in range(len(inputfile)):
        f = inputfile[i_file]
        fin = open(f, "r")
        x1, y1 = readcontext(fin, num_y=num_y, skip_y=skip_y, skiprows = skiprows)
        x1 = np.array(x1)/natom[i_file]
        y1 = np.array(y1)/natom[i_file]
        x.append(x1)
        y.append(y1[0])

    
    for xi in x:
        print(len(xi))
    print("\n")
    for yi in y:
        print(len(yi))
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
    print((min_x, min_y))
    print((max_x, max_y))
    max_ = max(max_x, max_y)
    min_ = min(min_x, min_y)
    xtickList = (max_-min_) * np.arange(0, 1.3, 0.3) + min_

    plt.figure(figsize=(5,5))
    ptr = 0
    for i_file in range(len(x)):
        # print(x[i_file])
        # for yi in y[i_file]:
        #     print(yi)
        # print("\n")
        form = assignformat[formatindicator]
        addline(x[i_file],y[i_file], form[ptr], labellist[i_file], formatindicator=formatindicator)
        ptr += 1
    
    setfigform(xtickList, xtickList, xlabel = args.xlabel, ylabel = args.ylabel, title = args.title, xlimit=(min_,max_), ylimit=(min_,max_))
    # add diagonal line
    if args.diagonal_line:
        plt.plot((min_, max_), (min_, max_), ls="--", c="k")
    
    if args.logx:
        plt.semilogx()
    if args.logy:
        plt.semilogy()
    
    plt.savefig("fig", dpi=1100, bbox_inches = "tight")
    plt.show()
    
    from sklearn.metrics import mean_squared_error, r2_score
    for i_file in range(len(x)):
        print(np.sqrt(mean_squared_error(x[i_file], y[i_file])), r2_score(x[i_file], y[i_file]))
        plt = plot_error_distribution(x[i_file], y[i_file])
        plt.xlim((-0.5,0.5))
        plt.savefig("distrib")
        plt.show()

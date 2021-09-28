import matplotlib.pyplot as plt
import numpy as np
import argparse
from formatlist import assignformat
from plotfunctions import addline, setfigform, getmaxmin, readcontext


if __name__ == "__main__":
    labellist = ["100K", "200K", "300K", "400K"]

    parser = argparse.ArgumentParser(description='Figure texts')
    parser.add_argument('--title', type=str, default='', help='titile of the figure')
    parser.add_argument('--skip', type=int, default=0, help='skip columes')
    parser.add_argument('--skip_first_line', type=bool, default=True, help="skip first line")
    parser.add_argument('--num_y', type=int, default=1, help="number of y")
    parser.add_argument('--xlabel', type=str, default="x", help="xlabel")
    parser.add_argument('--ylabel', type=str, default="y", help="ylabel")
    parser.add_argument('INPUT', type=str, nargs = "+",
                                 help="input file")
    parser.add_argument('--format', type=str, default='line-dot', help="Format of plots: line, line-dot, dot")
    args = parser.parse_args()
    
    formatindicator = args.format
    
    inputfile = args.INPUT
    
    num_y = args.num_y
    skip_first_line = args.skip_first_line
    skip_y = args.skip
    
    
    x = []
    y = []
    for f in inputfile:
        fin = open(f, "r")
        context = fin.readlines()
        if skip_first_line:
            context.pop(0)
        x1, y1 = readcontext(context)
        x.append(x1)
        y.append(y1)

    ptr = 0
    for i_file in range(len(x)):
        print(x[i_file])
        for yi in y[i_file]:
            print(yi)
        print("\n")
        for i in range(num_y):
            form = assignformat[formatindicator]
            addline(x[i_file],y[i_file][i], form[ptr], labellist[i], formatindicator=formatindicator)
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
    print((min_x, min_y))
    print((max_x, max_y))
    xtickList = (max_x-min_x) * np.arange(0, 1, 0.4) + min_x
    ytickList = (max_y-min_y) * np.arange(0, 1, 0.2) + min_y
    
    setfigform(xtickList, ytickList, xlabel = args.xlabel, ylabel = args.ylabel, title = args.title)
    # add diagonal line
    plt.plot((min_x, max_x), (min_y, max_y), ls="--", c="k")
    
    plt.savefig("fig")
    plt.show()
    

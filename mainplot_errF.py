import matplotlib.pyplot as plt
import numpy as np
import argparse
from formatlist import generateformat
from plotfunctions import addline, setfigform, getmaxmin, readcontext


if __name__ == "__main__":

    labellist = [" ", " ", " ", " ", " "]
    parser = argparse.ArgumentParser(description='Figure texts')
    parser.add_argument('--title', type=str, default='', help='titile of the figure')
    parser.add_argument('--skip', type=int, default=0, help='skip columes')
    parser.add_argument('--skiprows', type=bool, default=True, help="skip first line")
    parser.add_argument('--num_y', type=int, default=1, help="number of y")
    parser.add_argument('--xlabel', type=str, default="x", help="xlabel")
    parser.add_argument('--ylabel', type=str, default="y", help="ylabel")
    parser.add_argument('INPUT', type=str, nargs = "+",
                                 help="input file")
    parser.add_argument('--format', type=str, default='line-dot', help="Format of plots: line, line-dot, dot")
    parser.add_argument("--singlecolor", type=bool, default=False, help="use single color")
    args = parser.parse_args()
    
    formatindicator = args.format
    
    inputfile = args.INPUT
    
    # num_y = args.num_y
    num_y = 5
    skiprows = args.skiprows
    # skip_y = args.skip
    
    
    x = []
    y = []
    for f in inputfile:
        fin = open(f, "r")
        context = fin.readlines()
        x0, y0 = readcontext(context, num_y = 5, skip_y = 0, skiprows = skiprows)
        x1 = []
        y1 = []
        for idata in range(len(x0)):
            # x1 = np.sqrt(x0[idata]*x0[idata] + y0[0][idata]*y0[0][idata] + y0[1][idata]*y0[1][idata]) 
            # y1 = np.sqrt(y0[2][idata]*y0[2][idata] + y0[3][idata]*y0[3][idata] + y0[4][idata]*y0[4][idata]) 
            x1.append(x0[idata])
            y1.append(y0[2][idata])
            x1.append(y0[0][idata])
            y1.append(y0[3][idata])
            x1.append(y0[1][idata])
            y1.append(y0[4][idata])
        x.append(x1)
        y.append(y1)

    
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
    min_x = min_x - 0.1 * (max_x-min_x)
    max_x = max_x + 0.1 * (max_x-min_x)
    min_y = min_y - 0.1 * (max_y-min_y)
    max_y = max_y + 0.1 * (max_y-min_y)
    print((min_x, min_y))
    print((max_x, max_y))
    min_ = min(min_x, min_y)
    max_ = max(max_x, max_y)
    xtickList = (max_-min_) * np.arange(-0.2, 1.2, 0.2) + min_
    ytickList = (max_-min_) * np.arange(-0.2, 1.2, 0.2) + min_

    plt.figure(figsize=(5,5))
    plt.rcParams['agg.path.chunksize'] = 10000
    assignformat = generateformat(len(y), singlecolor=args.singlecolor)
    ptr = 0
    for i_file in range(len(x)):
        # for idx in range(len(x[i_file])):
        #     print(x[i_file][idx], y[i_file][idx])
        # print("\n")
        form = assignformat[formatindicator]
        addline(x[i_file],y[i_file], form[ptr], labellist[i_file], formatindicator=formatindicator)
        ptr += 1
    
    setfigform(xtickList, ytickList, xlabel = args.xlabel, ylabel = args.ylabel, xlimit=(min_, max_), ylimit=(min_, max_), title = args.title)
    # add diagonal line
    plt.plot((min_x, max_x), (min_y, max_y), ls="--", c="k")
    
    plt.savefig("fig", bbox_inches = "tight")
    plt.show()
    

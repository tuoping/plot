import matplotlib.pyplot as plt
import numpy as np
import argparse
from formatlist import assignformat
from plotfunctions import addline, setfigform, getmaxmin, readcontext, bold_axis_and_ticks, plot_error_distribution
import seaborn as sns



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
    args = parser.parse_args()
    
    formatindicator = args.format
    
    inputfile = args.INPUT
    
    # num_y = args.num_y
    num_y = 5
    skiprows = args.skiprows
    skip_y = args.skip
    
    
    x = []
    y = []
    for f in inputfile:
        fin = open(f, "r")
        x0, y0 = readcontext(fin, num_y=num_y, skip_y=skip_y, skiprows = skiprows)
        x1 = []
        y1 = []
        for idata in range(len(x0)):
            #x_ = np.sqrt(x0[idata]*x0[idata] + y0[0][idata]*y0[0][idata] + y0[1][idata]*y0[1][idata]) 
            #y_ = np.sqrt(y0[2][idata]*y0[2][idata] + y0[3][idata]*y0[3][idata] + y0[4][idata]*y0[4][idata]) 
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
    print((min_x, min_y))
    print((max_x, max_y))
    xtickList = (max_x-min_x) * np.arange(0, 1.3, 0.3) + min_x
    ytickList = (max_y-min_y) * np.arange(0, 1.2, 0.2) + min_y

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
    
    setfigform(xtickList, ytickList, xlabel = args.xlabel, ylabel = args.ylabel, title = args.title)
    # add diagonal line
    if args.diagonal_line:
        plt.plot((min_x, max_x), (min_y, max_y), ls="--", c="k")
    
    if args.logx:
        plt.semilogx()
    if args.logy:
        plt.semilogy()
    
    plt.savefig("fig", bbox_inches = "tight")
    plt.show()
    
    from sklearn.metrics import mean_squared_error, r2_score
    for i_file in range(len(x)):
        print(np.sqrt(mean_squared_error(x[i_file], y[i_file])), r2_score(x[i_file], y[i_file]))
        plt = plot_error_distribution(x[i_file], y[i_file])
        plt.xlim((-0.5,0.5))
        plt.savefig("distrib")
        plt.show()

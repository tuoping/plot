import matplotlib.pyplot as plt
import numpy as np
import argparse
from copy import deepcopy
import os,sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from formatlist import assignformat
from plotfunctions import addline, setfigform, getmaxmin, readcontext


if __name__ == "__main__":
    #labellist = ["500K", "600K", "700K", "800K"]
    labellist = ["Free energy", "Energy without entropy", "Energy(sigma->0)"]

    parser = argparse.ArgumentParser(description='Figure texts')
    parser.add_argument('--title', type=str, default='', help='titile of the figure')
    parser.add_argument('--skip', type=int, default=0, help='skip columes')
    parser.add_argument('--natom', type=float, default=1.0, help='y/natom')
    parser.add_argument('--skip_first_line', type=bool, default=False, help="skip first line, default=False")
    parser.add_argument('--num_y', type=int, default=1, help="number of y")
    parser.add_argument('--xlabel', type=str, default="x", help="xlabel")
    parser.add_argument('--ylabel', type=str, default="y", help="ylabel")
    parser.add_argument('INPUT', type=str,
                                 help="input file")
    parser.add_argument('--format', type=str, default='line-dot', help="Format of plots: line, line-dot, dot")
    parser.add_argument("--diagonal_line", type=bool, default=False, help="Add diagonal line")
    args = parser.parse_args()
    
    formatindicator = args.format
    
    inputfile = args.INPUT
    
    num_y = args.num_y
    skip_first_line = args.skip_first_line
    skip_y = args.skip
    
    
    fin = open(inputfile, "r")
    context = fin.readlines()
    print(args.skip_first_line)
    if skip_first_line:
        context.pop(0)

    x, y_ = readcontext(context, num_y = num_y, skip_y = skip_y)
    
    x.pop(0)
    print(x)
    y = []
    for j in range(len(y_)):
        yi=y_[j]
        y.append([])
        for i in range(1,len(yi)):
            y[-1].append((yi[i]-yi[i-1])/args.natom)
            # print(yi[i],yi[i-1],args.natom)
    print(y)
    print("\n")
    
    
    max_x, min_x = getmaxmin(x)
    max_y, min_y = getmaxmin(y)
    print((min_x, min_y))
    print((max_x, max_y))
    for yi in y:
        for i in range(len(yi)):
            yi[i]=(yi[i])*1000
            print(i,x[i],yi[i])
        print("\n")
    print(x)
    print(y)
    for i in range(num_y):
        form = assignformat[formatindicator]
        addline(x,y[i],form[i],labellist[i],formatindicator=formatindicator)
    #max_x = 1200 #(max_x)
    #min_x = 460 #min_x
    max_x = (max_x)
    min_x = min_x
    max_y = (max_y)*1000
    min_y = min_y*1000
    print((min_x, min_y))
    print((max_x, max_y))
    #xtickList = np.arange(450, 1250, 100)# (max_x-min_x) * np.arange(-0, 1.0, 0.2) + min_x
    #xtickList = np.arange(460, 600, 20)# (max_x-min_x) * np.arange(-0, 1.0, 0.2) + min_x
    xtickList = (max_x-min_x) * np.arange(-0, 1.0, 0.2) + min_x
    print(xtickList)
    ytickList = (max_y-min_y) * np.arange(-0.2, 1.0, 0.2) + min_y
    print(ytickList)
    
    setfigform(xtickList, ytickList, xlabel = args.xlabel, ylabel = args.ylabel, title = args.title)
    # add diagonal line
    if args.diagonal_line:
        plt.plot((min_x, max_x), (min_y, max_y), ls="--", c="k")
    
    plt.savefig("fig")
    plt.show()
    

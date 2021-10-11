import matplotlib.pyplot as plt
import numpy as np
import argparse
from formatlist import assignformat
from copy import deepcopy

def addline(x, y, form:dict, label=None, formatindicator="line-dot"):
    if formatindicator == "dot":
        plt.scatter(x,y,c=form["c"], marker=form["marker"], label=label)
    elif formatindicator == "line-dot":
        plt.plot(x,y,c=form["c"], linestyle=form["linestyle"], marker=form["marker"], label=label)
    elif formatindicator == "line":
        plt.plot(x,y,c=form["c"], linestyle=form["linestyle"], label=label)


def setfigform(xtickList, ytickList, xlabel, ylabel, title = ""):
    plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.15)
    plt.legend()
    plt.title(title,fontsize = 16)
    plt.xlabel(xlabel,fontsize = 14)
    plt.ylabel(ylabel, fontsize = 14)
    plt.xticks( xtickList )
    plt.yticks( ytickList )
    plt.tick_params(axis='both',width=2,labelsize = 14)
    

def getmaxmin(data, dtype = float):
    tmpdata = np.copy(data)
    max_data = np.reshape(tmpdata, [-1]).max()
    min_data = np.reshape(tmpdata, [-1]).min()
    return max_data, min_data

def readcontext(context, num_y=1, skip_y=0):
    x = []
    y = []
    for i in range(num_y):
        y.append([])
    for line in context:
        c = line.split()
        if len(c) < num_y+skip_y+1:
            break
        x.append(float(c[0]))
        for idx in range(skip_y+1, num_y+skip_y+1):
            y[idx -1-skip_y].append(float(c[idx]))
    return x,y

if __name__ == "__main__":
    labellist = ["100K", "200K", "300K", "400K"]

    parser = argparse.ArgumentParser(description='Figure texts')
    parser.add_argument('--title', type=str, default='', help='titile of the figure')
    parser.add_argument('--skip', type=int, default=0, help='skip columes')
    parser.add_argument('--skip_first_line', type=bool, default=True, help="skip first line")
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
    if skip_first_line:
        context.pop(0)

    x, y = readcontext(context, num_y = num_y, skip_y = skip_y)
    
    print(x)
    for yi in y:
        print(yi)
    print("\n")
    for i in range(num_y):
        form = assignformat[formatindicator]
        addline(x,y[i],form[i],labellist[i],formatindicator=formatindicator)
    
    
    max_x, min_x = getmaxmin(x)
    max_y, min_y = getmaxmin(y)
    print((min_x, min_y))
    print((max_x, max_y))
    xtickList = (max_x-min_x) * np.arange(0, 1, 0.4) + min_x
    ytickList = (max_y-min_y) * np.arange(0, 1, 0.2) + min_y
    
    setfigform(xtickList, ytickList, xlabel = args.xlabel, ylabel = args.ylabel, title = args.title)
    # add diagonal line
    if args.diagonal_line:
        plt.plot((min_x, max_x), (min_y, max_y), ls="--", c="k")
    
    plt.savefig("fig")
    plt.show()
    

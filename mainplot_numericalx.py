import matplotlib.pyplot as plt
import numpy as np
import argparse
from copy import deepcopy
import os,sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from formatlist import assignformat

def addline(x, y, form:dict, label=None, formatindicator="line-dot"):
    if formatindicator == "dot":
        plt.scatter(x,y,c=form["c"], s=10, marker=form["marker"], label=label)
    elif formatindicator == "line-dot":
        plt.plot(x,y,c=form["c"], linestyle=form["linestyle"], marker=form["marker"], label=label)
    elif formatindicator == "line":
        plt.plot(x,y,c=form["c"], linestyle=form["linestyle"], label=label)


def setfigform(xtickList, ytickList, xlabel, ylabel, title = ""):
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.15)
    plt.legend()
    plt.title(title,fontsize = 16)
    plt.xlabel(xlabel,fontsize = 14)
    plt.ylabel(ylabel, fontsize = 14)
    plt.xticks( xtickList)
    plt.yticks( ytickList)
    plt.tick_params(axis='both',width=2,labelsize = 12)
    

def getmaxmin(data, dtype = float):
    tmpdata = np.copy(data)
    max_data = np.reshape(tmpdata, [-1]).max()
    min_data = np.reshape(tmpdata, [-1]).min()
    return max_data, min_data

def readcontext(context, num_y=1, skip_y=0, skiprows=0):
    c_ = np.loadtxt(context, skiprows=skiprows)
    c = np.transpose(c_)
    #x = c[0]
    #y = c[skip_y:skip_y+num_y]
    print(c)
    x = np.arange(np.shape(c)[1])*0.002+0.8
    y = c[skip_y:skip_y+num_y]
    return x,y

if __name__ == "__main__":
    labellist = ["solid", "liquid"]

    parser = argparse.ArgumentParser(description='Figure texts')
    parser.add_argument('--title', type=str, default='', help='titile of the figure')
    parser.add_argument('--skip', type=int, default=0, help='skip columes')
    parser.add_argument('--skiprows', type=int, default=0, help="skip rows")
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
    skiprows = args.skiprows
    skip_y = args.skip
    
    
    fin = open(inputfile, "r")
    # context = fin.readlines()
    # if skip_first_line:
    #     context.pop(0)
    # 
    # x, y = readcontext(context, num_y = num_y, skip_y = skip_y)
    x, y = readcontext(fin, num_y=num_y, skip_y=skip_y, skiprows=skiprows)
    
    print("x=")
    print(x)
    print("y=")
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
    xtickList = (max_x-min_x) * np.arange(0, 1, 0.2) + min_x
    ytickList = (max_y-min_y) * np.arange(0, 1, 0.2) + min_y
    
    setfigform(xtickList, ytickList, xlabel = args.xlabel, ylabel = args.ylabel, title = args.title)
    # add diagonal line
    if args.diagonal_line:
        plt.plot((min_x, max_x), (min_y, max_y), ls="--", c="k")
    
    plt.savefig("fig")
    plt.show()
    
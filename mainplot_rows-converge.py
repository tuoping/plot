import matplotlib.pyplot as plt
import numpy as np
import argparse
from copy import deepcopy
import os,sys

from formatlist import generateformat
from plotfunctions import addline, setfigform, getmaxmin, readcontext, startfig, setfigform_simple


def readcontextrows(context, skip_y=0, skiprows=0):
    c_ = np.loadtxt(context, dtype="str", skiprows=skiprows)
    if len(c_.shape) == 1:
        c_ = c_[np.newaxis, :]
    y = [np.average(c_[-600:-400].astype(np.float), axis=0), np.average(c_[-400:-200].astype(np.float), axis=0), np.average(c_[-200:].astype(np.float), axis=0)]
    # y = c_[::1]
    return y

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Figure texts')
    parser.add_argument('--title', type=str, default='', help='titile of the figure')
    parser.add_argument('--skip', type=int, default=1, help='skip columes')
    parser.add_argument('--skiprows', type=int, default=1, help="skip rows")
    parser.add_argument('--num_y', type=int, default=1, help="number of y")
    parser.add_argument('--xlabel', type=str, default="x", help="xlabel")
    parser.add_argument('--ylabel', type=str, default="y", help="ylabel")
    parser.add_argument('INPUT', type=str, nargs = "+",
                                 help="input file")
    parser.add_argument('--format', type=str, default='line-dot', help="Format of plots: line, line-dot, dot")
    parser.add_argument("--diagonal_line", type=bool, default=False, help="Add diagonal line")
    parser.add_argument("--logx", type=bool, default=False, help="log scale of x axis")
    parser.add_argument("--logy", type=bool, default=False, help="log scale of y axis")
    parser.add_argument("--xmax", type=float, default=None, help="")
    parser.add_argument("--xmin", type=float, default=None, help="")
    parser.add_argument("--ymax", type=float, default=None, help="")
    parser.add_argument("--ymin", type=float, default=None, help="")
    parser.add_argument("--scalex", type=float, default=1.0, help="")
    parser.add_argument("--s0", type=float, default=0.0, help="")
    parser.add_argument("--epsilon", type=float, default=1.0, help="")
    args = parser.parse_args()
    
    args.format="dot"
    formatindicator = args.format
    
    inputfile = args.INPUT
    
    num_y = args.num_y
    skiprows = args.skiprows
    skip_y = args.skip
    
    
    y = []
    for i in range(len(inputfile)):
       fin = open(inputfile[i], "r")
       y_ = readcontextrows(fin, skip_y=skip_y, skiprows=skiprows)
       for i in range(len(y_)):
           y.append(y_[i][1:])
           # y.append(y_[i][-1])
    y = np.array(y)
    x = np.loadtxt("Sk-kgrid1D.dat")[1:]*float(args.scalex)
    ordered_x = np.array(sorted(x))
    y_ref = args.s0/(1.+ordered_x*ordered_x*args.epsilon)
    print("Shape of y = ", y.shape)
    print("Shape of x = ", x.shape)
    print("xdata: ",x)
    print("ydata: ",y)
    
    
    startfig((5,5))

    labellist = [" " for i in range(len(y))]
    assignformat = generateformat(len(y))
    for i in range(len(y)):
        form = assignformat[formatindicator]
        addline(x,y[i],form[i],labellist[i],formatindicator=formatindicator)
    
    setfigform_simple(xlabel = "k^2", ylabel = "Sk", xlimit = (args.xmin, args.xmax), ylimit = (args.ymin, args.ymax))
    # add diagonal line
    if args.diagonal_line:
        plt.plot((min_x, max_x), (min_y, max_y), ls="--", c="k")
    # plt.plot(ordered_x,y_ref,ls="--",c="b")
    
    if args.logx:
        plt.semilogx()
    if args.logy:
        plt.semilogy()
    
    plt.savefig(inputfile[0][:-4], bbox_inches = "tight")
    plt.show()
    

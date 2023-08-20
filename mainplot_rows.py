import matplotlib.pyplot as plt
import numpy as np
import argparse
from copy import deepcopy
import os,sys

SCRIPT_DIR = "/home/tuoping/soft/plot/"
sys.path.append(SCRIPT_DIR)

from formatlist import generateformat
from plotfunctions import addline, setfigform, getmaxmin, readcontext, startfig, setfigform_simple


def readcontextrows(context, cols, skiprows=0):
    c_ = np.loadtxt(context, dtype="str", skiprows=skiprows).T
    if len(c_.shape) == 1:
        c_ = c_[np.newaxis, :].T
    y = c_[cols].astype(np.float).T
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
    args = parser.parse_args()
    
    formatindicator = args.format
    
    inputfile = args.INPUT
    
    num_y = args.num_y
    skiprows = args.skiprows
    skip_y = args.skip
    
    fin = open(inputfile[0], "r")
    _header = fin.readline()
    header = _header.split()
    header.pop(0)
    header.pop(0)
    header.pop(0)
    header.pop(0)
    header_1 = [x for x in header if "_sfpbc.ds" in x]
    col_1 = np.array([header.index(x)+2 for x in header if "_sfpbc.ds" in x])
    print(header_1)
    items = np.array([np.array(h.split("-")[-1]) for h in header_1])
    # items = np.array([np.array(h.split("-")[1]) for h in header])
    fin.close()

    x_sk = np.array([float(x) for x in items])
    print(x_sk)

    
    y = []
    for i in range(len(inputfile)):
       fin = open(inputfile[i], "r")
       y_ = readcontextrows(fin, col_1, skiprows=skiprows)
       print(y_)
       for j in range(len(y_)):
           y.append(y_[j])
    y = np.array(y)
    time = y_.T[0]
    
    plt.figure()
    labellist = [" "]*len(y)
    assignformat = generateformat(len(y))
    form = assignformat[formatindicator]
    for i in range(len(y)):
        addline(x_sk,y[i],form[i],labellist[i],formatindicator=formatindicator)
    
    setfigform_simple(xlabel = "Sk", ylabel = "SF")
    
    plt.savefig("sfsk")
    plt.show()

import matplotlib.pyplot as plt
import numpy as np
import argparse
import os,sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from formatlist import assignformat
from formatlist import assignformat
from plotfunctions import addline, setfigform, getmaxmin, readcontext


def readcondidate(context, num_y=1, skip_y=0):
    x = []
    y = []
    for i in range(num_y):
        y.append([])
    for line in context:
        c = line.split()
        if len(c) < num_y+skip_y+1:
            break
        x.append(c[0])
        for idx in range(skip_y+1, num_y+skip_y+1):
            y[idx -1-skip_y].append(int(c[idx]))
    return x,y

if __name__ == "__main__":
    # labellist = ["100K", "200K", "300K", "400K"]
    labellist = ["sys6", "sys7"]
    # labellist = ["sys0", "sys1", "sys2", "sys3"]

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
    parser.add_argument("--natom", type=int, default=1, help="Number of atoms, E_per_atom = E_tot/natom")
    args = parser.parse_args()
    
    formatindicator = args.format
    
    inputfile = args.INPUT
    
    # num_y = args.num_y
    num_y = 5
    skip_first_line = args.skip_first_line
    # skip_y = args.skip
    
    
    # x = []
    y = []
    natom = args.natom
    for f in inputfile:
        fin = open(f, "r")
        context = fin.readlines()
        if skip_first_line:
            context.pop(0)
        x0, y0 = readcontext(context, num_y = 5, skip_y = 0)
        # x1 = []
        y1 = []
        idata = 0
        assert(len(x0)%natom == 0)
        for iconf in range(0, int(len(x0)/natom)):
            y_max = 0.0
            for iatom in range(natom):
                y_ = np.sqrt((x0[idata]-y0[2][idata])*(x0[idata]-y0[2][idata]) + (y0[0][idata]-y0[3][idata])*(y0[0][idata]-y0[3][idata]) + (y0[1][idata]-y0[4][idata])*(y0[1][idata]-y0[4][idata]))
                # print(y_, (x0[idata]-y0[2][idata]), (y0[0][idata]-y0[3][idata]), (y0[1][idata]-y0[4][idata]))
                if y_ > y_max:
                    y_max = y_
                idata += 1
            y1.append(y_max)

        # x.append(x1)
        y.append(y1)

    candidatefile = ["candidate.shuffled.006.out", "candidate.shuffled.007.out"]
    xc = []
    yc = []
    for ifile in range(len(candidatefile)):
        f = candidatefile[ifile]
        print(f)
        fin = open(f, "r")
        context = fin.readlines()
        x0, y0 = readcondidate(context, num_y=1)
        _xc = []
        _yc = []
        print("Num_of_candidates: ",len(x0))
        print("DeltaF_modeldev", "DeltaF_DP_DFT", "Configure_idx")
        for idx_x0 in range(min(len(x0), len(y[ifile]))):
            _x0 = x0[idx_x0]
            x1 = os.path.join(os.path.join("../../", _x0), "model_devi.out")
     
            fcandidate = open(x1, "r")
            context_fcandidate = fcandidate.readlines()
            context_fcandidate.pop(0)
            xc0, yc0 = readcontext(context_fcandidate, num_y=1, skip_y=3)
            idx_candidate = xc0.index(y0[0][idx_x0])
            yc1 = yc0[0][idx_candidate]
            _xc.append(y[ifile][idx_x0])
            _yc.append(yc1)
            print(y[ifile][idx_x0], yc1, y0[0][idx_x0])
        xc.append(_xc)
        yc.append(_yc)

    y = xc
    x = yc

    ptr = 0
    for i_file in range(len(x)):
        # print(x[i_file])
        # for yi in y[i_file]:
        #     print(yi)
        # print("\n")
        form = assignformat[formatindicator]
        addline(x[i_file],y[i_file], form[ptr], labellist[i_file], formatindicator=formatindicator)
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
    min_ = min(min_x, min_y)
    max_ = max(max_x, max_y)
    min_x = 0.0
    min_y = 0.0
    max_x = round(max_,1)
    max_y = round(max_,1)
    xtickList = (max_x-min_x) * np.arange(0, 1, 0.1) + min_x
    ytickList = (max_y-min_y) * np.arange(0, 1, 0.1) + min_y
    
    setfigform(xtickList, ytickList, xlabel = args.xlabel, ylabel = args.ylabel, title = args.title)
    # add diagonal line
    plt.plot((min_x, max_x), (min_y, max_y), ls="--", c="k")
    
    plt.savefig("fig")
    plt.show()

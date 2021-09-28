import matplotlib.pyplot as plt
import numpy as np
import argparse

def getmaxmin(data, dim=1):
    num_data = len(data)
    max_data = -10000.0
    min_data = 10000.0
    if dim == 1:
        for elem in data:
            if elem > max_data:
                max_data = elem
            if elem < min_data:
                min_data = elem
    else: 
        if dim == 2:
            for i in range(num_data):
                for elem in data[i]:
                    if elem > max_data:
                        max_data = elem
                    if elem < min_data:
                        min_data = elem
        else:
            raise Exception("Dimension should be <= 2")
    return max_data, min_data

parser = argparse.ArgumentParser(description='Figure texts')
parser.add_argument('--title', type=str, default='', help='titile of the figure')
parser.add_argument('--skip', type=int, default=0, help='skip columes')
parser.add_argument('--skip_first_line', type=bool, default=True, help="skip first line")
# parser.add_argument('--num_y', type=int, default=1, help="number of y")
parser.add_argument('--xlabel', type=str, default="x", help="xlabel")
parser.add_argument('--ylabel', type=str, default="y", help="ylabel")
parser.add_argument('INPUT', type=str, 
                             help="input file")
args = parser.parse_args()
inputfile = args.INPUT

num_y = 6
skip_first_line = args.skip_first_line
skip_y = args.skip
xlabel = args.xlabel
ylabel = args.ylabel

fin = open(inputfile, "r")
if skip_first_line:
    line = fin.readline()
    print(line)
x = []
ytmp = []
for i in range(num_y):
    ytmp.append([])
while(True):
    try:
        line = fin.readline()
        content = line.split()
        # if len(content) < num_y+skip_y+1:
        if len(content) < num_y + skip_y:
            break
        # x.append(float(content[0]))
        for idx in range(skip_y, num_y+skip_y):
            ytmp[idx -skip_y].append(float(content[idx]))
    except(EOFError):
        break

print(len(ytmp[0]))
y = [[]]
for i in range(len(ytmp[0])):
    x.append(np.sqrt(ytmp[0][i]*ytmp[0][i] + ytmp[1][i]*ytmp[1][i] + ytmp[2][i]*ytmp[2][i]))
    y[0].append(np.sqrt(ytmp[3][i]*ytmp[3][i] + ytmp[4][i]*ytmp[4][i] + ytmp[5][i]*ytmp[5][i]))

num_y = 1

print(x)
print("\n")
for yi in y:
    print(yi)

#plot根据列表绘制出有意义的图形，linewidth是图形线宽，可省略
formatlist = []
formatdict = {'c':"r",'marker':'o'}
formatlist.append(formatdict)
formatdict = {'c':"c",'marker':'o'}
formatlist.append(formatdict)
formatdict = {'c':"b",'marker':'o'}
formatlist.append(formatdict)
formatdict = {'c':"green",'marker':'o'}
formatlist.append(formatdict)
formatdict = {'c':"violet",'marker':'o'}
formatlist.append(formatdict)
formatdict = {'c':"orange",'marker':'o'}
formatlist.append(formatdict)
formatdict = {'c':"darkblue",'marker':'o'}
formatlist.append(formatdict)
formatdict = {'c':"lime",'marker':'o'}
formatlist.append(formatdict)
formatdict = {'c':"turquoise",'marker':'o'}
formatlist.append(formatdict)
labellist = ["100K", "200K", "300K", "400K"]
for i in range(num_y):
    plt.scatter(x,y[i],c=formatlist[i]['c'], marker=formatlist[i]['marker'], label=labellist[i])


# plt.plot(x,y1,"r-d",label="y1")
plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.15)
#fig, ax = plt.subplots(1, 1)
#ax.plot((0, 1), (0, 1), transform=ax.transAxes, ls="--", c="k", label="1:1 line")

plt.legend()
plt.title(args.title,fontsize = 16)

#设置坐标轴标签
#plt.xlabel("kspacing",fontsize = 14)
# if num_y == 3:
#     plt.ylabel("Err. of Forces(eV/A)",fontsize = 14)
# else:
#     if num_y == 9:
#         plt.ylabel("Err. of Virials(eV)",fontsize = 14)
#     else:
#         plt.ylabel("Err. of Energies(eV)",fontsize = 14)
plt.xlabel(xlabel,fontsize = 14)
plt.ylabel(ylabel, fontsize = 14)
        

max_x, min_x = getmaxmin(x)
xtickList = (max_x-min_x) * np.arange(0, 1, 0.4) + min_x
plt.xticks( xtickList )
max_y, min_y = getmaxmin(y, dim=2)
ytickList = (max_y-min_y) * np.arange(0, 1, 0.2) + min_y
plt.yticks( ytickList )

print((min_x, min_y))
print((max_x, max_y))
plt.plot((min_x, max_x), (min_y, max_y), ls="--", c="k")
#设置刻度标记的大小
plt.tick_params(axis='both',width=2,labelsize = 14)

plt.savefig("fig")
plt.show()

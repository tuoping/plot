import matplotlib.pyplot as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Figure texts')
parser.add_argument('--title', type=str, default='', help='titile of the figure')
parser.add_argument('--skip', type=int, default=0, help='skip columes')
parser.add_argument('--skip_first_line', type=bool, default=True, help="skip first line")
parser.add_argument('--num_y', type=int, default=1, help="number of y")
parser.add_argument('--xlabel', type=str, default="x", help="xlabel")
parser.add_argument('--ylabel', type=str, default="y", help="ylabel")
args = parser.parse_args()

num_y = args.num_y
skip_first_line = args.skip_first_line
skip_y = args.skip
xlabel = args.xlabel
ylabel = args.ylabel

fin = open("input.dat", "r")
if skip_first_line:
    line = fin.readline()
    print(line)
x = []
y = []
for i in range(num_y):
    y.append([])
while(True):
    try:
        line = fin.readline()
        content = line.split()
        if len(content) < num_y+skip_y+1:
            break
        x.append(float(content[0]))
        for idx in range(skip_y+1, num_y+skip_y+1):
            y[idx -1-skip_y].append(float(content[idx]))
    except(EOFError):
        break

print(x)
for yi in y:
    print(yi)

#plot根据列表绘制出有意义的图形，linewidth是图形线宽，可省略
formatlist = []
formatdict = {'c':"r",'linestyle':'-','marker':'o'}
formatlist.append(formatdict)
formatdict = {'c':"c",'linestyle':'-','marker':'o'}
formatlist.append(formatdict)
formatdict = {'c':"b",'linestyle':'-','marker':'o'}
formatlist.append(formatdict)
formatdict = {'c':"green",'linestyle':'-','marker':'o'}
formatlist.append(formatdict)
formatdict = {'c':"violet",'linestyle':'-','marker':'o'}
formatlist.append(formatdict)
formatdict = {'c':"orange",'linestyle':'-','marker':'o'}
formatlist.append(formatdict)
formatdict = {'c':"darkblue",'linestyle':'-','marker':'o'}
formatlist.append(formatdict)
formatdict = {'c':"lime",'linestyle':'-','marker':'o'}
formatlist.append(formatdict)
formatdict = {'c':"turquoise",'linestyle':'-','marker':'o'}
formatlist.append(formatdict)
labellist = ["100K", "200K", "300K", "400K"]
for i in range(num_y):
    plt.plot(x,y[i],c=formatlist[i]['c'], linestyle=formatlist[i]['linestyle'], marker=formatlist[i]['marker'], label=labellist[i])
# plt.plot(x,y1,"r-d",label="y1")
plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.15)

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
        

xtickList = (x[-1]-x[0]) * np.arange(0, 1, 0.2) + x[0]
plt.xticks( xtickList )
max_y = -10000.0
min_y = 10000.0
for i in range(num_y):
    for elem in y[i]:
        if elem > max_y:
            max_y = elem
        if elem < min_y:
            min_y = elem
print(max_y, min_y)
ytickList = (max_y-min_y) * np.arange(0, 1, 0.1) + min_y
plt.yticks( ytickList )

#设置刻度标记的大小
plt.tick_params(axis='both',width=2,labelsize = 14)

plt.savefig("fig")
plt.show()

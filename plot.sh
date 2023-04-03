#!/bin/bash
dir=X/
file=COLVAR
python ~/soft/plot/mainplot_multifile.py $file ~/data/plumedrun-slow/colvars/cubic-500K/$dir/$file ~/data/plumedrun-slow/colvars/2d-500K/$dir/$file ~/data/plumedrun-slow/colvars/hex-500K/$dir/$file ~/data/plumedrun-slow/colvars/hex2-500K/$dir/$file ~/data/plumedrun-slow/colvars/amorph/$dir/$file  --headerskip=2 --item=sfbcccombine3,sfbcccombine1 --format=dot

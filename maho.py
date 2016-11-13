import mahotas as mh
import numpy as np
import mahotas.demos
from pylab import imshow, show
#labeled images are integers where vals correspond to different reg. 
#reg 1: pixels val is 1 
#reg 2: val 2, so on. 
#region 0 is the background by default
# regions = np.zeros((8,8), bool)

# regions[:3,:3] = 1
##defines what two pixels to be in the same region
#use square for 8 neightbor 
f1 = mh.imread('zeggs03.jpeg')
f0 = f1;
f = f0[:,:,0]
f2 = mh.gaussian_filter(f, 8)
f = (f2 < f2.mean())
imshow(f)
#show()
labeled, n_nucleus  = mh.label(f)
print('Found {} nuclei.'.format(n_nucleus))
imshow(labeled)
#show()
print f2.shape
dnaf = mh.gaussian_filter(f2, 16.5)
rmax = mh.regmin(dnaf)
imshow(mh.overlay(f2, rmax))
show()
seeds,nr_nuclei = mh.label(rmax)
print nr_nuclei
# sizes = mh.labeled.labeled_size(labeled)
# too_big = np.where(sizes > 10000)
# labeled = mh.labeled.remove_regions(labeled, too_big)
# imshow(labeled)
# show()
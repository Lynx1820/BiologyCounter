import mahotas as mh
import numpy as np
from pylab import imshow, gray, show, jet
from os import path
#takes the pict and turn in 
photo = mh.imread('zeggs01.jpg', as_grey=True)
photo = photo.astype(np.uint8)
T_otsu = mh.otsu(photo)
#print(T_otsu)
gray()
dnaf = mh.gaussian_filter(photo, 16)
# print dnaf
rmax = mh.regmax(dnaf)
print rmax
imshow(mh.overlay(photo, rmax))
show()
seeds,nr_nuclei = mh.label(rmax)
print nr_nuclei
print seeds
# T = mh.thresholding.otsu(dnaf.astype(np.uint8))
# print T
# print dnaf
# imshow(dnaf < T)
# show()
# labeled, nr_objects = mh.label(dnaf < T)
# print nr_objects
# imshow(labeled)
# jet()
# show()
T = mh.thresholding.otsu(dnaf.astype(np.uint8))
dist = mh.distance(dnaf < T)
print "this didatance"
print dist
print dist.max()
dist = dist.max() - dist
dist -= dist.min()
dist = dist/float(dist.ptp()) * 255
dist = dist.astype(np.uint8)
imshow(dist)
show()
nuclei = mh.cwatershed(dist, seeds)
imshow(nuclei)
show()
whole = mh.segmentation.gvoronoi(nuclei)
imshow(whole)
show()
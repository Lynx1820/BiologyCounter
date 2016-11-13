f = mh.gaussian_filter(f, 4)
f = (f> f.mean())
imshow(f)
show()
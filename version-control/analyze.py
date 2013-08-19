import numpy as np
import pylab as pl
import pickle

#results = np.load("results.npy")
results = pickle.load(open('results.pkl'))

t = results['bins'][:-1]
a = results['locs']

pl.plot(t,a)
pl.show()

tc = 1385

pl.loglog(t[t>tc],a[t>tc])
pl.show()

t>tc
t[t>tc]
a[t>tc]

pl.loglog(t[t>tc],a[t>tc])
pl.show()

pl.plot(t,a)
pl.show()

pl.loglog(t[t>tc],a[t>tc])
pl.show()

c = (t>tc)*(t<1800)
pl.loglog(t[c],a[c])

pl.show()

x = np.log10(t[c])
y = np.log10(a[c])
pl.plot(x,y,'.')
pl.show()

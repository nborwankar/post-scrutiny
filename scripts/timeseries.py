import mailbox
import numpy as np
import pylab as pl
import email
import time
import os.path

NAME = "mozilla.general"
MBOX_PATH = "../" + NAME
TIME_FILE = NAME + ".times.npy"

mb = mailbox.mbox(MBOX_PATH)

def get_time(message):
    return email.utils.mktime_tz(
        email.utils.parsedate_tz(message.get('Date'))
        )

def mail_times(mb):
    return [get_time(m) for m in mb.values()]

if os.path.isfile(TIME_FILE):
    times = np.load(TIME_FILE)
else:
    times = np.array(mail_times(mb))
    np.save(TIME_FILE,times)

n_bins = 10000
#start = np.amin(times)
#stop = np.amax(times)
#step = (stop - start / n_bins)
#avoid fencepost error here
#bins = np.arange(start + step, stop, step)
#mail = 

pl.hist(times,n_bins)
pl.show()
hist, bin_edges = np.histogram(times,bins=n_bins)
print hist
print bin_edges



pl.plot()

# simple python script to generate input data for DMcomp experiment : dringeis
# this script is very similar to $ROOTDIR/verification/offline_exf_seaice/input/gendata.m
#
import numpy as np
from copy import copy
from rw import readfield

kwr, kprt =1, 1
nx, ny, nr = 40, 100, 1

pix_sides=int(nx/10)


# ------------------------------------------------------

def writefield(fname,data):
    import sys
    print( 'write to file: '+fname)
    datac=copy(data)
    if sys.byteorder == 'little':
        datac.byteswap(True)
    fid = open(fname,"wb")
    datac.tofile(fid)
    fid.close()


H0 = -200.

# Uniform depth
namf = 'bathy_DMcomp.bin';
depth = H0*np.ones((ny,nx),dtype='float64')
depth[0:1,:] = 0.;

if kwr > 0:
    writefield(namf,depth)


#------------------------------------------------------

namfA='ice0_area_DMcomp.bin'
namfH='ice0_heff_DMcomp.bin'
rhFile='../ice_input/heff_h_25_hd_b.txt'
raFile='../ice_input/area_h_25_hd_b.txt'
iceC0=1.0
iceH0=1.0
randomH=False
randomA=False
uni=True
read_file=False

if uni :

    iceNat=np.ones((ny,nx),dtype='float64')

    iceNat[:,:pix_sides] = 0
    iceNat[:,-pix_sides:] = 0

    iceConc=copy(iceNat)
    iceHeff=copy(iceNat)

    if randomA :
        randC=np.random.randint(low=80,high=101,size=(ny,nx))/100.
        iceConc=iceConc*randC
    if randomH :
        randH=np.random.randint(low=80,high=101,size=(ny,nx))/100.
        iceHeff=iceHeff*randH

    iceConc=iceConc*iceC0
    iceHeff=iceHeff*iceH0


if read_file :

    iceheff=np.loadtxt(rhFile,delimiter=' ')
    iceConc=np.loadtxt(raFile,delimiter=' ')


# iceheff[-2:-1,:]=1.5
# iceConc[-2:-1,:]=1
# iceConc[-2:-1,0:pix_sides] = 0
# iceConc[-2:-1,-pix_sides:-1] = 0
# iceheff[-2:-1,0:pix_sides] = 0
# iceheff[-2:-1,-pix_sides:-1] = 0


if kwr > 0 :
    writefield(namfH,iceHeff)
    writefield(namfA,iceConc)

if kprt > 0 :
 import matplotlib.pyplot as plt

 hScal=np.asarray([-1.1, 0.1])*np.abs(H0);
 plt.figure(1)
 # plt.subplot(211)
 var=depth
 plt.pcolormesh(var,cmap='viridis')
 plt.colorbar()
 plt.axes().set_aspect('equal', 'datalim')
 plt.title('Depth [m]')


 plt.figure(2)
 plt.pcolormesh(iceHeff,cmap='viridis')
 plt.colorbar()
 plt.axes().set_aspect('equal', 'datalim')
 plt.title('Effective ice thickness');

 plt.figure(3)
 plt.pcolormesh(iceConc,cmap='viridis')
 plt.colorbar()
 plt.axes().set_aspect('equal', 'datalim')
 plt.title('Ice concentration');


 plt.show()

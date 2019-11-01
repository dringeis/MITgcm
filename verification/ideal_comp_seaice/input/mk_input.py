#! /usr/bin/env python
# simple python script to generate input data for obcs package
# this script is very similar to /verification/seaice_obcs/input/mk_input.m
#
# Generate input files for MITgcm/DMcomp
#

import numpy as np
from copy import copy,deepcopy
import os
from glob import glob
import sys
from rw import *

# remove extisting files
for filename in glob("*.DMcomp"):
    os.remove(filename)

nx=40
ny=100
nz=1
nt=2
ix=range(nx)
iy=range(ny)

# Create the zeroes BC
temp_z_4=np.zeros((nt,nz,ny,nx),dtype='float64')

# U/V/T/S lateral boundary conditions

# for f in ['T','S','U','V']:

#     x1=ix[0]
#     x2=ix[-1]
#     y1=iy[0]
#     y2=iy[-1]

#     for t in range(0,nt):

#         for d in ['N','S','E','W']:

#             fo=str('OB'+d+f.lower()+'.DMcomp')

#             if d=='N':
#                 data=np.array(temp_z_4[t,:,y1,ix])
#                 writefield(fo,data,method='ab')
#             elif d=='S':
#                 data=np.array(temp_z_4[t,:,y2,ix])
#                 writefield(fo,data,method='ab')
#             elif d=='E':
#                 data=np.array(temp_z_4[t,:,iy,x2])
#                 writefield(fo,data,method='ab')
#             elif d=='W':
#                 data=np.array(temp_z_4[t,:,iy,x1])
#                 writefield(fo,data,method='ab')


## Sea Ice lateral boundary conditions
######################################

# fld=['AREA','HEFF','HSALT','HSNOW','UICE','VICE']
fld=['AREA','HEFF','UICE','VICE']
# nme=['a','h','sl','sn','uice','vice']
nme=['a','h','uice','vice']

# Create the zeroes BC (3dim, no need of z for sea ice)
temp_z_3=np.zeros((nt,ny,nx),dtype='float64')

## Create the ice pack

# Concentration
iceConc0=readfield('ice0_area_DMcomp.bin',(ny,nx),datatype=float)
# iceConc=copy(temp_z_4)
# for t in range(nt):
#     iceConc[t,:,:,:]=iceConc0

# Mean Thickness
iceHeff0=readfield('ice0_heff_DMcomp.bin',(ny,nx),datatype=float)
# iceHeff=copy(temp_z_4)
# for t in range(nt):
#     iceHeff[t,:,:,:]=iceHeff0

## Matrices for seaice speed
# Speed at the start m/s
u_si_ini=0.
v_si_ini=0.0

# Velocity at the end m/s
u_si_end=0.0
v_si_end=-0.1

# Constructing the time speed arrays
u_arr=np.linspace(u_si_ini,u_si_end,nt)
v_arr=np.linspace(v_si_ini,v_si_end,nt)

# construct the matrics corresponding
u_si=copy(temp_z_3)
v_si=copy(temp_z_3)

for t in range(nt):
    u_si[t,-1,:]=u_arr[t]
    v_si[t,-1,:]=v_arr[t]

# Which data choose for which sea ice variable and which direction
icedata={
    # 'a':{
    #     'N':iceConc0,
        # 'S':iceConc
        # 'E':temp_z_4,
        # 'W':temp_z_4,
    # },
    # 'h':{
    #     'N':iceHeff0,
        # 'S':iceHeff,
        # 'E':temp_z_4,
        # 'W':temp_z_4,
    # },
    # 'sl':{
        # 'N':temp_z_4,
        # 'S':temp_z_4,
        # 'E':temp_z_4,
        # 'W':temp_z_4,
    # },
    # 'sn':{
        # 'N':temp_z_4,
        # 'S':temp_z_4,
        # 'E':temp_z_4,
        # 'W':temp_z_4,
    # # },
    'uice':{
        'N':u_si,
        # 'S':temp_z_4,
        # 'E':temp_z_4,
        # 'W':temp_z_4,
    },
    'vice':{
        'N':v_si,
        # 'S':temp_z_4,
        # 'E':temp_z_4,
        # 'W':temp_z_4,
    },
}

data={}

for f in icedata :

    x1=ix[0]
    x2=ix[-1]
    y1=iy[0]
    y2=iy[-1]

    for t in  range(0,nt):

        for d in icedata[f]:

            if len(icedata[f][d].shape)==3:
                temp_data=deepcopy(icedata[f][d][t,:,:])
            elif len(icedata[f][d].shape)==2:
                temp_data=deepcopy(icedata[f][d])


            fo=str('OB'+d+f+'.DMcomp')

            if t==0:

                if d=='N':
                    data[fo]=np.zeros((nt,nx),dtype=float)
                    data[fo][t,:]=temp_data[y2,ix].T
                elif d=='S':
                    data[fo]=np.zeros((nt,nx),dtype=float)
                    data[fo][t,:]=temp_data[y1,ix].T
                elif d=='E':
                    data[fo]=np.zeros((nt,ny),dtype=float)
                    data[fo][t,:]=temp_data[iy,x2].T
                elif d=='W':
                    data[fo]=np.zeros((nt,ny),dtype=float)
                    data[fo][t,:]=temp_data[iy,x1].T

            else :
                if d=='N':
                    data[fo][t,:]=temp_data[y2,ix].T
                elif d=='S':
                    data[fo][t,:]=temp_data[y1,ix].T
                elif d=='E':
                    data[fo][t,:]=temp_data[iy,x2].T
                elif d=='W':
                    data[fo][t,:]=temp_data[iy,x1].T

    writefield(fo,data[fo],method='ab')
    del data[fo]



# # bathymetry
# bathy = readfield('bathy_DMcomp.bin',(ny,nx),datatype=float)
# writefield('bathy.DMcomp',bathy[iy,ix])

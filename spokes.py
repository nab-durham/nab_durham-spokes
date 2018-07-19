#!/usr/bin/env python
#
# (c) Nazim Ali Bharmal 2001--2018
# (c) David Buscher 2001
# See LICENSE for more information

from numpy import *

def factorial(up_num,low_num=1):
  j=1.0
  for i in range(low_num,up_num+1):
    if i!=0: j=j*i
  return(j+0.0)   

# need; radius, 

def spokes(gridSize, nangles=None, outerRadius=None, ratio=1, ongrid=1, offset=None):
   '''Define coordinates that represent spokes
   Let gridSize be the size of the square 2D array,
   Let nangles be the number of radial spokes,
   Let outerRadius be maximum radius from the centre for each spoke,
   Let ratio allow for varying maximum radius, based on an elliptical model,
   Let ongrid define whether spokes start at the intersection of array elements
    or at the centre of one,
   Let offset '''
   if outerRadius == None: outerRadius = (gridSize-1.0)/2.0+1.0e-10
   if nangles==None: nangles=int(outerRadius*2*pi)/2

   baseRadius,baseCentre =\
      radius(gridSize, gridSize, ratio=ratio, ongrid=ongrid, offset=offset, fullCoords=1)

   angles=linspace(0,2*pi,nangles+1)[:nangles]
   anglescds=(array([
      arange(0,outerRadius)*cos(angles.reshape([-1,1])),
      arange(0,outerRadius)*sin(angles.reshape([-1,1])) ])
     +array([baseCentre[0],baseCentre[1]]).reshape([2,1,1])).round()
   return (anglescds[0]*gridSize+anglescds[1]).astype(int32)

def radius(xSize, ySize, ratio=1, ongrid=1, offset=None, fullCoords=None):
    '''Calculate the radius from the centre of a rectangular grid
      ongrid=1 = the coordinates are relative to pixel edges
      ongrdi=0 = the coordinates are relative to pixel centres
      fullCoords=1 return the central grid point.'''
    baseCentre=[ (ySize-ongrid*1.0)/2.0, (xSize-ongrid*1.0)/2.0 ]
    if offset!=None:
       if len(offset)>1:
         for i in (0,1): baseCentre[i]-=offset[i]
       else:
         for i in (0,1): baseCentre[i]-=offset

    ry=arange(ratio*ySize)-ratio*baseCentre[0]
    rx=arange(xSize)-baseCentre[1]
    rxSquared = rx*rx
    rySquared = ry*ry
    rSquared = add.outer(rySquared,rxSquared)
    if fullCoords:
       return sqrt(rSquared), baseCentre
    else:
       return(sqrt(rSquared))

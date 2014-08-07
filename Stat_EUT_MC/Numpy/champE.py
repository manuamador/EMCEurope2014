#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 08 08:01:34 2013

Ensemble de fonctions pour calculer un champ électrique créé par un ensemble
de dipôles de Hertz

@author: emmanuel.amador@edf.fr
"""
from __future__ import division
from numpy import *

c = 299792458.0
  

def champE(x,y,z,I,f):
    """
    Cette fonction calcule le champ électrique créé par un ensemble de dipôles
    Paramètres:
    - x,y,z, vecteurs des coordonnées cartésiennes des points où le champ E est calculé 
    - I matrice des dipôles (x|y|z|tilt|azimut|amplitude|phase)
    - f tableau des fréquences
    """
    N=len(x)
    Ex=zeros((N,len(f)))
    Ey=zeros((N,len(f)))
    Ez=zeros((N,len(f)))
    #Erac=zeros((N,len(f)))
    for i in range(0,N): #boucle sur les N points de mesure
        X=R*cos(phi[i])*sin(theta[i])
        Y=R*sin(phi[i])*sin(theta[i])
        Z=R*cos(theta[i])
        DX = X-I[:,0]
        DY = Y-I[:,1]
        DZ = Z-I[:,2]
        dist = sqrt(DX**2+DY**2+DZ**2)
        dp=tile(dist, (len(f),1))
        fp=tile(f,(len(dist),1))
        phaseI=tile(I[:,6],(len(f),1))
        phase=2*pi*dp*fp.T/c+phaseI
        ca    = cos(I[:,3])
        sa    = sin(I[:,3])
        cb    = cos(I[:,4])
        sb    = sin(I[:,4])
        distx = ((-sb)**2+(1-(-sb)**2)*ca)*DX+(-sb*cb*(1-ca))*DY\
            +(cb*sa)*DZ
        disty = (-sb*cb*(1-ca))*DX+((cb)**2+(1-cb**2)*ca)*DY+(sb*sa)*DZ
        distz = (-cb*sa)*DX+(-sb*sa)*DY+ca*DZ
        distxy = sqrt(distx**2+disty**2)
        costheta = distz/dist
        sintheta = distxy/dist
        cosphi   = distx/distxy
        sinphi   = disty/distxy
        L =tile(I[:,5],(len(f),1))*1/dp*(fp.T/c)**2*377
        Ex = sum(exp(1j*phase)*L*tile(((((-sb)**2+(1-(-sb)**2)*ca)\
            *(-sintheta*costheta*cosphi)+(-sb*cb*(1-ca))\
            *(-sintheta*costheta*sinphi)+(-cb*sa)\
            *(-sintheta*(-sintheta)))),(len(f),1)),axis=1)
        Ey = sum(exp(1j*phase)*L*tile((((-sb*cb*(1-ca))\
            *(-sintheta*costheta*cosphi)+((cb)**2+(1-(cb)**2)*ca)\
            *(-sintheta*costheta*sinphi)+(-sb*sa)\
            *(-sintheta*(-sintheta)))),(len(f),1)),axis=1)
        Ez = sum(exp(1j*phase)*L*tile((((cb*sa)\
            *(-sintheta*costheta*cosphi)+(sb*sa)\
            *(-sintheta*costheta*sinphi)\
            +ca*(-sintheta*(-sintheta)))),(len(f),1)),axis=1)           
    return Ex,Ey,Ez


def champElointain(R,theta,phi,I,f):
    """
    Cette fonction calcule le champ électrique lointain par un ensemble de dipôles
    Paramètres:
    - R distance de la mesure
    - theta,phi  coordonées angulaires des points de mesures
    - I matrice des dipôles (x|y|z|tilt|azimut|amplitude|phase)
    - f tableau des fréquences
    """
    N=len(theta)
    Eth=zeros((N,len(f)))
    Eph=zeros((N,len(f)))
    #Er=zeros((N,len(f)))
    for i in range(0,N): #boucle sur les N points de mesure
        X=R*cos(phi[i])*sin(theta[i])
        Y=R*sin(phi[i])*sin(theta[i])
        Z=R*cos(theta[i])
        DX = X-I[:,0]
        DY = Y-I[:,1]
        DZ = Z-I[:,2]
        dist = sqrt(DX**2+DY**2+DZ**2)
        dp=tile(dist, (len(f),1))
        fp=tile(f,(len(dist),1))
        phaseI=tile(I[:,6],(len(f),1))
        phase=2*pi*dp*fp.T/c+phaseI
        ca    = cos(I[:,3])
        sa    = sin(I[:,3])
        cb    = cos(I[:,4])
        sb    = sin(I[:,4])
        distx = ((-sb)**2+(1-(-sb)**2)*ca)*DX+(-sb*cb*(1-ca))*DY\
            +(cb*sa)*DZ
        disty = (-sb*cb*(1-ca))*DX+((cb)**2+(1-cb**2)*ca)*DY+(sb*sa)*DZ
        distz = (-cb*sa)*DX+(-sb*sa)*DY+ca*DZ
        distxy = sqrt(distx**2+disty**2)
        costheta = distz/dist
        sintheta = distxy/dist
        cosphi   = distx/distxy
        sinphi   = disty/distxy
        L =tile(I[:,5],(len(f),1))*1/dp*(fp.T/c)**2*377
        Exx = sum(exp(1j*phase)*L*tile(((((-sb)**2+(1-(-sb)**2)*ca)\
            *(-sintheta*costheta*cosphi)+(-sb*cb*(1-ca))\
            *(-sintheta*costheta*sinphi)+(-cb*sa)\
            *(-sintheta*(-sintheta)))),(len(f),1)),axis=1)
        Eyy = sum(exp(1j*phase)*L*tile((((-sb*cb*(1-ca))\
            *(-sintheta*costheta*cosphi)+((cb)**2+(1-(cb)**2)*ca)\
            *(-sintheta*costheta*sinphi)+(-sb*sa)\
            *(-sintheta*(-sintheta)))),(len(f),1)),axis=1)
        Ezz = sum(exp(1j*phase)*L*tile((((cb*sa)\
            *(-sintheta*costheta*cosphi)+(sb*sa)\
            *(-sintheta*costheta*sinphi)\
            +ca*(-sintheta*(-sintheta)))),(len(f),1)),axis=1)           
        Eth[i,:]= real(Exx*cos(theta[i])*cos(phi[i])\
            +Eyy*cos(theta[i])*sin(phi[i])-Ezz*sin(theta[i]))
        Eph[i,:]= real(-Exx*sin(phi[i])+Eyy*cos(phi[i]))
        #Er[i,:] = abs(Exx*sin(theta[i])*cos(phi[i])\
        #   +Eyy*sin(theta[i])*sin(phi[i])+Ezz*cos(theta[i]))
    return Eth,Eph

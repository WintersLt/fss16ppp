#!/usr/bin/python

from objectives import Schaffer, Osyczka2, Kursawe
from sa import sa
from mws import mws

for model in [Schaffer, Osyczka2, Kursawe]:
    for optimizer in [sa, mws]:
        optimizer(model())


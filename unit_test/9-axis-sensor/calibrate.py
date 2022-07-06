import sys
sys.path.append('../../main')
from machine import Machine

ma = Machine()
ma.nine.calibrate(ma.motor)
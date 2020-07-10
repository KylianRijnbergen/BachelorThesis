# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 13:44:45 2020

@author: Kylian Rijnbergen
"""

import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"]="0"

from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())

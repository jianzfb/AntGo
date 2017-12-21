#  -*- coding: UTF-8 -*-
from pkgutil import walk_packages
import os
import os.path
from .standard import *
from .simpleimages import *
from .csvs import *
is_support_tf = True
try:
  from .tfrecordsreader import *
  is_support_tf = True
except:
  is_support_tf = False

def global_import(name):
  p = __import__(name, globals(), locals(), level=1)
  globals().pop(name)
  lst = p.__all__ if '__all__' in dir(p) else dir(p)
  for k in lst:
    globals()[k] = p.__dict__[k]

for _, module_name, _ in walk_packages([os.path.dirname(__file__)]):
  if not module_name.startswith('_'):
    if module_name == 'tfrecordsreader':
      continue
   
    global_import(module_name)


def AntDataset(dataset_name, parse_flag=''):
  # absorb some small error
  if dataset_name in globals():
    return globals()[dataset_name]
  elif dataset_name.capitalize() in globals():
    return globals()[dataset_name.capitalize()]
  elif dataset_name.title() in globals():
    return globals()[dataset_name.title()]
  elif dataset_name.upper() in globals():
    return globals()[dataset_name.upper()]
  elif dataset_name.lower() in globals():
    return globals()[dataset_name.lower()]
  else:
    if parse_flag == 'csv':
      return CSV
    elif (parse_flag == 'tfrecord' or parse_flag == 'tfrecords') and is_support_tf:
      return TFRecordsReader
    
    if dataset_name.startswith('tf') and is_support_tf:
      return TFRecordsReader
    
    if dataset_name.startswith('image'):
      return SimpleImages
    
    return Standard

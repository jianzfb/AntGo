# -*- coding: UTF-8 -*-
# @Time    : 17-12-27
# @File    : celeba.py
# @Author  : jian<jian@mltalker.com>
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
from antgo.dataflow.dataset import *
import os
import numpy as np
__all__ = ['CelebA']

CELEBA_URL = "http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html"
class CelebA(Dataset):
  def __init__(self, train_or_test, dir=None, params=None):
    super(CelebA, self).__init__(train_or_test, dir)
    
    # 0.step maybe download
    if not (os.path.exists(os.path.join(self.dir, 'Img')) and
              os.path.exists(os.path.join(self.dir, 'Anno')) and
              os.path.exists(os.path.join(self.dir, 'Eval'))):
      self.download(self.dir,
                    file_names=['pack.zip'],
                    default_url='shell:unzip {file_placeholder} -d %s'%'/'.join(self.dir.split('/')[0:-1]))
    
    # 1.step data folder (wild or align)
    image_flag = getattr(params, 'image', 'align')
    if image_flag == 'align':
      self._data_folder = os.path.join(self.dir, 'Img', 'img_align_celeba')
    else:
      self._data_folder = os.path.join(self.dir, 'Img', 'img_celeba')
      
    # 2.step data split(train/val/test)
    self._file_list = []
    self._file_map = {}
    with open(os.path.join(self.dir, 'Eval', 'list_eval_partition.txt'), 'r') as fp:
      content = fp.readline()
      while content:
        file_name, file_flag = content.split(' ')
        if self.train_or_test == 'train':
          if int(file_flag) == 0:
            self._file_map[file_name] = len(self._file_list)
            self._file_list.append(os.path.join(self._data_folder, file_name))
        elif self.train_or_test == 'val':
          if int(file_flag) == 1:
            self._file_map[file_name] = len(self._file_list)
            self._file_list.append(os.path.join(self._data_folder, file_name))
        else:
          if int(file_flag) == 2:
            self._file_map[file_name] = len(self._file_list)
            self._file_list.append(os.path.join(self._data_folder, file_name))
        
        content = fp.readline()
    
    self.ids = range(len(self._file_list))
    
    # 3.step annotation folder
    self._annotations = {}
    # 3.1 step landmark annotation
    # landmark name
    # lefteye_x
    # lefteye_y
    # righteye_x
    # righteye_y
    # nose_x
    # nose_y
    # leftmouth_x
    # leftmouth_y
    # rightmouth_x
    # rightmouth_y
    if image_flag == 'align':
      with open(os.path.join(self.dir, 'Anno', 'list_landmarks_align_celeba.txt')) as fp:
        # skip fist two rows
        fp.readline()
        fp.readline()
        landmark_content = fp.readline()
        while landmark_content:
          file_name, l_x, l_y, r_x, r_y, n_x, n_y, lm_x, lm_y, rm_x, rm_y = \
            [i for i in landmark_content.replace('\n','').split(' ') if i != '']

          if file_name in self._file_map:
            self._annotations[file_name] = {'landmark': [int(l_x),
                                                         int(l_y),
                                                         int(r_x),
                                                         int(r_y),
                                                         int(n_x),
                                                         int(n_y),
                                                         int(lm_x),
                                                         int(lm_y),
                                                         int(rm_x),
                                                         int(rm_y)]}
          landmark_content = fp.readline()
    else:
      with open(os.path.join(self.dir, 'Anno', 'list_landmarks_celeba.txt')) as fp:
        # skip fist two rows
        fp.readline()
        fp.readline()
        landmark_content = fp.readline()
        while landmark_content:
          file_name, l_x, l_y, r_x, r_y, n_x, n_y, lm_x, lm_y, rm_x, rm_y = \
            [i for i in landmark_content.replace('\n','').split(' ') if i != '']
          if file_name in self._file_map:
            self._annotations[file_name] = {'landmark': [int(l_x),
                                                         int(l_y),
                                                         int(r_x),
                                                         int(r_y),
                                                         int(n_x),
                                                         int(n_y),
                                                         int(lm_x),
                                                         int(lm_y),
                                                         int(rm_x),
                                                         int(rm_y)]}
          landmark_content = fp.readline()

    # 3.2 step attribute annotation
    # attribute names
    # 5_o_Clock_Shadow
    # Arched_Eyebrows
    # Attractive
    # Bags_Under_Eyes
    # Bald
    # Bangs
    # Big_Lips
    # Big_Nose
    # Black_Hair
    # Blond_Hair
    # Blurry
    # Brown_Hair
    # Bushy_Eyebrows
    # Chubby
    # Double_Chin
    # Eyeglasses
    # Goatee
    # Gray_Hair
    # Heavy_Makeup
    # High_Cheekbones
    # Male
    # Mouth_Slightly_Open
    # Mustache
    # Narrow_Eyes
    # No_Beard
    # Oval_Face
    # Pale_Skin
    # Pointy_Nose
    # Receding_Hairline
    # Rosy_Cheeks
    # Sideburns
    # Smiling
    # Straight_Hair
    # Wavy_Hair
    # Wearing_Earrings
    # Wearing_Hat
    # Wearing_Lipstick
    # Wearing_Necklace
    # Wearing_Necktie
    # Young
    with open(os.path.join(self.dir, 'Anno', 'list_attr_celeba.txt')) as fp:
      # skip first two rows
      fp.readline()
      fp.readline()

      attribute_content = fp.readline()
      while attribute_content:
        file_name, \
        o_Clock_Shadow, \
        Arched_Eyebrows, \
        Attractive, \
        Bags_Under_Eyes, \
        Bald, \
        Bangs, \
        Big_Lips, \
        Big_Nose, \
        Black_Hair, \
        Blond_Hair, \
        Blurry, \
        Brown_Hair, \
        Bushy_Eyebrows, \
        Chubby, \
        Double_Chin, \
        Eyeglasses, \
        Goatee, \
        Gray_Hair, \
        Heavy_Makeup, \
        High_Cheekbones, \
        Male, \
        Mouth_Slightly_Open, \
        Mustache, \
        Narrow_Eyes, \
        No_Beard, \
        Oval_Face, \
        Pale_Skin, \
        Pointy_Nose, \
        Receding_Hairline, \
        Rosy_Cheeks, \
        Sideburns, \
        Smiling, \
        Straight_Hair, \
        Wavy_Hair, \
        Wearing_Earrings, \
        Wearing_Hat, \
        Wearing_Lipstick, \
        Wearing_Necklace, \
        Wearing_Necktie, \
        Young = [i for i in attribute_content.replace('\n', '').split(' ') if i != '']
        
        if file_name in self._file_map:
          self._annotations[file_name]['attribute'] = [int(o_Clock_Shadow),
                                                       int(Arched_Eyebrows),
                                                       int(Attractive),
                                                       int(Bags_Under_Eyes),
                                                       int(Bald),
                                                       int(Bangs),
                                                       int(Big_Lips),
                                                       int(Big_Nose),
                                                       int(Black_Hair),
                                                       int(Blond_Hair),
                                                       int(Blurry),
                                                       int(Brown_Hair),
                                                       int(Bushy_Eyebrows),
                                                       int(Chubby),
                                                       int(Double_Chin),
                                                       int(Eyeglasses),
                                                       int(Goatee),
                                                       int(Gray_Hair),
                                                       int(Heavy_Makeup),
                                                       int(High_Cheekbones),
                                                       int(Male),
                                                       int(Mouth_Slightly_Open),
                                                       int(Mustache),
                                                       int(Narrow_Eyes),
                                                       int(No_Beard),
                                                       int(Oval_Face),
                                                       int(Pale_Skin),
                                                       int(Pointy_Nose),
                                                       int(Receding_Hairline),
                                                       int(Rosy_Cheeks),
                                                       int(Sideburns),
                                                       int(Smiling),
                                                       int(Straight_Hair),
                                                       int(Wavy_Hair),
                                                       int(Wearing_Earrings),
                                                       int(Wearing_Hat),
                                                       int(Wearing_Lipstick),
                                                       int(Wearing_Necklace),
                                                       int(Wearing_Necktie),
                                                       int(Young) ]
          
        attribute_content = fp.readline()
    # 3.3 step bounding box
    # bounding box: x_1 y_1 width height
    with open(os.path.join(self.dir, 'Anno', 'list_bbox_celeba.txt')) as fp:
      # skip first two rows
      fp.readline()
      fp.readline()
      
      bounding_box_content = fp.readline()
      while bounding_box_content:
        file_name, x, y, width, height = [i for i in bounding_box_content.replace('\n', '').split(' ') if i != '']
        
        if file_name in self._file_map:
          boxes = np.zeros((1, 4), dtype=np.uint16)
          boxes[0, 0] = int(x)
          boxes[0, 1] = int(y)
          boxes[0, 2] = int(x) + int(width)
          boxes[0, 3] = int(y) + int(height)
          self._annotations[file_name]['bbox'] = boxes
        bounding_box_content = fp.readline()
  
  @property
  def size(self):
    return len(self._file_list)
  
  def data_pool(self):
    epoch = 0
    while True:
      max_epoches = self.epochs if self.epochs is not None else 1
      if epoch >= max_epoches:
        break
      epoch += 1
      
      # idxs = np.arange(len(self.ids))
      idxs = copy.deepcopy(self.ids)
      if self.rng:
        self.rng.shuffle(idxs)
        
      for k in idxs:
        image_file = self._file_list[k]
        file_name = image_file.split('/')[-1]
        image = imread(image_file)
        
        self._annotations[file_name].update({'id': k, 'info': [image.shape[0], image.shape[1], image.shape[2]]})
        yield [image, self._annotations[file_name]]
  
  def at(self, id):
    image_file = self._file_list[id]
    file_name = image_file.split('/')[-1]
    image = imread(image_file)
    self._annotations[file_name].update({'id': id, 'info': [image.shape[0], image.shape[1], image.shape[2]]})
    return image, self._annotations[file_name]
  
  def split(self, split_params={}, split_method='holdout'):
    assert (self.train_or_test == 'train')
    assert (split_method == 'holdout')
    validation_dataset = CelebA('val', self.dir)
    return self, validation_dataset
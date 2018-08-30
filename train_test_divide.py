import shutil as st
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import random

import sys, time

class ProgressBar:
    def __init__(self, count = 0, total = 0, width = 50):
        self.count = count
        self.total = total
        self.width = width
    def move(self):
        self.count += 1
    def log(self, s):
        sys.stdout.write(' ' * (self.width + 9) + '\r')
        sys.stdout.flush()
        print(s)
        progress = self.width * self.count // self.total
        sys.stdout.write('{0:3}/{1:3}: '.format(self.count, self.total))
        sys.stdout.write('#' * progress + '-' * (self.width - progress) + '\r')
        if progress == self.width:
            sys.stdout.write('\n')
        sys.stdout.flush()

sets=[]

classes = ["customer", "sale"]

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

#
def convert_annotation(image_id):
    try:
        in_file = open('./Annotations/%s.xml'%(image_id))
        out_file = open('./labels/%s.txt'%(image_id), 'w')
        tree=ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bb = convert((w,h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
#            print('%s success'%(image_id))
        in_file.close()
        out_file.close()
        return 0
    except FileNotFoundError as e:
    #     print('%s fail'%(image_id))
         return 1


def get_availabe_ids():
    imageids=os.listdir('./labels')
    log_file=open('./labels/available_id.txt', 'w')
    log_file.truncate()
    for fullname in imageids:
        str1=fullname.split('.')[0]
        log_file.write(str1+ "\n")
        print('%s available'%(str1))
    log_file.close()


def remove_unused_ids():
    image_ids = open('./labels/log.txt').read().strip().split()
    for name in image_ids:
        try:
            st.move('./JPEGImages/%s.jpg' % (name), './JPEGImages/unused/%s.jpg' % (name))
            print('move %s success' % (name))
        except IOError:
            print('move %s fail: no found' % (name))


def get_unmatched_ids():
    log_file = open('./labels/log.txt', 'w')
    bar = ProgressBar(total=15514)
    for image_id in range(1, 15515, 1):
        bar.move()
        bar.log('We have arrived at: ' + str(image_id))
        if (convert_annotation(image_id) != 0):
            log_file.write(str(image_id) + "\n")
    log_file.close()

def train_test_holdout():
    with open('./labels/available_id.txt') as f:
        image_ids = f.read().strip().split()
    test_ids = random.sample(image_ids,int(len(image_ids)*0.3))
    train_ids = list(set(image_ids) ^ set(test_ids))
    wd = getcwd()
    with open('./train.all.txt','w') as f1:
        for id in train_ids:
            f1.write('%s/JPEGImages/%s.jpg'%(wd,id)+'\n')
    with open('./test.all.txt', 'w') as f2:
        for id in test_ids:
            f2.write('%s/JPEGImages/%s.jpg' % (wd, id) + '\n')

def gen_testimageset():
    image_ids=[]
    with open('test.all.txt') as f1:
        for line in f1.readlines():
            image_ids.append(line.strip().split('/')[-1].split('.')[0])
    with open('./test.txt','w') as f2:
        for id in image_ids:
            f2.write('%s'%(id)+'\n')





if __name__ == '__main__':
    gen_testimageset()

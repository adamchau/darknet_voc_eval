import shutil as st
import os
import pickle
image_ids = open('./labels/log.txt').read().strip().split()
for name in image_ids:
    try:
        st.move('./JPEGImages/%s.jpg'%(name),'./JPEGImages/unused/%s.jpg'%(name))
        print('move %s success'%(name))
    except IOError:
        print('move %s fail: no found'%(name))


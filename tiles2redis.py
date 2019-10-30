#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from redis import StrictRedis

image_dirs = []


def get_file(path):
    parents = os.listdir(path)
    # print(parents)

    for parent in parents:
        map_path = os.path.join(path, parent)
        # print(map_path)
        if os.path.isdir(map_path):
            get_file(map_path)
        else:
            image_dirs.append(map_path)
    #print(image_dirs)


def get_url():
    sr = StrictRedis(host='localhost', port=6379, db=2)
    for img_dir in image_dirs:
        l = img_dir.split("/")
        with open(img_dir, 'rb') as f:
            img_data = f.read()
        key = "%s_%s_%s" % (l[-3], l[-2], l[-1].split(".")[0])
        print("image key value", key, len(img_data))
        sr.set(key, img_data)


if __name__ == '__main__':
    get_file('/home/sinoeco/hdd/dataset/panorama/gdal_leaflet_viewer/tiles')
    get_url()


#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from xpinyin import Pinyin

pinyin = Pinyin()
out_dir = "./out"


def walk_dir(dir_name):
    map_list = []

    for rootpath, dirnames, filenames in os.walk(dir_name):

        def foo(name):
            name_pinyin = pinyin.get_pinyin(name, "_")
            target_path = os.path.join(rootpath, name)
            target_pinyin = os.path.join(rootpath, name_pinyin)
            map_list.append([target_path, target_pinyin])

        for dname in dirnames:
            foo(dname)

        for fname in filenames:
            foo(fname)

    return map_list


if __name__ == "__main__":
    # if len(sys.argv) == 1:
    #   print(u'fname2pinyin 目标目录 [输出目录]')
    #   exit(-1)
    target_dir = "./utest"
    if len(sys.argv) == 2:
        target_dir = sys.argv[1]
    if len(sys.argv) == 3:
        target_dir = sys.argv[1]
        out_dir = sys.argv[2]

    if target_dir == out_dir:
        print(u"[目标目录]和[输出目录]不能相同")
        exit(-1)

    if os.path.exists(out_dir):
        os.system("rm -fr %s" % (out_dir))
    os.system("cp -fr %s %s" % (target_dir, out_dir))

    map_list = walk_dir(out_dir)
    while len(map_list) > 0:
        data = map_list.pop()
        os.rename(data[0], data[1])

#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

from xpinyin import Pinyin

pinyin = Pinyin()


def __tidy_name(name):
    invalid_char = u"\\\"!$^()+=/{[;:?<>,]}！￥（）—【】、|。，《》·`&%'…@#*."
    common_char = u"1234567890"
    chinese_name = ""
    pinyin_name = ""
    for char in name:
        if char in invalid_char:
            continue
        if char in common_char:
            chinese_name += char
            pinyin_name += char
            continue
        key = "%X" % ord(char)
        if len(key) >= 4:
            chinese_name += char
        else:
            pinyin_name += char

    chinese_name = chinese_name.strip(" ")
    pinyin_name = pinyin_name.strip(" ")
    if chinese_name != "":
        return chinese_name
    return pinyin_name.lower()


def __walk_dir(dir_name):
    map_list = []

    for path, dirs, files in os.walk(dir_name):

        for dname in dirs:
            target_path = os.path.join(path, dname)
            dname = __tidy_name(dname)
            name_pinyin = pinyin.get_pinyin(dname, "_")
            target_pinyin = os.path.join(path, name_pinyin)
            map_list.append([target_path, target_pinyin])

        for fname in files:
            target_path = os.path.join(path, fname)
            if fname.find(".") != -1:
                suffix = fname.split(".")[-1]
                fname = fname.replace("." + suffix, "")
                fname = __tidy_name(fname)
                name_pinyin = pinyin.get_pinyin(fname, "_") + "." + suffix
            else:
                name_pinyin = pinyin.get_pinyin(fname, "_")
            target_pinyin = os.path.join(path, name_pinyin)
            map_list.append([target_path, target_pinyin])

    return map_list


def translate_to_pinyin(target_dir="./utest", out_dir="./out"):
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    shutil.copytree(target_dir, out_dir)

    map_list = __walk_dir(out_dir)
    while len(map_list) > 0:
        data = map_list.pop()
        os.rename(data[0], data[1])


def translate_cover_pinyin(target_dir):
    map_list = __walk_dir(target_dir)
    while len(map_list) > 0:
        data = map_list.pop()
        os.rename(data[0], data[1])


def main():
    translate_to_pinyin('./res', './out')
    # translate_cover_pinyin("../res")


if __name__ == "__main__":
    main()

#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

from xpinyin import Pinyin

pinyin = Pinyin()

WARNING_FILE_NAME = 'warning_duplication.txt'


def _tidy_name(name):
    invalid_char = u" !\"#$%&'()*+,-./:;<=>?@[\\]^_{|}—‘’“”…、。《》【】！（），：；？￥"
    common_char = u"1234567890"
    fname = ""
    # chinese_name = ""
    # pinyin_name = ""
    for char in name:
        if char in invalid_char:
            continue
        if char in common_char:
            # chinese_name += char
            # pinyin_name += char
            fname += char
            continue
        key = "%X" % ord(char)
        fname += char
    #     if len(key) >= 4:
    #         chinese_name += char
    #     else:
    #         pinyin_name += char

    # chinese_name = chinese_name.strip(" ")
    # pinyin_name = pinyin_name.strip(" ")
    # if chinese_name != "":
    #     return chinese_name
    # return pinyin_name.lower()
    return fname.lower()


duplication_cache = {}
class DuplicationTypeConst:
    ORGIN_DUPLICATION = "ORGIN_DUPLICATION"
    PINYIN_DUPLICATION = "PINYIN_DUPLICATION"


def _check_duplication_files(tag, content):
    global duplication_cache
    cache =  duplication_cache.get(tag, {})
    duplication_cache[tag] = cache
    _tmp = cache.get(content, 0)
    cache[content] = _tmp + 1


def output_duplication_files():
    global duplication_cache
    for key, value in duplication_cache.items():

        def _write_result(content):
            with open(WARNING_FILE_NAME, 'a+', encoding='utf-8') as fp:
                fp.write(key + ': ' + content + '\n')

        for fname in value:
            if value[fname] > 1:
                _write_result(fname)


def _walk_dir(dir_name):
    map_list = []

    for path, dirs, files in os.walk(dir_name):

        for dname in dirs:
            target_path = os.path.join(path, dname)
            dname = _tidy_name(dname)
            name_pinyin = pinyin.get_pinyin(dname, "_")
            target_pinyin = os.path.join(path, name_pinyin)
            map_list.append([target_path, target_pinyin])

        for fname in files:
            _check_duplication_files(DuplicationTypeConst.ORGIN_DUPLICATION, fname)
            target_path = os.path.join(path, fname)
            if fname.find(".") != -1:
                suffix = fname.split(".")[-1]
                fname = fname.replace("." + suffix, "")
                fname = _tidy_name(fname)
                name_pinyin = pinyin.get_pinyin(fname, "_") + "." + suffix
            else:
                name_pinyin = pinyin.get_pinyin(fname, "_")
            _check_duplication_files(DuplicationTypeConst.PINYIN_DUPLICATION, name_pinyin)
            target_pinyin = os.path.join(path, name_pinyin)
            map_list.append([target_path, target_pinyin])

    return map_list


def translate_to_pinyin(target_dir="./utest", out_dir="./out"):
    """ 翻译目标路径内的文件到输出目录 """
    shutil.copytree(target_dir, out_dir)
    map_list = _walk_dir(out_dir)
    while len(map_list) > 0:
        data = map_list.pop()
        if not os.path.exists(data[1]):
            os.rename(data[0], data[1])


def translate_cover_pinyin(target_dir):
    """ 翻译目标路径内的文件 """
    map_list = _walk_dir(target_dir)
    while len(map_list) > 0:
        data = map_list.pop()
        os.rename(data[0], data[1])


def init_env(out_dir):
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    if os.path.exists(WARNING_FILE_NAME):
        os.remove(WARNING_FILE_NAME)


def main():
    out_dir = './out'
    init_env(out_dir)
    translate_to_pinyin('./res', out_dir)
    output_duplication_files()


if __name__ == "__main__":
    main()

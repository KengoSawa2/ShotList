#!/usr/bin/env python
# -*- coding: utf-8 -*-
from natsort import natsort_keygen

def winmacsort(namelist):
    # Change the dir search order to match the appearance order of Windows Explorer,Mac Finder.
    # Give priority to folders starting with '_' and '-'
    # NOTE: Do not consider other Explorer's unique display order,such as!,@,~,etc...

    natsort_key = natsort_keygen()
    namelist.sort(key=natsort_key)

    under_list = []  # _から始まるフォルダ名のリスト
    hyphen_list = []  # -から始まるフォルダ名のリスト
    for name in namelist[:]:
        if (name.startswith('_')):
            under_list.insert(0, name)
            namelist.remove(name)
        if (name.startswith('-')):
            hyphen_list.insert(0, name)
            namelist.remove(name)

    insert_list = hyphen_list + under_list

    for adddir in insert_list:
        namelist.insert(0, adddir)
    return

#!/usr/bin/env python


def cons_list(obj):
    l=[]
    for d in dir(obj):
        if d[:2]!='__' and d[-2:]!="__":
            l.append(getattr(obj,d))
    return l

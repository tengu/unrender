#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from pprint import pprint

def paths(paths, threashold, min_depth):
    """reduce a stream of paths into patterns that could have produce them.
    """

    tree={}

    for path in paths:
        segs=path.strip('/').split('/')
        node=tree
        for s in segs:
            node=node.setdefault(s, {})

    collapse(tree, threashold=threashold, min_depth=min_depth)

    return tree

def collapse(n, key=None, path=None, **opt):

    assert isinstance(n, dict)

    # required opts.. that's an oxymoron
    threashold=int(opt['threashold'])
    min_depth=int(opt['min_depth'])

    if not path:
        path=[]
    depth=len(path)

    children=n.items()
    if depth>min_depth and len(children)>threashold:
        if 'legend' in opt:
            print >>sys.stderr, 'COLLAPSE:', depth, '/'.join(s or '' for s in path+[key]), len(children), n.keys()[:10]
        star_node=collapse_node(n)
        children=[('*', star_node)]

    for k,c in children:
        collapse(c, key=k, path=path+[k], **opt)


def collapse_node( n):

    children=n.items()

    # unlink
    for k,v in children:
        del n[k]
    # new node
    collapsed_node={}
    n['*']=collapsed_node
    # splice grandchildren to the new node
    for _,c in children:
        for gck,gcv in c.items():
            collapsed_node[gck]=gcv

    return collapsed_node

def flatten(n, key, path):

    assert isinstance(n, dict), ('expected dict', n)

    if n:
        for ck,cn in n.items():
            flatten(cn, ck, path+[key])
    else:
        print '/'.join(path+[key])

def dump(t, d=0, key=None):

    prefix='.'*d

    if isinstance(t, dict):

        children=t.items()

        for k,v in children:
            print prefix, k
            dump(v, d+1, key=k)
    else:
        print prefix, t

if __name__=='__main__':

    import sys
    import baker

    def _paths(threashold=10, min_depth=2):

        path_list=[line.strip('\n') for line in sys.stdin.readlines()]
        tree=paths(path_list, threashold=int(threashold), min_depth=int(min_depth))
        flatten(tree, '', [])

    baker.command(_paths, 'path')

    baker.run()

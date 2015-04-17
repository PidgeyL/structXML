#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Analyzes XML files and returns information about the structure, as
# well as the structure itself.
#
# Copyright (c) 2015	Pieter-Jan Moreels

# Imports
import argparse
import xmltodict
from collections import OrderedDict

# Parse command line arguments
argp=argparse.ArgumentParser(description='Analyze an XML file and return its structure')
argp.add_argument('xml', metavar='xml', type=str, help='xml file to analyze')
argp.add_argument('-o',  metavar='xml', type=str, help='file to export structutre to')
args=argp.parse_args()

def getAttr(dict):
  x=[]
  if type(dict)==list:
    for i in dict:
      y=list(i)
      x.extend([x for x in y if x.startswith("@")])
  elif type(dict)==OrderedDict:
    y=list(dict)
    x=[x for x in y if x.startswith("@")]    
  list(set(x))
  return x

def dig(dict,depth=0):
  pad="  "*depth
  keylist=""
  attrList=["%s='value'"%x[1:] for x in getAttr(dict)]
  attr=", ".join(attrList) if len(attrList)>0 else ""
  attrs=" %s"%attr if len(attr)>0 else ""
  if type(dict)==list:
    for x in dict:
      keylist+="%s\n"%dig(x,depth+1)
    keylist = "\n".join(list(OrderedDict.fromkeys(keylist.split("\n"))))
  elif type(dict)==OrderedDict:
    keys=list(dict.keys())
    for x in keys:
      if not x.startswith("@"):
        result=dig(dict[x],depth=depth+1)
        if result.strip().startswith("<"):
          keylist+="%s<%s%s>\n%s\n%s</%s>\n"%(pad,attrs,x,result,pad,x)
        else:
          keylist+="%s<%s%s> %s </%s>\n"%(pad,x,attrs,result.strip(),x)
  else:
    keylist = "%svalue"%pad
  return keylist.strip("\n")


if __name__ == '__main__':
  if not args.xml:
    sys.exit('No imputfile selected')
  xml=open(args.xml,'r').read()
  dict=xmltodict.parse(xml)
  struct=dig(dict)
  print(struct)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Analyzes XML files and returns information about the structure, as
# well as the structure itself.
#
# Copyright (c) 2015	Pieter-Jan Moreels

# Imports
import argparse
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

# Parse command line arguments
argp=argparse.ArgumentParser(description='Analyze an XML file and return its structure')
argp.add_argument('-i', help='xml file to analyze')
argp.add_argument('-o', help='file to export structutre to')
args=argp.parse_args()

# Parser
class XMLHandler(ContentHandler):
  def __init__(self):
    self.tags={}
  def startElement(self, name, attrs):
    keys=list(self.tags.keys())
    if not name in keys:
      element={'attrs':attrs, 'recur':1}
      self.tags[name]=element
    else:
      oldAttrs=self.tags[name]['attrs']
      allAttrs=oldAttrs
      # add new attrs
      self.tags[name]['attrs']=allAttrs
      self.tags[name]['recur']+=1

if __name__ == '__main__':
  if not args.i:
    sys.exit('No imputfile selected')
  # create parser
  parser=make_parser()
  xh=XMLHandler()
  parser.setContentHandler(xh)
  parser.parse(args.i)
  tags=xh.tags
  for x in tags:
    print("%s - recurs: %s times"%(x,tags[x]['recur']))

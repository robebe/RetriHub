#!/bin/bash

#d3 visualization demo
if which xdg-open > /dev/null
then
  xdg-open d3_visualize/example_1/index.html
  xdg-open d3_visualize/example_2/index.html
elif which gnome-open > /dev/null
then
  gnome-open d3_visualize/example_1/index.html
  gnome-open d3_visualize/example_2/index.html
fi

#!/bin/bash

ALSADEV="plughw:0,0" $HOME/julius/bin/julius -w $HOME/hug/dic/hug_entity.dic -C $HOME/hug/conf/julius.jconf -module

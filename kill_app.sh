#!/bin/bash
sudo ps aux | grep node | grep -v grep | awk '{ print "kill -9", $2 }' | sh
sudo ps aux | grep julius | grep -v grep | awk '{ print "kill -9", $2 }' | sh
sudo ps aux | grep python | grep -v grep | awk '{ print "kill -9", $2 }' | sh
exit 0

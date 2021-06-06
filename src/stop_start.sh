#!/bin/bash


sudo systemctl stop cnc.service
sleep 11.0
date
sudo systemctl start cnc.service

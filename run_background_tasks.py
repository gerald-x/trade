#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

if __name__ == '__main__':
    command = "python3 manage.py process_tasks"
    subprocess.call(command, shell=True)

# strip_uid.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.1.3

import re

def strip_uid(uid_str):
  stripped = re.search('(.+):uid-(.+)', uid_str)

  if stripped:
    return stripped.group(1)
  else:
    return uid_str



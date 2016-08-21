# helpers.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.1.3

import re
import string
import random

def strip_uid(uid_str):
  stripped = re.search('(.+):uid-(.+)', uid_str)

  if stripped:
    return stripped.group(1)
  else:
    return uid_str

def rand_uid(length):
  random_str = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(length))

  return random_str



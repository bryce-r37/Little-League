# file: config.py
# authors: Bryce Robinson
# date: 4/22/23

import os

class Config(object):
   SECRET_KEY = os.environ.get('SECRET_KEY') or 'sic_em_bears'

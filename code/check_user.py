import os
import sys

# Automatically which user to support (Alice (Tianxin) Wang or Avik)
is_alice = 'alice' in os.getcwd() 
DIR_PATH = '/home/alice' if is_alice else "/Users/avikgarg/repo"

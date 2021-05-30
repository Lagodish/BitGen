import os
import subprocess
import sys
import time
import random
import math


while True:
    process1 = subprocess.Popen([sys.executable, "main.py"])
    process1.wait()

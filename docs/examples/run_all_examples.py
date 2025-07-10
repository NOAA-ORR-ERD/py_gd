#!/bin/env python

"""
script to run all teh examples

Good to make sure they all work, and to generate images for the docs.
"""

from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).parent


all_examples = [fn for fn in HERE.glob("*.py") if not fn.name in {"build_color_images.py",
                                                                  "run_all_examples.py",
                                                                  "build_example_page.py"}
                                                                  ]

failures = 0
for script in all_examples:
    print("**************************")
    print("*")
    print("*  Running:   %s"%script)
    print("*")
    print("**************************")

    try:
        subprocess.check_call(["python", script], shell=False)
    except subprocess.CalledProcessError:
        print(f"{script} Failed!!!!")
        failures += 1

sys.exit(failures)





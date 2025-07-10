
from pathlib import Path

HERE = Path(__file__).parent

HEADER = """.. _sample_scripts:

Sample Scripts
==============

A good way to learn to use py_gd is to check out a few example scripts.

"""

all_examples = [fn for fn in HERE.glob("*.py") if not fn.name in {"build_color_images.py",
                                                                  "run_all_examples.py",
                                                                  "build_example_page.py"}
                                                                  ]

def gen_example(script_path):
    if "draw_dots" in str(script_path.stem):
        img_filename = str(script_path.stem) + ".gif"
    else:
        img_filename = str(script_path.stem) + ".png"

    docstring = []
    with open(script_path) as script:
        # find the docstring
        for line in script:
            if line.startswith('"""'):
                break
        for line in script:
            line = line.strip()
            if line.startswith('"""'):
                break
            else:
                docstring.append(line)
    section = f"""

{docstring[0]}\n{"-"*len(docstring[0])}
{"\n".join(docstring[1:])}

.. image:: examples/{img_filename}
    :align: center
    """
    return section

with open(HERE / "../sample_scripts.rst", 'w') as rst:
    rst.write(HEADER)
    for script in all_examples:
        rst.write(gen_example(script))

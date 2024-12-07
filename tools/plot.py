import matplotlib.pyplot as plt
import numpy as np

footer = """
from io import StringIO
buffer = StringIO()
plt.savefig(buffer, format='svg')
buffer.seek(0)
svg_content = buffer.getvalue()
buffer.close()
"""

def run(code, thread):
    context = {}
    exec(code + footer, context)
    return " ".join(context["svg_content"].split("\n")[3:])

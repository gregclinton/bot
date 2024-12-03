import matplotlib.pyplot as plt
import numpy as np

code = """
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

plt.plot(x, y)
plt.title('Sine Curve')
plt.xlabel('x')
plt.ylabel('sin(x)')

plt.close()
"""
footer = """
from io import StringIO
buffer = StringIO()
plt.savefig(buffer, format='svg')
buffer.seek(0)
svg_content = buffer.getvalue()
buffer.close()
"""

def invoke(company, department, caller, command):
    context = {}
    exec(code + footer, context)
    return context["svg_content"]


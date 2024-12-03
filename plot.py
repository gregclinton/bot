import matplotlib.pyplot as plt
import numpy as np

def invoke(company, department, caller, command):
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)

    plt.plot(x, y)
    plt.title('Sine Curve')
    plt.xlabel('x')
    plt.ylabel('sin(x)')

    plt.close()
    return "plot"


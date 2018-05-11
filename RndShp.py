
def shape_p1(name):

    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon
    from matplotlib  import cm
    import pandas as pd
    import math
    from colour import Color
    import random
    from pylab import savefig

    plt.figure(figsize=(1,0.62))
    plt.axis('off')
    c = Color(rgb=(0.5,1,0.5))
    c.luminance = 0.2

    for i in range(1000):
        coordinates = [[x,y] for x, y in np.random.normal(0.5,0.075,(10,2))]
        axes = plt.gca()
        try:
            lum = np.random.normal(0,0.3)
            if c.luminance+lum >= 0 and  c.luminance+lum <= 1:
                c.luminance += lum
            else: 
                c.luminance -= lum
            r = np.random.normal(0,0.0005)
            if c.red+r >= 0 and  c.red+r <= 1:
                c.red += r
            else: 
                c.red -= r
            g = np.random.normal(0,0.0005)
            if c.green+g >= 0 and  c.green+g <= 1:
                c.green += g
            else: 
                c.green -= r        
            b = np.random.normal(0,0.0005)
            if c.blue+b >= 0 and  c.blue+b <= 1:
                c.blue += b
            else: 
                c.green -= r
        except ValueError:
            pass
        try:
            axes.add_patch(Polygon([[x,y] for x,y in coordinates],
                           facecolor= c.hex,
                           alpha = 0.1,
                           closed=False))
        except ValueError:
            pass

    savefig(name, transparent=True)

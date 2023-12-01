import numpy as np, math, pygame

def bezier(screen, pts, color, size, step = 0.05):
    N = len(pts)
    n = N-1
    last = pts[0]
    for t in np.arange(0, 1, step):
        z = np.zeros(2)
        for i in range(N):
            z += np.dot((math.factorial(n)/(math.factorial(i)*math.factorial(n-i)))
                        *((1-t)**(n-i))*(t**i),pts[i])

        #pygame.draw.circle(screen, color, z.astype(int), size)
        pygame.draw.line(screen, color, last, z.astype(int), size)
        last = z.astype(int)
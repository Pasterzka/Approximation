from matplotlib import pyplot as plt
import numpy as np
import loadData

def naturalCubicSplineCoefficients(x, y):
    n = len(x) - 1
    h = [x[i+1] - x[i] for i in range(n)]
    
    # Tworzenie układu równań
    alpha = [0] + [3 * ((y[i+1] - y[i])/h[i] - (y[i] - y[i-1])/h[i-1]) for i in range(1, n)]

    l = [1] + [0]*n
    mu = [0]*n
    z = [0]*(n+1)

    for i in range(1, n):
        l[i] = 2 * (x[i+1] - x[i-1]) - h[i-1]*mu[i-1]
        mu[i] = h[i] / l[i]
        z[i] = (alpha[i] - h[i-1]*z[i-1]) / l[i]

    l[n] = 1
    z[n] = 0
    c = [0]*(n+1)
    b = [0]*n
    d = [0]*n
    a = y[:-1]

    for j in reversed(range(n)):
        c[j] = z[j] - mu[j]*c[j+1]
        b[j] = ((y[j+1] - y[j])/h[j]) - h[j]*(c[j+1] + 2*c[j])/3
        d[j] = (c[j+1] - c[j]) / (3*h[j])

    return a, b, c[:-1], d, x[:-1] 


def evaluateSpline(a, b, c, d, x_base, x_query):
    y_query = []
    for x in x_query:
        for i in range(len(x_base)):
            if x_base[i] <= x <= x_base[i+1] if i+1 < len(x_base) else True:
                dx = x - x_base[i]
                y = a[i] + b[i]*dx + c[i]*dx**2 + d[i]*dx**3
                y_query.append(y)
                break
    return y_query


def interpolationSplinePlots(filename, minY, maxY):
    distances, elevations = loadData.loadData(filename)

    fig, axes = plt.subplots(2, 2)
    axes = axes.flatten() 
    fig.suptitle("Interpolacja funkcjami sklejanymi (spline) – różna liczba węzłów", fontsize=16)

    nodes_counts = [5, 10, 15, 20]
    colors = ['r', 'g', 'm', 'c']

    for idx, (nodesN, ax) in enumerate(zip(nodes_counts, axes)):
        step = len(distances) // nodesN
        indices = list(range(0, len(distances), step))
        nodesX = [distances[i] for i in indices]
        nodesY = [elevations[i] for i in indices]

        # Oblicz współczynniki spline
        a, b, c, d, x_base = naturalCubicSplineCoefficients(nodesX, nodesY)

        # Interpolacja na gęstej siatce
        interpX = np.linspace(nodesX[0], nodesX[-1], 500)
        interpY = evaluateSpline(a, b, c, d, x_base, interpX)

        # Rysowanie danych i interpolacji
        ax.plot(distances, elevations, 'b--', label='Dane oryginalne', alpha=0.5)
        ax.plot(interpX, interpY, color=colors[idx], label=f'Spline ({nodesN} węzłów)')
        ax.plot(nodesX, nodesY, 'o', color=colors[idx], label='Węzły')

        # Etykiety i stylizacja
        ax.set_title(f'{nodesN} węzłów', fontsize=12)
        ax.set_xlabel('Odległość [m]')
        if idx == 0:
            ax.set_ylabel('Wysokość [m n.p.m.]')
        ax.set_ylim(minY, maxY)
        ax.grid(True)
        ax.legend(fontsize=9)

    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    plt.show()
from matplotlib import pyplot as plt
import numpy as np
import loadData

def interpolationSplinePlot(filename, minY, maxY):
    distances, elevations = loadData.loadData(filename)

    fig, axes = plt.subplots(2, 2)
    fig.suptitle("Interpolacja funkcjami sklejanymi (natural spline)", fontsize=16)

    colors = ['r', 'g', 'm', 'c']
    nodes_counts = [5, 10, 15, 20]

    for idx, (nodesN, ax) in enumerate(zip(nodes_counts, axes.flatten())):
        # Wybór węzłów
        n = len(distances)
        step = n // nodesN
        indices = list(range(0, n, step))
        nodesX = [distances[i] for i in indices]
        nodesY = [elevations[i] for i in indices]
        m = len(nodesX) - 1
        h = [nodesX[i+1] - nodesX[i] for i in range(m)]

        # Układ równań spline
        alpha = [0] + [3 * ((nodesY[i+1] - nodesY[i])/h[i] - (nodesY[i] - nodesY[i-1])/h[i-1]) for i in range(1, m)]
        l = [1] + [0]*m
        mu = [0]*m
        z = [0]*(m+1)

        for i in range(1, m):
            l[i] = 2 * (nodesX[i+1] - nodesX[i-1]) - h[i-1]*mu[i-1]
            mu[i] = h[i] / l[i]
            z[i] = (alpha[i] - h[i-1]*z[i-1]) / l[i]

        l[m] = 1
        z[m] = 0
        c = [0]*(m+1)
        b = [0]*m
        d = [0]*m
        a = nodesY[:-1]

        for j in reversed(range(m)):
            c[j] = z[j] - mu[j]*c[j+1]
            b[j] = ((nodesY[j+1] - nodesY[j])/h[j]) - h[j]*(c[j+1] + 2*c[j])/3
            d[j] = (c[j+1] - c[j]) / (3*h[j])

        # Interpolacja
        interpX = np.linspace(nodesX[0], nodesX[-1], 500)
        interpY = []
        for x_val in interpX:
            for i in range(m):
                if nodesX[i] <= x_val <= nodesX[i+1]:
                    dx = x_val - nodesX[i]
                    y_val = a[i] + b[i]*dx + c[i]*dx**2 + d[i]*dx**3
                    interpY.append(y_val)
                    break

        # Rysowanie danych
        ax.plot(distances, elevations, 'b-', label='Dane oryginalne', alpha=0.7, linewidth=1.5)
        ax.plot(interpX, interpY, 
                color=colors[idx], 
                linestyle='-', 
                label=f'Spline ({nodesN} węzłów)')
        
        # Rysowanie i podpisywanie węzłów
        #for i, (x, y) in enumerate(zip(nodesX, nodesY)):
        #    ax.plot(x, y, 'o', color=colors[idx], markersize=6)
        #    ax.text(x, y, f'({x:.0f}, {y:.1f})', fontsize=8, 
        #            ha='center',
        #            va='bottom' if i % 2 else 'top',
        #            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

        ax.set_xlabel('Odległość [m]', fontsize=10)
        ax.set_ylabel('Wysokość [m n.p.m.]', fontsize=10)
        ax.set_title(f'{nodesN} węzłów spline', fontsize=12)
        ax.legend(fontsize=9, loc='upper right')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(minY, maxY)

    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.show()

import normalization as nor
import matplotlib.pyplot as plt
import numpy as np

import loadData 


# Obliczanie wartości wielomianu w punkcie x
def interpolationLagrange(ponitsX, ponitsY, x):
    n = len(ponitsX)
    result = 0.0
    
    for i in range(n):
        term = ponitsY[i]
        for j in range(n):
            if j != i:
                term *= (x - ponitsX[j]) / (ponitsX[i] - ponitsX[j])
        result += term
    return result

# Obliczanie wartości wielomianu dla x-ów
def interpolationLagrangeVectorized(ponitsX, ponitsY, valuesX):
    return np.array([interpolationLagrange(ponitsX, ponitsY, x) for x in valuesX])

def interpolationLagrangePlot(filename):
    distances, elevations = loadData.loadData(filename)
    
    # Normalizacja dziedziny
    distanceNorm, minDistance, maxDistance = nor.normalize(distances)

    fig, axes = plt.subplots(2, 2)
    fig.suptitle("Interpolacja Lagrange'a dla różnych liczby węzłów", fontsize=16)

    colors = ['r', 'g', 'm', 'c']
    nodes_counts = [5, 10, 15, 20]
    
    for idx, (nodesN, ax) in enumerate(zip(nodes_counts, axes.flatten())):
        # Wybieramy węzły interpolacji
        n = len(distanceNorm)
        step = n // nodesN
        indices = range(0, n, step)
        nodesX = [distanceNorm[i] for i in indices]
        nodesY = [elevations[i] for i in indices]
        
        # Punkty do interpolacji
        interpolationnormX = np.linspace(0, 1, 500)
        
        # Interpolacja Lagrange'a
        interpolationY = interpolationLagrangeVectorized(nodesX, nodesY, interpolationnormX)
        
        # Denormalizacja
        interpolationX = nor.denormalize(interpolationnormX, minDistance, maxDistance)
        
        # Rysowanie
        ax.plot(distances, elevations, 'b-', label='Dane oryginalne', alpha=0.7, linewidth=1.5)
        ax.plot(interpolationX, interpolationY, 
                color=colors[idx], 
                linestyle='-',
                label=f'Interpolacja ({nodesN} węzłów)')
        

        for i, (x, y) in enumerate(zip([distances[i] for i in indices], nodesY)):
            ax.plot(x, y, 'o', color=colors[idx], markersize=6)
            ax.text(x, y, f'({x:.0f}, {y:.1f})', 
                   fontsize=8, 
                   ha='center', 
                   va='bottom' if i % 2 else 'top',
                   bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
            
        ax.set_xlabel('Odległość [m]', fontsize=10)
        ax.set_ylabel('Wysokość [m n.p.m.]', fontsize=10)
        ax.set_title(f'{nodesN} węzłów interpolacji', fontsize=12)
        ax.legend(fontsize=9, loc='upper right')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-50, 250)
        
    # Konfiguracja wykresu
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.show()

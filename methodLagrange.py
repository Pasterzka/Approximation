from math import cos, pi
import normalization as nor
import matplotlib.pyplot as plt
import numpy as np
import loadData 

#Generuje węzły Chebysheva
def nodesChebyshevGet(n, a, b):
    nodes = []
    for k in range(1, n+1):
        x = cos((2*k - 1) * pi / (2*n))
        nodes.append(0.5*(a + b) + 0.5*(b - a)*x)
    nodes.sort()
    return nodes


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

def interpolationLagrangePlot(filename, minY, maxY):
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
        

        #for i, (x, y) in enumerate(zip([distances[i] for i in indices], nodesY)):
        #    ax.plot(x, y, 'o', color=colors[idx], markersize=6)
        #    ax.text(x, y, f'({x:.0f}, {y:.1f})', 
        #           fontsize=8, 
        #           ha='center', 
        #           va='bottom' if i % 2 else 'top',
        #           bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
            
        ax.set_xlabel('Odległość [m]', fontsize=10)
        ax.set_ylabel('Wysokość [m n.p.m.]', fontsize=10)
        ax.set_title(f'{nodesN} węzłów interpolacji', fontsize=12)
        ax.legend(fontsize=9, loc='upper right')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(minY, maxY)
        
    # Konfiguracja wykresu
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.show()

def interpolationLagrangeComparePlot(filename, minY, maxY):
    distances, elevations = loadData.loadData(filename)

    # Normalizacja dziedziny
    distanceNorm, minDistance, maxDistance = nor.normalize(distances)

    fig, axes = plt.subplots(2, 2)
    fig.suptitle("Porównanie interpolacji Lagrange'a dla różnych rozmieszczeń węzłów", fontsize=16)

    nodes_counts = [5, 10, 15, 20]
    colors = ['r', 'g', 'm', 'c']
    node_types = ['Równomierne', 'Chebyshev']
    line_styles = ['-', '--']

    for idx, (nodesN, ax) in enumerate(zip(nodes_counts, axes.flatten())):
        # Rysowanie oryginalnych danych
        ax.plot(distances, elevations, 'b-', label='Dane oryginalne', alpha=0.7, linewidth=1.5)
        
        for node_type, ls in zip(node_types, line_styles):
            if node_type == 'Równomierne':
                # Wybieramy równomiernie rozłożone węzły
                n = len(distanceNorm)
                step = n // nodesN
                indices = range(0, n, step)
                nodesX = [distanceNorm[i] for i in indices]
                nodesY = [elevations[i] for i in indices]
            else:
                # Generujemy węzły Chebysheva
                cheb_nodes = nodesChebyshevGet(nodesN, 0, 1)
                nodesX = []
                nodesY = []
                for node in cheb_nodes:
                    idx_closest = np.argmin(np.abs(np.array(distanceNorm) - node))
                    nodesX.append(distanceNorm[idx_closest])
                    nodesY.append(elevations[idx_closest])
            
            # Punkty do interpolacji
            interpolationnormX = np.linspace(0, 1, 500)
            
            # Interpolacja Lagrange'a
            interpolationY = interpolationLagrangeVectorized(nodesX, nodesY, interpolationnormX)
            
            # Denormalizacja
            interpolationX = nor.denormalize(interpolationnormX, minDistance, maxDistance)
            nodesX_denorm = nor.denormalize(nodesX, minDistance, maxDistance)
            
            # Rysowanie interpolacji
            ax.plot(interpolationX, interpolationY, 
                    color=colors[idx], 
                    linestyle=ls,
                    label=f'{node_type} ({nodesN} węzłów)')
            
            # Zaznaczenie węzłów
            marker = 'o' if node_type == 'Równomierne' else 's'
            ax.plot(nodesX_denorm, nodesY, 
                    marker, 
                    color=colors[idx],
                    markersize=6,
                    alpha=0.7)
            
        # Konfiguracja subplotu
        ax.set_xlabel('Odległość [m]', fontsize=10)
        ax.set_ylabel('Wysokość [m n.p.m.]', fontsize=10)
        ax.set_title(f'Porównanie dla {nodesN} węzłów', fontsize=12)
        ax.legend(fontsize=9, loc='upper right')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(minY,maxY)

    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.show()


def interpolationLagrangeChebyshevPlot(filename, minY, maxY):
    distances, elevations = loadData.loadData(filename)
    
    # Normalizacja dziedziny
    distanceNorm, minDistance, maxDistance = nor.normalize(distances)

    fig, axes = plt.subplots(2, 2)
    fig.suptitle("Interpolacja Lagrange'a dla różnych liczby węzłów", fontsize=16)

    colors = ['r', 'g', 'm', 'c']
    nodes_counts = [5, 10, 15, 20]
    
    for idx, (nodesN, ax) in enumerate(zip(nodes_counts, axes.flatten())):
        # Wybieramy węzły interpolacji
        # Generujemy węzły Chebysheva
        cheb_nodes = nodesChebyshevGet(nodesN, 0, 1)
        nodesX = []
        nodesY = []
        for node in cheb_nodes:
            idx_closest = np.argmin(np.abs(np.array(distanceNorm) - node))
            nodesX.append(distanceNorm[idx_closest])
            nodesY.append(elevations[idx_closest])
        
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
        

        #for i, (x, y) in enumerate(zip([distances[i] for i in indices], nodesY)):
        #    ax.plot(x, y, 'o', color=colors[idx], markersize=6)
        #    ax.text(x, y, f'({x:.0f}, {y:.1f})', 
        #           fontsize=8, 
        #           ha='center', 
        #           va='bottom' if i % 2 else 'top',
        #           bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
            
        ax.set_xlabel('Odległość [m]', fontsize=10)
        ax.set_ylabel('Wysokość [m n.p.m.]', fontsize=10)
        ax.set_title(f'{nodesN} węzłów interpolacji', fontsize=12)
        ax.legend(fontsize=9, loc='upper right')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(minY, maxY)
        
    # Konfiguracja wykresu
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.show()
import csv
import math
import matplotlib.pyplot as plt
import numpy as np

# Wczytywanie danych z pliku .csv
def loadData(filename):
    distances = []
    elevations = []

    with open(filename, newline='') as csvfile:

        reader = csv.DictReader(csvfile)

        prevLat, prevLon = None, None
        totalDistnace = 0.0

        for row in reader:

            lat = float(row['latitude'])
            lon = float(row['longitude'])
            ele = float(row['elevation'])

            if prevLat and prevLon is not None:
                d = calculateDistance(prevLat, prevLon, lat, lon)
                totalDistnace += d

            distances.append(totalDistnace)
            elevations.append(ele)

            prevLat, prevLon = lat, lon
        
    return distances, elevations

# Obliczanie odległości między dwoam miejscami na ziemi (odległość w metrach)
def calculateDistance(lat1, lon1, lat2, lon2):

    R = 6371000

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c 

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

# Normalizacja danych
def normalize(x):
    minX, maxX = min(x), max(x)
    return [(xi - minX)/(maxX - minX) for xi in x], minX, maxX

# Denormalizacja
def denormalize(normX, minX, maxX):
    return [xi * (maxX - minX) + minX for xi in normX]


def interpolationLagrangePlot(filename):
    distances, elevations = loadData(filename)
    
    # Normalizacja dziedziny
    distanceNorm, minDistance, maxDistance = normalize(distances)

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
        interpolationX = denormalize(interpolationnormX, minDistance, maxDistance)
        
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


if __name__ == "__main__":
   filename = "Data/CSV/trasa2-2.csv"
   interpolationLagrangePlot(filename)
    
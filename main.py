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

    plt.plot(distances, elevations, 'b-', label='Dane oryginalne', alpha=0.7, linewidth=2)

    colors = ['r', 'g', 'm', 'c']
    line_styles = ['-', '-', '-', '-']
    nodes_counts = [5, 10, 15, 20]
    
    for idx, nodesN in enumerate(nodes_counts):
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
        plt.plot(interpolationX, interpolationY, 
                color=colors[idx], 
                linestyle=line_styles[idx],
                label=f'Interpolacja ({nodesN} węzłów)')
        plt.plot([distances[i] for i in indices], nodesY, 
                'o', 
                color=colors[idx],
                markersize=5,
                alpha=0.7)
        
    # Konfiguracja wykresu
    plt.xlabel('Odległość [m]', fontsize=12)
    plt.ylabel('Wysokość [m n.p.m.]', fontsize=12)
    plt.title("Porównanie interpolacji Lagrange'a dla różnych liczby węzłów", fontsize=14)
    plt.legend(fontsize=10, loc='upper right')
    plt.grid(True, alpha=0.3)
    plt.ylim(-50, 250)
    
    # Zwiększenie czytelności osi
    plt.tick_params(axis='both', which='major', labelsize=10)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
   filename = "Data/CSV/trasa2-2.csv"
   interpolationLagrangePlot(filename)
    
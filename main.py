import csv
import math

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

    R = 6371e3

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c 



if __name__ == "__main__":
    filename = "Data/CSV/trasa1-21.csv"
    distances, evaluations = loadData(filename)
    print(distances)
    print("Hello World")
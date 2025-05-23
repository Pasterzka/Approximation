# Normalizacja danych
def normalize(x):
    minX, maxX = min(x), max(x)
    return [(xi - minX)/(maxX - minX) for xi in x], minX, maxX

# Denormalizacja danych
def denormalize(normX, minX, maxX):
    return [xi * (maxX - minX) + minX for xi in normX]
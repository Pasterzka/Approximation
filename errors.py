import numpy as np
import methodLagrange as mL
import methodSpline as mS
import normalization as nor
import loadData

def meanSquaredError(trueY, predY):
    return np.mean((np.array(trueY) - np.array(predY)) ** 2)

def maxAbsoluteError(trueY, predY):
    return np.max(np.abs(np.array(trueY) - np.array(predY)))

def analyzeErrors(filename):
    distances, elevations = loadData.loadData(filename)
    distanceNorm, minDistance   , maxDistance = nor.normalize(distances)

    nodeCounts = [5, 10, 15, 20, 25, 50, 100]
    methods = ['lagrange_uniform', 'lagrange_chebyshev', 'spline']
    mseErrors = {method: [] for method in methods}
    maxErrors = {method: [] for method in methods}

    denseX = np.linspace(0, 1, 500)
    denseTrueY = np.interp(denseX, distanceNorm, elevations)

    for nodesN in nodeCounts:
        # Równomierne węzły
        step = len(distanceNorm) // nodesN
        indices = range(0, len(distanceNorm), step)
        uniformNodesX = [distanceNorm[i] for i in indices]
        uniformNodesY = [elevations[i] for i in indices]

        # Chebyshev
        chebNodes = mL.nodesChebyshevGet(nodesN, 0, 1)
        chebNodesX, chebNodesY = [], []
        for node in chebNodes:
            idx = np.argmin(np.abs(np.array(distanceNorm) - node))
            chebNodesX.append(distanceNorm[idx])
            chebNodesY.append(elevations[idx])

        # Interpolacje
        lagrangeUniformY = mL.interpolationLagrangeVectorized(uniformNodesX, uniformNodesY, denseX)
        lagrangeChebY = mL.interpolationLagrangeVectorized(chebNodesX, chebNodesY, denseX)

        # Spline
        a, b, c, d, x_base = mS.naturalCubicSplineCoefficients(uniformNodesX, uniformNodesY)
        splineY = mS.evaluateSpline(a, b, c, d, x_base, denseX)

        # Obliczanie błędów
        mseErrors['lagrange_uniform'].append(meanSquaredError(denseTrueY, lagrangeUniformY))
        mseErrors['lagrange_chebyshev'].append(meanSquaredError(denseTrueY, lagrangeChebY))
        mseErrors['spline'].append(meanSquaredError(denseTrueY, splineY))

        maxErrors['lagrange_uniform'].append(maxAbsoluteError(denseTrueY, lagrangeUniformY))
        maxErrors['lagrange_chebyshev'].append(maxAbsoluteError(denseTrueY, lagrangeChebY))
        maxErrors['spline'].append(maxAbsoluteError(denseTrueY, splineY))

    print("\n--- Podsumowanie błędów interpolacji ---")
    for method in methods:
        print(f"\nMetoda: {method}")
        for n, mse, max_err in zip(nodeCounts, mseErrors[method], maxErrors[method]):
            print(f"Węzły: {n:<4} | MSE: {mse:.4f} | MaxError: {max_err:.4f}")
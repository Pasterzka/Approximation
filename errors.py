import numpy as np
import methodLagrange as mL
import methodSpline as mS
import normalization as nor
import loadData

def mean_squared_error(y_true, y_pred):
    return np.mean((np.array(y_true) - np.array(y_pred)) ** 2)

def max_absolute_error(y_true, y_pred):
    return np.max(np.abs(np.array(y_true) - np.array(y_pred)))

def analyze_errors(filename):
    distances, elevations = loadData.loadData(filename)
    distanceNorm, minDistance, maxDistance = nor.normalize(distances)

    node_counts = [5, 10, 15, 20, 25, 50, 100]
    methods = ['lagrange_uniform', 'lagrange_chebyshev', 'spline']
    errors_mse = {method: [] for method in methods}
    errors_max = {method: [] for method in methods}

    x_dense = np.linspace(0, 1, 500)
    y_true_dense = np.interp(x_dense, distanceNorm, elevations)

    for nodesN in node_counts:
        # Równomierne węzły
        step = len(distanceNorm) // nodesN
        indices = range(0, len(distanceNorm), step)
        nodesX_uniform = [distanceNorm[i] for i in indices]
        nodesY_uniform = [elevations[i] for i in indices]

        # Chebyshev
        cheb_nodes = mL.nodesChebyshevGet(nodesN, 0, 1)
        nodesX_cheb, nodesY_cheb = [], []
        for node in cheb_nodes:
            idx = np.argmin(np.abs(np.array(distanceNorm) - node))
            nodesX_cheb.append(distanceNorm[idx])
            nodesY_cheb.append(elevations[idx])

        # Interpolacje
        y_lagrange_uniform = mL.interpolationLagrangeVectorized(nodesX_uniform, nodesY_uniform, x_dense)
        y_lagrange_cheb = mL.interpolationLagrangeVectorized(nodesX_cheb, nodesY_cheb, x_dense)

        # Spline
        a, b, c, d, x_base = mS.naturalCubicSplineCoefficients(nodesX_uniform, nodesY_uniform)
        y_spline = mS.evaluateSpline(a, b, c, d, x_base, x_dense)

        # Obliczanie błędów
        errors_mse['lagrange_uniform'].append(mean_squared_error(y_true_dense, y_lagrange_uniform))
        errors_mse['lagrange_chebyshev'].append(mean_squared_error(y_true_dense, y_lagrange_cheb))
        errors_mse['spline'].append(mean_squared_error(y_true_dense, y_spline))

        errors_max['lagrange_uniform'].append(max_absolute_error(y_true_dense, y_lagrange_uniform))
        errors_max['lagrange_chebyshev'].append(max_absolute_error(y_true_dense, y_lagrange_cheb))
        errors_max['spline'].append(max_absolute_error(y_true_dense, y_spline))

    print("\n--- Podsumowanie błędów interpolacji ---")
    for method in methods:
        print(f"\nMetoda: {method}")
        for n, mse, max_err in zip(node_counts, errors_mse[method], errors_max[method]):
            print(f"Węzły: {n:<4} | MSE: {mse:.4f} | MaxError: {max_err:.4f}")
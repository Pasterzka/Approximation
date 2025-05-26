import matplotlib.pyplot as plt
import numpy as np
import methodLagrange as mL
import methodSpline as mS
import normalization as nor
import loadData 
import errors

def compare_all_methods(filename, minY, maxY):
    distances, elevations = loadData.loadData(filename)
    distanceNorm, minDistance, maxDistance = nor.normalize(distances)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    fig.suptitle("Porównanie metod interpolacji", fontsize=16)

    nodes_counts = [5, 10, 15, 20]
    colors = ['r', 'g', 'm', 'c']
    line_styles = {'lagrange': '-', 'chebyshev': '--', 'spline': '-.'}

    for idx, (nodesN, ax) in enumerate(zip(nodes_counts, axes)):
        # Równomierne węzły
        n = len(distanceNorm)
        step = n // nodesN
        indices = range(0, n, step)
        nodesX_uniform = [distanceNorm[i] for i in indices]
        nodesY_uniform = [elevations[i] for i in indices]
        
        # Węzły Chebysheva
        cheb_nodes = mL.nodesChebyshevGet(nodesN, 0, 1)
        nodesX_cheb = []
        nodesY_cheb = []
        for node in cheb_nodes:
            idx_closest = np.argmin(np.abs(np.array(distanceNorm) - node))
            nodesX_cheb.append(distanceNorm[idx_closest])
            nodesY_cheb.append(elevations[idx_closest])
        
        # Punkty do interpolacji
        x_interp = np.linspace(0, 1, 500)
        
        # ---- Interpolacja Lagrange'a (równomierne) ----
        y_lagrange_uniform = mL.interpolationLagrangeVectorized(nodesX_uniform, nodesY_uniform, x_interp)
        
        # ---- Interpolacja Lagrange'a (Chebyshev) ----
        y_lagrange_cheb = mL.interpolationLagrangeVectorized(nodesX_cheb, nodesY_cheb, x_interp)
        
        # ---- Spline kubiczny (naturalny) ----
        a, b, c, d, x_base = mS.naturalCubicSplineCoefficients(nodesX_uniform, nodesY_uniform)
        y_spline = mS.evaluateSpline(a, b, c, d, x_base, x_interp)
        
        # Denormalizacja
        x_interp_denorm = nor.denormalize(x_interp, minDistance, maxDistance)
        nodesX_uniform_denorm = nor.denormalize(nodesX_uniform, minDistance, maxDistance)
        nodesX_cheb_denorm = nor.denormalize(nodesX_cheb, minDistance, maxDistance)
        
        # Rysowanie
        ax.plot(distances, elevations, 'b-', label='Dane oryginalne', alpha=0.5)
        
        # Metody interpolacji
        ax.plot(x_interp_denorm, y_lagrange_uniform, 
                color=colors[idx], linestyle=line_styles['lagrange'],
                label=f'Lagrange (równomierne)')
        
        ax.plot(x_interp_denorm, y_lagrange_cheb,
                color=colors[idx], linestyle=line_styles['chebyshev'],
                label=f'Lagrange (Chebyshev)')
        
        ax.plot(x_interp_denorm, y_spline,
                color=colors[idx], linestyle=line_styles['spline'],
                label=f'Spline kubiczny')
        
        # Węzły
        ax.plot(nodesX_uniform_denorm, nodesY_uniform, 'o', 
                color=colors[idx], markersize=5, alpha=0.7)
        
        ax.plot(nodesX_cheb_denorm, nodesY_cheb, 'x',
                color=colors[idx], markersize=6, alpha=0.7)
        
        # Konfiguracja wykresu
        ax.set_title(f'{nodesN} węzłów', fontsize=12)
        ax.set_xlabel('Odległość [m]', fontsize=10)
        ax.set_ylabel('Wysokość [m n.p.m.]', fontsize=10)
        ax.legend(fontsize=9, loc='upper right')
        ax.set_ylim(minY, maxY)
        ax.grid(True, alpha=0.3)
        
       
    plt.tight_layout()
    plt.subplots_adjust(top=0.92, right=0.85)
    plt.show()

if __name__ == "__main__":
    filename = "Data/CSV/trasa1-21.csv"
    #mL.interpolationLagrangePlot(filename, -20, 120)
    #mL.interpolationLagrangeChebyshevPlot(filename, -20, 120)
    #mL.interpolationLagrangeComparePlot(filename, -20, 120)
    #compare_all_methods(filename, -20, 120)
    #compare_all_methods(filename, 0, 1000)
    #mS.interpolationSplinePlots(filename, -20, 120)
    errors.analyze_errors(filename)

    filename = "Data/CSV/trasa2-2.csv"
    #mL.interpolationLagrangePlot(filename, -50, 250)
    #mL.interpolationLagrangeChebyshevPlot(filename, -50, 250)
    #mL.interpolationLagrangeComparePlot(filename, -50, 250)
    #compare_all_methods(filename, -50, 250)
    #compare_all_methods(filename, 0, 1000)
    #mS.interpolationSplinePlots(filename, -50, 250)
    errors.analyze_errors(filename)

    filename = "Data/CSV/trasa3-7.csv"
    #mL.interpolationLagrangePlot(filename, 200, 1800)
    #mL.interpolationLagrangeChebyshevPlot(filename, 200, 1800)
    #mL.interpolationLagrangeComparePlot(filename, 200, 1800)
    #compare_all_methods(filename, 200, 1800)
    #mS.interpolationSplinePlots(filename, 200, 1800)
    errors.analyze_errors(filename)

    filename = "Data/CSV/trasa4-19.csv"
    #mL.interpolationLagrangePlot(filename, 200, 1800)
    #mL.interpolationLagrangeChebyshevPlot(filename, 200, 1800)
    #mL.interpolationLagrangeComparePlot(filename, 200, 1800)
    #compare_all_methods(filename, 200, 1800)
    #mS.interpolationSplinePlots(filename, 200, 1800)
    errors.analyze_errors(filename)

    filename = "Data/CSV/trasa5-20.csv"
    #mL.interpolationLagrangePlot(filename, 200, 1800)
    #mL.interpolationLagrangeChebyshevPlot(filename, 200, 1800)
    #mL.interpolationLagrangeComparePlot(filename, 200, 1800)
    #compare_all_methods(filename, 200, 2500)
    #mS.interpolationSplinePlots(filename, 200, 1800)
    errors.analyze_errors(filename)
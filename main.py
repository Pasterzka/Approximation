import methodLagrange as mL
import methodSpline as mS

if __name__ == "__main__":
    filename = "Data/CSV/trasa2-2.csv"
    #mL.interpolationLagrangePlot(filename, -50, 250)
    #mL.interpolationLagrangeChebyshevPlot(filename, -50, 250)
    #mL.interpolationLagrangeComparePlot(filename, -50, 250)
    mS.interpolationSplinePlot(filename, -50, 250)
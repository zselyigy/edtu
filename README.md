# edtu
E function value distribution on the experimental temperature uncertainty


Written by István Gy. Zsély, ELTE Chemical Kinetics Laboratory.

Version 0.1 (18/07/2023).

Program edtu calculates the E error function value for random samples of the simulation results for evenly distributed simulation temperatures.
The error calculation method is 'By data series and datasets'

**Inputs**
- Optima++ output file containing the experimental data and the calculated - simulation temperature dependent - concentration values in mole fractions.
- Optima++ output file containing the estimated experimental standard deviations in abs mole fractions for each point.

**Output**
calculatedEvalues.txt         - A file containing the calculated overall E values based on the random sampling stratas.
calculatedEvaluesbyPoints.txt - The E values using the nominal temperature simulation result. For checking purposes
sigmas_used.txt               - The simga values used. For checking purposes.

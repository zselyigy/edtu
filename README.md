# edtu
E function value distribution on the experimental temperature uncertainty


Written by István Gy. Zsély, ELTE Chemical Kinetics Laboratory.

Version 0.3 (26/07/2023).

Program edtu calculates the E error function value for random samples of the simulation results for evenly distributed simulation temperatures.
The error calculation method is 'By data series and datasets'.
It can read concentration and sigma or E values.
The random samples can be generated on the fly or read them from file.

**Inputs**

edtu handles two type of inputs.

Option 1
- Optima++ output file containing the experimental data and the calculated - simulation temperature dependent - concentration values in mole fractions.
- Optima++ output file containing the estimated experimental standard deviations in abs mole fractions for each point.

Option 2
- A file exported from the graphical interface of Optima++ containing the E values calculated for the nominal and the simulation temperature dependent E values

Optionally, the file of the random sampling can be read instead of its generation on fly.

**Output**

calculatedEvalues.txt         - A file containing the calculated overall E values based on the random sampling stratas.
calculatedEvaluesbyPoints.txt - The E values using the nominal temperature simulation result. For checking purposes
sigmas_used.txt               - The simga values used. For checking purposes.
Optinal: the file of the random samples.
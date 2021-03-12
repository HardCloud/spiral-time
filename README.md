# spiral-time
Spiral time series data set generator 

This function generates a data set which is meant to be used as a benchmark time series data set. It is highly inspired by the synthetic spiral data set in the ILC paper (https://arxiv.org/abs/2009.00329). In this scenario, environments are indexed by time. At each time step/environment, the causal and spurious features are treated in the following manner: The causal features are subjected to a fixed transformation (for instance, rotation by some angle \alpha) at every time step/environment. Another, time dependent function, transforms the spurious features, differently in different environments/time steps. The time dependent function can be chosen to have an increasing or decreasing influence with time on the spurious correlations.

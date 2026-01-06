# Lotka - Volterra equations according to https://sail.usc.edu/~lgoldste/ArtPhon/Slides/lotka-volterramodel.pdf and
# https://math.libretexts.org/Bookshelves/Applied_Mathematics/Mathematical_Biology_(Chasnov)/01%3A_Population_Dynamics/1.04%3A_The_Lotka-Volterra_Predator-Prey_Model


import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def LV(
        t: float,
        pops: list[float],
        alpha: float,
        beta: float,
        gamma: float,
        delta: float
):
    """Function to solve the Lotka Volterra equations.

    Pass in the population sizes and the relevant parameters to find the time derivatives.

    Args:
        t (float): placeholder for time (so that it fits to be passed to solve_ivp).
        pops (List): A list containing the population sizes of the prey and the predators.
        alpha (float): parameter
        beta (float): parameter
        gamma (float): parameter
        delta (float): parameter
    
    Returns:
        tuple: (dx by dt, dy by dt)
    """
    del t
    
    x = pops[0]
    y = pops[1]

    dx_dt = alpha * x - beta * x * y # Prey eq
    dy_dt = - gamma * y + delta * x * y # Pred eq

    return dx_dt, dy_dt

def dimensionless_LV(
        t,
        values,
        r
):
    xhat = values[0]
    yhat = values[1]

    dxhat_dthat = r * (xhat - xhat * yhat)
    dyhat_dthat = (1 / r) * (- yhat + xhat * yhat)

    return dxhat_dthat, dyhat_dthat

def add_to_plot(
        systemchoice,
        typeanalysis,
        time,
        initial_state,
        args,
        what_to_plot_ts
):
    t_span = (0, time)

    if systemchoice == 0:
        system = LV

    elif systemchoice == 1:
        system = dimensionless_LV

    else:
        raise Exception("Unsupported system choice")
    
    times_to_compute = np.linspace(0, time, 100 * time)

    solution = solve_ivp(
        system,
        t_span,
        initial_state,
        args = args,
        t_eval = times_to_compute
    )

    t = solution.t
    x = solution.y[0]
    y = solution.y[1]

    if typeanalysis == 0: # timeseries
        if what_to_plot_ts == 'x':
            xlabel = input("x label: ")
            plt.plot(t, x, label = xlabel)

        elif what_to_plot_ts == 'y':
            ylabel = input("y label: ")
            plt.plot(t, x, label = ylabel)

        elif what_to_plot_ts == 'b':
            xlabel = input("x label: ")
            ylabel = input("y label: ")
            plt.plot(t, x, label = xlabel)
            plt.plot(t, y, label = ylabel)
        
        plt.legend()

    elif typeanalysis == 1: # phase portrait
        label = input("Plot label: ")
        plt.plot(x, y, label = label)
        plt.legend()

system = input("Do you want to solve the dimensional or dimensionless Lotka Volterra equations? (dimensional 0 dimensionless 1) \n")
system = int(system)

typeanalysis = input("Do you want to do a time series plot or phase portrait? (ts 0 pp 1)\n")
typeanalysis = int(typeanalysis)

time = input("What length of time do you want to solve in? (integer)\n")
time = int(time)

if typeanalysis == 0: # time series plot
    what_to_plot_ts = input("What do you want to plot? (x for x-values, y for y-values, b for both)\n")
else:
    what_to_plot_ts = None

if typeanalysis == 0 and system == 0:
    plt.title("Time series plot")
    plt.xlabel("Time")
    plt.ylabel("Population size")

elif typeanalysis == 0 and system == 1:
    plt.title("Time series plot")
    plt.xlabel("Time")
    plt.ylabel("xhat and yhat values")

elif typeanalysis == 1 and system == 0:
    plt.title("Phase portrait")
    plt.xlabel("Number of prey")
    plt.ylabel("Number of predators")

elif typeanalysis == 1 and system == 1:
    plt.title("Phase portrait")
    plt.xlabel("Number of xhat")
    plt.ylabel("Number of yhat")


keep_in_co = "n"
keep_par = "n"
first_run = True

while True:

    if system == 0:
        if keep_in_co == "n":
            x0 = input("x0 value: ")
            x0 = float(x0)
            y0 = input("y0 value: ")
            y0 = float(y0)
            initial_state = (x0, y0)

        if keep_par == "n":
            alpha = input("alpha value: ")
            alpha = float(alpha)
            beta = input("beta value: ")
            beta = float(beta)
            gamma = input("gamma value: ")
            gamma = float(gamma)
            delta = input("delta value: ")
            delta = float(delta)
            args = (alpha, beta, gamma, delta)        
        
    elif system == 1:
        if keep_in_co == "n":
            xhat0 = input("xhat0 value: ")
            xhat0 = float(xhat0)
            yhat0 = input("yhat0 value: ")
            yhat0 = float(yhat0)
            initial_state = (xhat0, yhat0)
        
        if keep_par == "n":
            r = input("r value: ")
            r = float(r)
            args = (r,)
        
    else:
        raise Exception("Not a valid system number")

    add_to_plot(system, typeanalysis, time, initial_state, args, what_to_plot_ts)

    keepgoing = input("Add another solution to plot? (y or n)\n")

    if keepgoing == "n":
        break

    if first_run:
        keep_in_co = input("Keep initial conditions constant?\n")
        keep_par = input("Keep parameters constant?\n")
        first_run = False

plt.show()
# Lotka - Volterra equations according to https://sail.usc.edu/~lgoldste/ArtPhon/Slides/lotka-volterramodel.pdf

# Parameters
alpha = 1
beta = 1
delta = 1
gamma = 1

def dx_dt(x, y):
    return alpha * x - beta * x * y # Prey eq
def dy_dt(x, y):
    return delta * x * y - gamma * y # Pred eq
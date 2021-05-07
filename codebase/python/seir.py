#!/usr/bin/python3


from scipy.integrate import odeint
import numpy as np
import argparse
import matplotlib.pyplot as plt
#import mpld3
#mpld3.enable_notebook()

def plotseird(args, t, S, E, I, R, D=None, L=None, R0=None, Alpha=None, CFR=None):
    """Plot function. """

    f, ax = plt.subplots(1,1,figsize=(10,4))
    # ax.plot(t, S/1e6, 'b', alpha=0.7, linewidth=2, label='Mottagliga')
    ax.plot(t, E/1e6, 'k--', alpha=0.7, linewidth=2, label='Smittspridare')
    ax.plot(t, I/1e6, 'k:', alpha=0.7, linewidth=2, label='Infekterade')
    ax.grid(True)
    # ax.plot(t, R/1e6, 'g', alpha=0.7, linewidth=2, label='Återhämtade')

    if D is not None:
        ax.plot(t, D/1e6, 'k-.', alpha=0.7, linewidth=2, label='Avlidna')
        #ax.plot(t, (S+E+I+R+D)/1e6, 'c--', alpha=0.7, linewidth=2, label='Total')
    #else:

        #ax.plot(t, (S+E+I+R)/1e6, 'c--', alpha=0.7, linewidth=2, label='Total')

    ax.set_xlabel('Antal dagar')
    ax.set_ylabel('Antal miljoner personer')

    #ax.yaxis.set_tick_params(length=0)
    #ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend(borderpad=2.0)
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)
    if L is not None:
        plt.title("Lockdown after {} days".format(L))
        
    ax.grid(True)            
    
    if args is not None:
        if args.save:
            plt.savefig('D:\\Users\\jjwikner\\google\\bok\\elektronism\\figs\\SEIRD.png',dpi=300)

        if args.plot:
            plt.show();

    if R0 is not None or CFR is not None:
        f = plt.figure(figsize=(12,4))
  
    if R0 is not None:
        # sp1
        ax1 = f.add_subplot(121)
        ax1.plot(t, R0, 'b--', alpha=0.7, linewidth=2, label='R_0')

        ax1.set_xlabel('Time (days)')
        ax1.title.set_text('R_0 over time')
        # ax.set_ylabel('Number (1000s)')
        # ax.set_ylim(0,1.2)
        #ax1.yaxis.set_tick_params(length=0)
        #ax1.xaxis.set_tick_params(length=0)
        ax1.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax1.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)

    if Alpha is not None:
        # sp2
        ax2 = f.add_subplot(122)
        ax2.plot(t, Alpha, 'r--', alpha=0.7, linewidth=2, label='alpha')

        ax2.set_xlabel('Time (days)')
        ax2.title.set_text('fatality rate over time')
        # ax.set_ylabel('Number (1000s)')
        # ax.set_ylim(0,1.2)
        ax2.yaxis.set_tick_params(length=0)
        ax2.xaxis.set_tick_params(length=0)
        ax2.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax2.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)

        plt.grid(True)
        plt.show();


def deriv_seir(y, t, N, beta, gamma, delta):
    S, E, I, R = y
    dSdt = -beta * S * I / N
    dEdt = beta * S * I / N - delta * E
    dIdt = delta * E - gamma * I
    dRdt = gamma * I
    return dSdt, dEdt, dIdt, dRdt

def deriv_seird(y, t, N, beta, gamma, delta, alpha, rho):
    S, E, I, R, D = y
    dSdt = -beta * S * I / N
    dEdt = beta * S * I / N - delta * E
    dIdt = delta * E - (1 - alpha) * gamma * I - alpha * rho * I
    dRdt = (1 - alpha) * gamma * I
    dDdt = alpha * rho * I
    return dSdt, dEdt, dIdt, dRdt, dDdt

def main(args):
    # Covid information

    gamma = 1.0 / args.illness
    delta = 1.0 / args.incubate  # incubation period of five days
    # args.R0 = 15.0
    beta = args.R0 * gamma  # R_0 = beta / gamma, so beta = R_0 * gamma
    alpha = args.deathrate/100
    rho = 1/args.lifetime

    (S0, E0, I0, R0, D0) = (args.pop-1, 1, 0, 0, 0)  # initial conditions: one exposed
    
    t = np.arange(args.timeline)

    y0 = (S0, E0, I0, R0, D0) # Initial conditions vector

    ret = odeint(deriv_seird, y0, t, args=(args.pop, beta, gamma, delta, alpha, rho))
    S, E, I, R,  D = ret.T

    plotseird(args, t, S, E, I, R, D)

    print(D[-1])
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot some covid stuff.')
    parser.add_argument('--plot', help='Plot the windows', action='store_true', default=True)
    parser.add_argument('--save', help='Plot the windows', action='store_true', default=True)
    parser.add_argument('--pop', help="Population size", type=int, default=10300000)
    parser.add_argument('--illness', help="Infection lasts", type=int, default=14)
    parser.add_argument('--incubate', help='Incubation time in days', type=int, default=10)
    parser.add_argument('--deathrate',help='Death rate (in %)', type=float, default=3)
    parser.add_argument('--lifetime',help='Expected time to death after infection', type=int, default=10)
    parser.add_argument('--R0',help='Expected something', type=float, default=10.0)
    parser.add_argument('--timeline',help='Number of days', type=int, default=365)
    args = parser.parse_args()
    main(args)

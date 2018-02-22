from riccati import riccati
import sam_constants as sc
import sam_parameters as sp
from Parameters import Parameters
from MJLS import MJLS
from mjlstd import mjlstd
from mjlstd_online import mjlstd_online
from mjlstd_eligibility import mjlstd_eligibility
import matplotlib
import matplotlib.pyplot as plt
import pickle
import numpy as np
from subprocess import call


def load(filename):
    """Loads persisted data."""
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except Exception:
        return None


def save(data, filename):
    """Persists data."""
    with open(filename, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


def get_E_cal_X(m, X):
    E_cal_X = np.zeros_like(X)
    for i in range(m.N):
        for j in range(m.N):
            E_cal_X[i] += m.P[i][j] * X[j]

    return E_cal_X


def plot_Y(m, Y_off, Y_el, X_ric, F_ric, factor):
    plt.figure()

    plt.suptitle(r'Entries of Y at each $t,\ell$-step for '
                 'eligibility traces (blue), '
                 'offline (red), '
                 'vs E_cal(X) (black) ')

    # Pairs (("indexes on X"), ("index on the plot function"))
    plot = [
        ((0, 0, 0), (1)),
        ((0, 0, 1), (2)),
        ((0, 1, 1), (3)),
        ((1, 0, 0), (4)),
        ((1, 0, 1), (5)),
        ((1, 1, 1), (6)),
        ((2, 0, 0), (7)),
        ((2, 0, 1), (8)),
        ((2, 1, 1), (9)),
    ]

    E_cal_X = get_E_cal_X(m, X_ric)

    for p in plot:
        # Get the Ys indexes
        i, j, k = p[0][0], p[0][1], p[0][2]

        # Get the actual values to plot
        Y_off_plot = [y[i][j][k] for y in Y_off]
        Y_el_plot = [y[i][j][k] for y in Y_el]
        E_cal_X_plot = [E_cal_X[i][j][k] for y in Y_off]

        # Create the suplot
        plt.subplot(3, 3, p[1])
        plt.plot(Y_el_plot, 'blue')
        plt.plot(Y_off_plot, 'red')
        plt.plot(E_cal_X_plot, 'black')
        # Configure plot
        plt.ylabel(r'$Y_{}({}, {})$'.format(i + 1, j + 1, k + 1))
        plt.xlabel('(t,el)-step')
        plt.grid(True)
        plt.tight_layout(h_pad=0., w_pad=0., pad=2)

    plt.savefig('Y_k_0_D_{:06.2f}_c_0.1_eligibility.pdf'.format(factor),
                bbox_inches='tight')
    plt.show()
    plt.close()


def plot_F(m, F_off, F_el, X_ric, F_ric, factor):
    plt.figure()

    plt.suptitle(r'Entries of F at each $\ell$-step for '
                 'eligibility traces (blue), '
                 'offline (red), '
                 'vs true optimal gain (black)')

    # Pairs (("indexes on X"), ("index on the plot function"))
    plot = [
        ((0, 0, 0), (1)),
        ((0, 0, 1), (2)),
        ((1, 0, 0), (3)),
        ((1, 0, 1), (4)),
        ((2, 0, 0), (5)),
        ((2, 0, 1), (6)),
    ]

    for p in plot:
        # Get the F indexes
        i, j, k = p[0][0], p[0][1], p[0][2]

        # Get the actual values to plot
        F_off_plot = [f[i][j][k] for f in F_off]
        F_el_plot = [f[i][j][k] for f in F_el]
        F_ric_plot = [F_ric[i][j][k] for f in F_off]

        # Create the suplot
        plt.subplot(3, 2, p[1])
        plt.step(range(len(F_el_plot)), F_el_plot, 'blue')
        plt.step(range(len(F_off_plot)), F_off_plot, 'red')
        plt.plot(F_ric_plot, 'black')
        # Configure plot
        plt.ylabel(r'$F_{}({}, {})$'.format(i + 1, j + 1, k + 1))
        plt.xlabel(r'$\ell$-step')
        plt.grid(True)
        plt.tight_layout(h_pad=0., w_pad=0., pad=2)

    plt.savefig('F_k_0_D_{:06.2f}_c_0.1_eligibility.pdf'.format(factor),
                bbox_inches='tight')
    plt.show()
    plt.close()


def plot_Delta(m, F_off, F_el, X_ric, F_ric, factor):
    Delta_off = [100. * abs((F_ric - f)/F_ric) for f in F_off]
    Delta_el = [100. * abs((F_ric - f)/F_ric) for f in F_el]

    plt.figure()

    plt.suptitle(r'Entries of $\Delta$ for '
                 'eligibility traces (blue), '
                 'offline (red) '
                 'variants at each $\ell$-step')

    # Pairs (("indexes on X"), ("index on the plot function"))
    plot = [
        ((0, 0, 0), (1)),
        ((0, 0, 1), (2)),
        ((1, 0, 0), (3)),
        ((1, 0, 1), (4)),
        ((2, 0, 0), (5)),
        ((2, 0, 1), (6)),
    ]

    for p in plot:
        # Get the Delta indexes
        i, j, k = p[0][0], p[0][1], p[0][2]

        # Get the actual values to plot
        Delta_off_plot = [f[i][j][k] for f in Delta_off]
        Delta_el_plot = [f[i][j][k] for f in Delta_el]

        # Create the suplot
        plt.subplot(3, 2, p[1])
        plt.step(range(len(Delta_el_plot)), Delta_el_plot, 'blue')
        plt.step(range(len(Delta_off_plot)), Delta_off_plot, 'red')
        # Configure plot
        plt.ylabel(r'$\Delta_{}({}, {})$'.format(i + 1, j + 1, k + 1))
        plt.xlabel(r'$\ell$-step')
        plt.grid(True)
        plt.tight_layout(h_pad=0., w_pad=0., pad=2)

    plt.savefig('Delta_k_0_D_{:06.2f}_c_0.1_eligibility.pdf'.format(factor),
                bbox_inches='tight')
    plt.show()
    plt.close()


def plot_Delta_Y(m, Y_off, Y_el, X_ric, F_ric, factor):
    Delta_off = [abs((X_ric - f)/X_ric) for f in Y_off]
    Delta_el = [abs((X_ric - f)/X_ric) for f in Y_el]

    plt.figure()

    plt.suptitle(r'Entries of $\Delta Y$ for '
                 'eligibility traces (blue), '
                 'offline (red) '
                 'variants at each $t,\ell$-step')

    # Pairs (("indexes on X"), ("index on the plot function"))
    plot = [
        ((0, 0, 0), (1)),
        ((0, 0, 1), (2)),
        ((1, 0, 0), (3)),
        ((1, 0, 1), (4)),
        ((2, 0, 0), (5)),
        ((2, 0, 1), (6)),
    ]

    for p in plot:
        # Get the Delta indexes
        i, j, k = p[0][0], p[0][1], p[0][2]

        # Get the actual values to plot
        Delta_off_plot = [f[i][j][k] for f in Delta_off]
        Delta_el_plot = [f[i][j][k] for f in Delta_el]

        # Create the suplot
        plt.subplot(3, 2, p[1])
        plt.step(range(len(Delta_el_plot)), Delta_el_plot, 'blue')
        plt.step(range(len(Delta_off_plot)), Delta_off_plot, 'red')
        # Configure plot
        plt.ylabel(r'$\Delta_{}({}, {})$'.format(i + 1, j + 1, k + 1))
        plt.xlabel(r'$\ell$-step')
        plt.grid(True)
        plt.tight_layout(h_pad=0., w_pad=0., pad=2)

    plt.savefig('Delta_Y_k_0_D_{:06.2f}_c_0.1_eligibility.pdf'.format(factor),
                bbox_inches='tight')
    plt.show()
    plt.close()


def plot_Delta_Y_sum(m, Y_off, Y_el, X_ric, F_ric, factor):
    Delta_off = [sum(sum(sum(abs((X_ric - f)/X_ric)))) / 12. for f in Y_off]
    Delta_el = [sum(sum(sum(abs((X_ric - f)/X_ric)))) / 12. for f in Y_el]

    fontsize = 15

    plt.figure()

    matplotlib.rc('xtick', labelsize=fontsize-2)
    matplotlib.rc('ytick', labelsize=fontsize-2)

    plt.step(range(len(Delta_off)), Delta_off, 'red', label=r'Offline')
    plt.step(range(len(Delta_el)), Delta_el, 'blue', label=r'Online')
    plt.legend(loc=1, fontsize=fontsize)

    # Configure plot
    plt.ylabel(r'$\Delta Y$', fontsize=fontsize)
    plt.xlabel(r'$(\ell, t)$-step', fontsize=fontsize)

    plt.grid(True)
    plt.tight_layout(h_pad=0., w_pad=0., pad=2)

    plt.savefig('Delta_Y_sum_k_0_D_{:06.2f}_c_0.1_'
                'eligibility.pdf'.format(factor), bbox_inches='tight')

    plt.show()
    plt.close()


def plot_Delta_F_sum(m, F_off, F_el, F_ric, factor):
    Delta_off = [sum(sum(sum(abs((F_ric - f)/F_ric)))) / 12. for f in F_off]
    Delta_el = [sum(sum(sum(abs((F_ric - f)/F_ric)))) / 12. for f in F_el]

    fontsize = 15

    plt.figure()

    matplotlib.rc('xtick', labelsize=fontsize-2)
    matplotlib.rc('ytick', labelsize=fontsize-2)

    plt.step(range(len(Delta_off)), Delta_off, 'red', label=r'Offline')
    plt.step(range(len(Delta_el)), Delta_el, 'blue', label=r'Online')
    plt.legend(loc=1, fontsize=fontsize)

    # Configure plot
    plt.ylabel(r'$\Delta F$', fontsize=fontsize)
    plt.xlabel(r'$\ell$-step', fontsize=fontsize)
    plt.grid(True)
    plt.tight_layout(h_pad=0., w_pad=0., pad=2)

    plt.savefig('Delta_F_sum_k_0_D_{:06.2f}_c_0.1_'
                'eligibility.pdf'.format(factor), bbox_inches='tight')

    plt.show()
    plt.close()


def main():
    """Runs the TD(\lambda) algorithm for the Samuelson problem."""
    print('wait for it...')

    seed = 0

    args = {
        'L': sp.L,
        'T': sp.T,
        'K': sp.K,
        'lambda_': sp.lambda_,
        'epsilon': sp.epsilon,
        'c': sp.c,
        'eta': sp.eta,
        'seed': seed,
    }
    p = Parameters(**args)

    factors = [1.]
    for factor in factors:
        filename = 'k_0_D_{:06.2f}_c_0.1_online.pickle'.format(factor)
        data = load(filename)
        if data is None:
            args = {
                'T': int(1e6),
                'N': sc.N,
                'A': sc.A,
                'B': sc.B,
                'C': sc.C,
                'D': factor * sc.D,
                'R': sc.P,
                'epsilon': sp.epsilon,
            }
            [F_ric, X_ric] = riccati(**args)

            args = {
                'N': sc.N,
                'm': sc.m,
                'n': sc.n,
                'A': sc.A,
                'B': sc.B,
                'C': sc.C,
                'D': sc.D,
                'P': sc.P,
                'X': 0. * sc.X,
                'F': F_ric,
            }
            m = MJLS(**args)

            (Fs, Ys, Fs_H, Ys_H) = mjlstd(p, m)
            (Fs_el, Ys_el, Fs_el_H, Ys_el_H) = mjlstd_eligibility(p, m)

        plot_Y(m, Ys_H, Ys_el_H, X_ric, F_ric, factor)
        plot_F(m, Fs_H, Fs_el_H, X_ric, F_ric, factor)
        plot_Delta(m, Fs_H, Fs_el_H, X_ric, F_ric, factor)
        plot_Delta_Y(m, Ys_H, Ys_el_H, X_ric, F_ric, factor)
        plot_Delta_Y_sum(m, Ys_H, Ys_el_H, X_ric, F_ric, factor)
        plot_Delta_F_sum(m, Fs_H, Fs_el_H, F_ric, factor)

        call(['cp', 'Delta_Y_sum_k_0_D_001.00_c_0.1_eligibility.pdf',
              '/home/rafaelbeirigo/papers/2018mjlstdon/fig/sam_Y.pdf'])

        call(['cp', 'Delta_F_sum_k_0_D_001.00_c_0.1_eligibility.pdf',
              '/home/rafaelbeirigo/papers/2018mjlstdon/fig/sam_F.pdf'])


if __name__ == '__main__':
    main()

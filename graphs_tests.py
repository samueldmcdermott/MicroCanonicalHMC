import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
from scipy.stats import linregress

import ESH
import targets
from bias import *

tab_colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']





def bounce_frequency_full_bias():
    """ Figure 1 """

    def point_reduction(points, reduction_factor):
        """reduces the number of points for plotting purposes"""

        indexes = np.concatenate((np.arange(1, 1 + points // reduction_factor, dtype=int),
                                  np.arange(1 + points // reduction_factor, points, reduction_factor, dtype=int)))
        return indexes

    def ess_axis(ax, ff):

        steps_to_ess = lambda n: 200 / n
        ess_to_steps = lambda e: 200 / e

        ymin, ymax = plt.ylim()
        ax2 = ax.secondary_xaxis(np.log10(0.1 / ymin) / np.log10(ymax / ymin), functions=(steps_to_ess, ess_to_steps))
        plt.text(8.5e2, 0.07, 'ESS', fontsize = ff)


    length = [    2,     5,     10,   30,   50,    75,    80,   90,   100,  1000, 10000, 10000000]
    mask_plot = [True, True, False, True, False, False, True, True, True, False, False, False]
    #mask_plot = len(length) * [True, ]

    X = np.load('Tests/data/bounces_eps1.npy')
    indexes = point_reduction(len(X[0]), 100)


    ff, ff_title, ff_ticks = 18, 20, 14
    plt.rcParams['xtick.labelsize'] = ff_ticks
    plt.rcParams['ytick.labelsize'] = ff_ticks
    plt.figure(figsize= (20, 8))
    ax = plt.gca()
    ff, ff_title, ff_ticks = 18, 20, 16
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    colors = plt.cm.cividis(np.linspace(0, 0.9, np.sum(mask_plot)))[::-1]
    plotted = 0
    dash_size = [1, 5, 15, 25, 40, 80]
    for n in range(len(length)):
        if mask_plot[n]:
            plt.plot(indexes, X[n, indexes], linestyle='--', dashes=(dash_size[plotted], 2),  color = colors[plotted], label = r'$\Delta x = $' + str(length[n]))
            plt.plot(indexes, X[n, indexes], alpha= 0.1, color=colors[plotted])

            plotted += 1
    # plt.plot([0, len(variance_bias)], [0.1, 0.1], ':', color='black', alpha = 0.5) #threshold for effective sample size 200
    plt.legend(fontsize = ff)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('# gradient evaluations', fontsize = ff)
    plt.ylabel('bias', fontsize = ff)
    plt.xlim(1, 1e6)
    ess_axis(ax, ff)
    plt.savefig('submission/FullBias.pdf')
    plt.show()



def dimension_dependence_prelim():

    dimensions = [50, 100, 200, 500, 1000]#, 3000, 10000]

    E, L = [], []
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 3, 1)
    folder_name = 'Kappa100_t'
    #folder_name = 'Rosenbrock_precondition_t'
    factor = 1.0 #Leapfrog
    #factor = 0.25 #Yoshida
    for i in range(len(dimensions)):
        d = dimensions[i]
        X = np.load('Tests/data/dimensions/'+folder_name+'/'+str(d)+'.npy')
        #peak
        plt.plot(X[:, 1], factor*X[:, 0], color = tab_colors[i], alpha= 0.5)

        #highest point
        imax= np.argmax(factor*X[:, 0])
        L.append(X[imax, 1])
        E.append(X[imax, 0])
        plt.plot(X[imax, 1], factor*X[imax, 0], '.', color = tab_colors[i])
        plt.text(X[imax, 1] * 1.05, factor*X[imax, 0]*1.03, 'd= '+str(d), color = tab_colors[i], alpha = 0.5) #dimension tag


    plt.ylabel('ESS')
    plt.xscale('log')
    plt.xlabel("orbit length between bounces")

    ###  L ~ sqrt(d)  ###
    plt.subplot(1, 3, 2)
    for i in range(len(dimensions)):
        plt.plot(dimensions[i], L[i], 'o', color = tab_colors[i])

    skip = 1
    slope= np.dot(np.sqrt(dimensions[skip:]), L[skip:]) / np.sum(dimensions[1:])
    print(slope)
    plt.title(r'$L \approx$' +'{0:.4}'.format(slope) + r' $\sqrt{d}$')
    plt.plot(dimensions, slope * np.sqrt(dimensions), ':', color = 'black')
    plt.xlabel('d')
    plt.ylabel('optimal orbit length between bounces')
    plt.xscale('log')
    plt.yscale('log')


    #ESS(d)
    plt.subplot(1, 3, 3)

    for i in range(len(dimensions)):
        plt.plot(dimensions[i], E[i], 'o', color= tab_colors[i])

    from scipy.stats import linregress

    res = linregress(np.log(dimensions[skip:]), np.log(E[skip:]))


    plt.title(r'ESS $\propto d^{-\alpha}, \quad \alpha = $' + '{0}'.format(np.round(-res.slope, 2)))
    plt.plot(dimensions, np.exp(res.intercept) * np.power(dimensions, res.slope), ':', color='black')
    plt.xlabel('d')
    plt.ylabel('ESS')
    plt.xscale('log')
    plt.yscale('log')

    #plt.savefig('Tests/bounce_dimension_dependence/'+folder_name+'.png')
    plt.show()



def kappa_dependence_prelim():

    kappa = [1, 10, 100, 10000, 10000]
    factor = 1.0  # Leapfrog
    # factor = 0.25 #Yoshida
    E, L = [], []


    plt.figure(figsize=(15, 5))

    ###  peaks ESS(L) for different kappa  ###
    plt.subplot(1, 3, 1)

    for i in range(len(kappa)):
        K = kappa[i]
        X = np.load('Tests/data/kappa/'+str(K)+'.npy')
        #peak
        plt.plot(X[:, 1], factor*X[:, 0], color = tab_colors[i], alpha= 0.5)

        #highest point
        imax= np.argmax(factor*X[:, 0])
        L.append(X[imax, 1])
        E.append(X[imax, 0])
        plt.plot(X[imax, 1], factor*X[imax, 0], '.', color = tab_colors[i])
        plt.text(X[imax, 1] * 1.05, factor*X[imax, 0]*1.03, 'kappa = '+str(K), color = tab_colors[i], alpha = 0.5) #dimension tag


    plt.ylabel('ESS')
    plt.xlabel("orbit length between bounces")


    ###  optimal L as a function of kappa  ###
    plt.subplot(1, 3, 2)
    for i in range(len(kappa)):
        plt.plot(kappa[i], L[i], 'o', color = tab_colors[i])

    # skip = 1
    # slope= np.dot(np.sqrt(dimensions[skip:]), L[skip:]) / np.sum(dimensions[1:])
    # print(slope)
    # plt.title(r'$L \approx$' +'{0:.4}'.format(slope) + r' $\sqrt{d}$')
    # plt.plot(dimensions, slope * np.sqrt(dimensions), ':', color = 'black')
    plt.xlabel('condition number')
    plt.ylabel('optimal orbit length between bounces')
    plt.xscale('log')
    #plt.yscale('log')


    ###  optimal ESS as a function of kappa  ###
    plt.subplot(1, 3, 3)

    for i in range(len(kappa)):
        plt.plot(kappa[i], E[i], 'o', color= tab_colors[i])

    #from scipy.stats import linregress
    #res = linregress(np.log(dimensions[skip:]), np.log(E[skip:]))


    #plt.title(r'ESS $\propto d^{-\alpha}, \quad \alpha = $' + '{0}'.format(np.round(-res.slope, 2)))
    #plt.plot(dimensions, np.exp(res.intercept) * np.power(dimensions, res.slope), ':', color='black')
    plt.xlabel('condition number')
    plt.ylabel('ESS')
    plt.xscale('log')
    plt.yscale('log')

    #plt.savefig('Tests/bounce_dimension_dependence/'+folder_name+'.png')
    plt.show()




def ill_conditioned():
    """Figure 2"""


    ff, ff_title, ff_ticks = 18, 20, 17

    plt.rcParams['xtick.labelsize'] = ff_ticks
    plt.rcParams['ytick.labelsize'] = ff_ticks
    plt.figure(figsize= (20, 8))
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    kappa = np.logspace(0, 5, 18)


    ess= [np.max(np.load('Tests/data/kappa/' + str(i) + '.npy')[:, 0]) for i in range(18)]
    plt.plot(kappa, ess, 'o:', color = 'tab:blue',  label = 'MCHMC (fine tuned)')

    ess_mchmc = np.load('Tests/data/kappa/L1.5.npy')[:, 0]
    plt.plot(kappa, ess_mchmc, 'o:', color = 'tab:blue', alpha = 0.5, label = 'MCHMC (tuning free)')

    ess_nuts = np.load('Tests/data/kappa_rotated_NUTS.npy')[0]
    plt.plot(kappa, ess_nuts, 'o:', color = 'tab:orange', label = 'NUTS')

    plt.ylabel('ESS', fontsize= ff)
    plt.xlabel('condition number', fontsize= ff)
    plt.xscale('log')
    plt.yscale('log')
    plt.legend(fontsize= ff)
    plt.savefig('submission/kappa.pdf')
    plt.show()



def Bimodal():
    """Figure 3"""

    ff, ff_title, ff_ticks = 19, 20, 17
    plt.rcParams['xtick.labelsize'] = ff_ticks
    plt.rcParams['ytick.labelsize'] = ff_ticks
    plt.figure(figsize=(20, 8))
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    mu = np.arange(1, 9)

    plt.plot(mu, np.load('Tests/data/mode_mixing_d50_L1.5.npy')[:, 0], 'o:', label='MCHMC')


    nuts_results = np.load('Tests/data/mode_mixing_NUTS.npy')

    plt.plot(nuts_results[1], nuts_results[0], 'o:', label= 'NUTS')


    plt.yscale('log')
    plt.xlabel(r'$\mu$', fontsize = ff)
    plt.ylabel('average steps spent in a mode', fontsize = ff)
    plt.legend(fontsize = ff)
    plt.savefig('submission/mode_mixing.pdf')

    plt.show()


def Funnel():
    """Figure 4"""

    def gaussianize(z, theta):
        return (z.T * np.exp(-0.5 * theta)).T, theta / 3.0

    eps, free_time = 0.1, 6
    data = np.load('Tests/data/funnel_free'+str(free_time) + '_eps'+str(eps)+'.npz')
    z, theta, w = data['z'], data['theta'], data['w']


    data = np.load('Tests/data/funnel_HMC.npz')
    zHMC, thetaHMC = data['z'], data['theta']


    ff, ff_title, ff_ticks = 18, 20, 14
    plt.rcParams['xtick.labelsize'] = ff_ticks
    plt.rcParams['ytick.labelsize'] = ff_ticks
    plt.figure(figsize=(24, 8))
    ff, ff_title, ff_ticks = 18, 20, 16



    ####   2d marginal in the original coordinates ####
    plt.subplot(1, 3, 1)
    plt.title('Original coordinates', fontsize = ff_title)
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.plot(zHMC[:, 0], thetaHMC, '.', ms= 1, color = 'tab:orange', label = 'NUTS')

    #plt.hist2d(z[:, 0], theta, cmap = 'Blues', weights= w, bins = 70, density=True, range= [[-30, 30], [-8, 8]], label ='MCHMC')
    plt.plot(z[::5000, 0], theta[::5000], '.', ms= 1, color = 'tab:blue', label = 'MCHMC')

    #plt.hist2d(z[:, 0], theta, weights= w, bins = 100, density=True, label = 'MCHMC')
    plt.xlim(-30, 30)
    plt.ylim(-8, 8)
    plt.xlabel(r'$z_1$', fontsize = ff)
    plt.ylabel(r'$\theta$', fontsize = ff)

    #### 2d marginal in the gaussianized coordinates ####
    plt.subplot(1, 3, 2)
    plt.title('Gaussianized coordinates', fontsize = ff_title)
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    Gz, Gtheta = gaussianize(z, theta)
    plt.hexbin(Gz[:, 0], Gtheta, C= w, cmap='Blues', gridsize=50, label='MCHMC', reduce_C_function=np.sum)

    GzHMC, GthetaHMC = gaussianize(zHMC, thetaHMC)
    plt.plot(GzHMC[:, 0], GthetaHMC, '.', ms= 4, color = 'tab:orange', alpha = 0.5, label ='NUTS')

    #level sets
    p_level = np.array([0.6827, 0.9545])
    x_level = np.sqrt(-2 * np.log(1 - p_level))
    phi = np.linspace(0, 2* np.pi, 100)
    for i in range(2):
        plt.plot(x_level[i] * np.cos(phi), x_level[i] * np.sin(phi), color = 'black', alpha= ([1, 0.5])[i])

    plt.xlabel(r'$\widetilde{z_1}$', fontsize = ff)
    plt.ylabel(r'$\widetilde{\theta}$', fontsize = ff)
    plt.xlim(-3, 3)
    plt.ylim(-3, 3)


    #### 1d theta marginal####
    plt.subplot(1, 3, 3)
    plt.title(r'$\theta$-marginal', fontsize = ff_title)
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.hist(thetaHMC, color='tab:orange', density=True, bins = 20, alpha = 0.5, label = 'NUTS')
    plt.hist(theta, weights= w, color='tab:blue', density=True, bins = 20, alpha = 0.5,  label = 'MCHMC')

    t= np.linspace(-10, 10, 100)
    plt.plot(t, norm.pdf(t, scale= 3.0), color= 'black', label = 'exact')

    #xmax = np.min([np.max(thetaHMC), np.max(theta)])
    #plt.xlim(-xmax, xmax)
    #plt.ylim(0, 1)


    plt.legend(fontsize = ff)
    plt.xlabel(r'$\theta$', fontsize = ff)
    plt.ylabel(r'$p(\theta)$', fontsize = ff)
    plt.savefig('submission/funnel.pdf')

    plt.show()





def Rosenbrock():
    """Figure 5"""

    xmin, xmax, ymin, ymax = -2.3, 3.9, -2, 16

    #ff_ticks =
    #plt.rcParams['xtick.labelsize'] = ff_ticks
    #plt.rcParams['ytick.labelsize'] = ff_ticks
    plot = sns.JointGrid(height=10, xlim=(xmin, xmax), ylim=(ymin, ymax))
    ff = 20

    # MCHMC
    d = 36
    X = np.load('Tests/data/rosenbrock.npz')
    x, y = X['samples'][:, 0], X['samples'][:, d // 2]
    w = X['w']
    sns.histplot(x=x, y=y, weights=w, bins=200, ax=plot.ax_joint)

    #sns.scatterplot(x=[], y=[], ax= plot.ax_joint, color = 'tab:blue')

    # # marginals
    sns.histplot(x= x, weights= w, bins= 40, fill= True, alpha = 0.5, linewidth= 0, ax= plot.ax_marg_x, stat= 'density', color= 'tab:blue', zorder = 2)
    sns.histplot(y= y, weights= w, bins= 40, fill= True, alpha = 0.5, linewidth= 0, ax= plot.ax_marg_y, stat= 'density', color= 'tab:blue', label= 'MCHMC', zorder = 2)


    # NUTS
    X= np.load('Tests/data/rosenbrock_HMC.npz')
    x, y = X['x'][:, 0], X['y'][:, 0]

    sns.scatterplot(x, y, s= 6, linewidth= 0, ax= plot.ax_joint, alpha = 0.7, color= 'tab:orange')

    # marginals
    sns.histplot(x=x, bins= 40, fill= True, alpha = 0.5, linewidth= 0, ax= plot.ax_marg_x, stat= 'density', color= 'tab:orange', zorder = 1)
    sns.histplot(y=y, bins= 40, fill= True, alpha = 0.5, linewidth= 0, ax= plot.ax_marg_y, stat= 'density', color= 'tab:orange', label= 'NUTS', zorder = 1)


    #exact
    import targets
    ros = targets.Rosenbrock(d = 2)
    X = ros.draw(1000)
    x, y = X[:, 0], X[:, 1]

    sns.scatterplot(x, y, s= 6, linewidth= 0, ax= plot.ax_joint, color= 'black', alpha = 0.5)

    # marginals
    sns.lineplot(x, np.exp(-0.5 * np.square(x - 1)) / np.sqrt(2 * np.pi), linewidth= 1, ax= plot.ax_marg_x, color= 'black', alpha = 0.5)
    ros = targets.Rosenbrock(d=2)
    X = ros.draw(5000000)
    x, y = X[:, 0], X[:, 1]
    sns.histplot(y=y, bins= 2000, fill= False, element= 'step', linewidth= 1, ax= plot.ax_marg_y, stat= 'density', color= 'black', alpha = 0.5, label= 'exact')


    plot.ax_marg_y.legend(fontsize = ff)

    plot.set_axis_labels(r'$x_1$', r'$y_1$', fontsize= ff)
    plt.tight_layout()
    plt.savefig('submission/rosenbrock.pdf')
    plt.show()



### old functions ###

def ess_epsilon():

    X = np.load('Tests/eps3.npy')
    plt.plot(X[:, 2], X[:, 0] , '.', color = 'black')

    plt.ylabel('ESS')
    plt.xlabel(r"$\epsilon$")
    #plt.savefig('Tests/eps_fine_tuning.png')
    plt.show()



def energy():
    eps_arr = [0.05, 0.1, 0.5, 1, 2]

    var = []
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    for n in range(len(eps_arr)):

        E = np.load('Tests/energy/E'+str(n)+'.npy')
        var.append(np.std(E))
        plt.plot(np.arange(1, 1+len(E))[::1000], E[::1000], label = r'$\epsilon$ = {0}'.format(eps_arr[n]), zorder = -n, color = tab_colors[n])


    plt.legend(loc= 4)
    plt.xlabel('rescaled time')
    plt.ylabel('energy')
    #plt.xscale('log')
    plt.xlim(1, 1e6)

    plt.subplot(1, 2, 2)
    for n in range(len(eps_arr)):
        plt.plot([eps_arr[n], ], [var[n], ], 'o', color = tab_colors[n])
    plt.yscale('log')
    plt.xlabel(r'$\epsilon$')
    plt.ylabel('STD[energy]')

    plt.savefig('Tests/energy.png')
    plt.show()



def funnel_debug():

    data = np.load('Tests/data/funnel.npz')
    z, theta, w = data['z'], data['theta'], data['w']

    data = np.load('Tests/data/funnel_HMC.npz')
    zHMC, thetaHMC = data['z'], data['theta']


    num = 100000
    plt.plot(z[:num, 0], theta[:num])
    plt.plot(zHMC[:, 0], thetaHMC, '.', ms=1, color='tab:orange', label='NUTS')
    # plt.xlim(-30, 30)
    # plt.ylim(-8, 8)
    plt.xlabel(r'$z_0$')
    plt.ylabel(r'$\theta$')
    plt.show()


def dimension_dependence():
    ###  dimension dependence ###
    plt.subplot(1, 2, 1)
    dimensions = [50, 100, 200, 500, 1000, 3000, 10000]
    markers = ['o:', 's:', 'v:']

    # tuned MCHMC
    target_names = ['StandardNormal_t', 'Kappa100_t', 'Rosenbrock_t']
    for i in range(len(target_names)):
        if i == 2:
            dim = [50, 100, 200, 500, 1000, 3000]
        else:
            dim = dimensions
        ess = [np.max(np.load('Tests/data/dimensions/' + target_names[i] + '/' + str(d) + '.npy')[:, 0]) for d in dim]
        plt.plot(dim, ess, markers[i], color='tab:blue')

    # NUTS
    target_names = ['StandardNormal', 'Kappa100', 'Rosenbrock']
    for i in range(len(target_names)):
        ess = np.load('Tests/data/dimensions/' + target_names[i] + '_NUTS.npy')[0]
        plt.plot(dimensions, ess, markers[i], color='tab:orange')

    plt.xlabel('d', fontsize=ff)
    plt.ylabel('ESS', fontsize=ff)
    plt.xscale('log')
    plt.yscale('log')
    plt.xticks([100, 1000, 10000], [r'$10^2$', r'$10^3$', r'$10^4$'])



def langevin():

    ymax = 0.015
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 2, 1)
    plt.title('Langevin')
    X = np.load('Tests/data/langevin_kappa10000.npy')
    plt.plot(X[:, 1], X[:, 0], 'o:')
    plt.ylim(0, ymax)
    plt.ylabel('ESS')
    plt.xlabel(r'$\eta$')
    plt.xscale('log')

    plt.subplot(1, 2, 2)
    X = np.load('Tests/data/no_langevin_kappa10000.npy')
    plt.title('Bounces')
    plt.plot(X[:, 1] / np.sqrt(100), X[:, 0], 'o:')
    plt.ylim(0, ymax)
    plt.xscale('log')
    plt.xlabel(r'$\alpha$')

    plt.savefig('Langevin_kappa10000.png')

    plt.show()

#bounce_frequency_full_bias()
#ill_conditioned()
#Bimodal()

#Funnel()
#Rosenbrock()

langevin()
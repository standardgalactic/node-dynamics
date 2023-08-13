"""
Visualization module.

This module contains functions for visualizing the results of the node dynamics with triadic interactions.
"""

# Import necessary packages
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import types

# Matplotlib configuration
MPL_CONFIG = {
    # Figure style
    'figure.figsize' : (3, 2.5),        # specify figure size
    # Font style
    'font.size' : 7,                    # specify default font size
    # Axes style
    'axes.labelsize' : 9,               # specify axes label size
    'axes.linewidth' : 0.5,             # specify axes line width
    # X-ticks style
    'xtick.direction' : 'in',           # specify x ticks direction
    'xtick.major.size' : 3,             # specify x ticks major size
    'xtick.major.width' : 0.5,          # specify x ticks major width
    'xtick.minor.size' : 1.5,           # specify x ticks minor size
    'xtick.minor.width' : 0.5,          # specify x ticks minor width
    'xtick.minor.visible' : False,      # specify x ticks minor visible
    'xtick.labelsize' : 7,              # specify x ticks label size
    'xtick.top' : True,                 # specify x ticks on top
    # Y-ticks style
    'ytick.direction' : 'in',           # specify y ticks direction
    'ytick.major.size' : 3,             # specify y ticks major size
    'ytick.major.width' : 0.5,          # specify y ticks major width
    'ytick.minor.size' : 1.5,           # specify y ticks minor size
    'ytick.minor.width' : 0.5,          # specify y ticks minor width
    'ytick.minor.visible' : False,      # specify y ticks minor visible
    'ytick.labelsize' : 7,              # specify y ticks label size
    'ytick.right' : True,               # specify y ticks on right
    # Line style
    'lines.linewidth' : 1.0,            # specify line width
    'lines.markersize' : 3,             # specify marker size
    # Grid style
    'grid.linewidth' : 0.5,             # specify grid line width
    # Legend style
    'legend.fontsize' : 6,              # specify legend label size
    'legend.frameon' : False,           # specify legend frame off
    'legend.loc' : 'best',              # specify legend position
    'legend.handlelength' : 2.5,        # specify legend handle length
    # Savefig style
    'savefig.bbox' : 'tight',           # specify savefig bbox
    'savefig.pad_inches' : 0.05,        # specify savefig pad inches
    'savefig.transparent' : True,       # specify savefig transparency
    # Mathtext style
    'mathtext.default' : 'regular',     # specify mathtext font
}

def plot_timeseries(X, output_file, t_max, n_samples=1, separate=False, theory=None):
    """Plot the timeseries.

    Parameters
    ----------
    X : numpy.ndarray of shape (n_nodes, n_timesteps, n_samples)
        The timeseries data.
    output_file : str
        The output file name.
    t_max : float
        The maximum time span.
    n_samples : int, optional
         (Default value = 1)
        The number of samples.
    separate : bool, optional
         (Default value = False)
        If True, plot each node separately.
    theory : function, optional
         (Default value = None)
        The theoretical solution.
    
    Returns
    -------
    None

    """
    # Update matplotlib rcParams
    plt.rcParams.update(MPL_CONFIG)

    # Get the number of nodes and timesteps
    n_nodes = X.shape[0]
    n_timesteps = X.shape[1]

    # Define the time span
    T = np.linspace(0., t_max, n_timesteps)

    # If not separate, plot all nodes in one figure
    if not separate:
        # Create a figure
        fig, ax = plt.subplots()

        # Loop over samples
        for i in range(n_samples):
            # Loop over nodes
            for n in range(n_nodes):
                # Plot the timeseries
                ax.plot(
                    T, 
                    X[n, :, i], 
                    label="node {}, sample# {}".format(
                        n+1, 
                        i+1
                    ), 
                    alpha=0.5
                )

        # Set the x and y labels
        ax.set_xlabel("$T$")
        ax.set_ylabel("$X_{i}$")

        # Set the x and y limits
        ax.set_xlim(0, t_max)

        # Add the legend
        ax.legend(
            loc='center left', 
            bbox_to_anchor=(1, 0.5), 
            fontsize=6
        )
    
    # If separate, plot each node in a separate figure
    else:

        # Create a figure
        fig, ax = plt.subplots(
            nrows=n_nodes, 
            ncols=1, 
            figsize=(4, 5), 
            sharex=True
        )
        # Loop over samples
        for i in range(n_samples):
            # Loop over nodes
            for n in range(n_nodes):
                # Plot the timeseries
                ax[n].plot(
                    T, 
                    X[n, :, i], 
                    label="node {}, sample# {}".format(n+1, i+1), 
                    alpha=0.5
                )
                # Set the y labels and x limits
                ax[n].set_ylabel("$X_{}$".format(n+1))
                ax[n].set_xlim(0, t_max)
                
        # Loop over nodes
        for n in range(n_nodes):
            # Plot the average
            ax[n].plot(
                T, 
                np.mean(X[n, :, :], axis=1), 
                "k--", 
                label="node {} average".format(n+1), 
                alpha=0.5
            )
        
        # Plot the theory if provided 
        if theory is not None:
            ax[0].plot(
                T, 
                theory(T), 
                "r-.", 
                label='no TI'
            )

        # Set the x labels
        ax[-1].set_xlabel("$T$")

    # Apply tight layout
    fig.tight_layout()

    # Save the figure
    fig.savefig(output_file)

    # Close the figure
    plt.close(fig)

def plot_pdf(probs, bins, output_file, f_theory=None, logscale=False, parallel=False):
    """Plot the probability distributions.

    Parameters
    ----------
    probs : list of numpy.ndarray of shape (n_nodes, n_bins)
        The probability distributions for all nodes.
    bins : list of numpy.ndarray of shape (n_nodes, n_bins)
        The bins for all nodes.
    output_file : str
        The output file name.
    f_theory : function, optional
         (Default value = None)
        The theoretical solution.
    logscale : bool, optional
         (Default value = False)
        If True, plot the log scale.
    parallel : bool, optional
         (Default value = False)
        If True, plot each node separately.
    
    Returns
    -------
    None
    
    """
    # Update matplotlib rcParams
    plt.rcParams.update(MPL_CONFIG)

    # Get the number of nodes
    n_nodes = len(probs)

    # Get the min and max of the bins
    Xmin = [np.min(bins[i]) for i in range(n_nodes)]
    Xmax = [np.max(bins[i]) for i in range(n_nodes)]

    # Plot the histogram
    if not parallel:
        x_min = min(Xmin)
        x_max = max(Xmax)

        # Create the figure
        fig, ax = plt.subplots()
        
        # Set the labels
        ax.set_xlabel(r'$X_{i}$')
        ax.set_ylabel(r'PDF $p^{\rm{st}}(X_{i})$')
        
        # Set the limits
        ax.set_xlim(x_min, x_max)

        # Loop over nodes
        for i in range(n_nodes):

            if probs[i].ndim == 1:
                # Plot the histogram
                ax.scatter(
                    bins[i], 
                    probs[i], 
                    label="X_{i}".format(i=i+1),
                    edgecolors='r',
                    facecolors='none',
                    marker='o'
                )
            elif probs[i].ndim == 2:
                # Plot the histogram
                ax.scatter(
                    bins[i], 
                    np.mean(probs[i], axis=1), 
                    label="X_{i}".format(i=i+1),
                    facecolors='none',
                    edgecolors='r',
                    marker='o'
                )
                if not logscale:
                    ax.errorbar(
                        bins[i],
                        np.mean(probs[i], axis=1),
                        yerr=np.std(probs[i], axis=1) / np.sqrt(probs[i].shape[1]),
                        fmt='none', 
                        color='r', 
                        ecolor='r', 
                        elinewidth=1, 
                        capsize=2, 
                        alpha=0.5
                    )
        
        # Plot the theory
        if f_theory is not None:
            # Create the x values
            x_theory = np.linspace(x_min, x_max) # default num points = 50

            # Loop over nodes
            for i in range(n_nodes):
                # Get the theory
                p_theory = f_theory[i](x_theory)

                # Plot the theory
                ax.plot(
                    x_theory, 
                    p_theory, 
                    "--", 
                    label="theory ($X_{i}$)".format(i=i+1)
                )
        
        # Set the yscale to log
        if logscale:
            ax.set_yscale("log")

    # Plot each node separately
    else:
        # Create the figure
        fig, axs = plt.subplots(
            nrows=1, 
            ncols=n_nodes, 
            sharey=True, 
            figsize=(n_nodes*2.5, 2.5)
        )
        
        # Set the y-axis label
        axs[0].set_ylabel(r'PDF $p^{\rm{st}}(X_{i})$')

        # Loop over nodes
        for i in range(n_nodes):
            if probs[i].ndim == 1 or \
                (probs[i].ndim == 2 and probs[i].shape[1] == 1):
                # Plot the histogram
                axs[i].scatter(
                    bins[i],
                    probs[i],
                    edgecolors='r',
                    facecolors='none',
                    marker='o'
                )
            elif probs[i].ndim == 2:
                # Plot the histogram
                axs[i].scatter(
                    bins[i], 
                    np.mean(probs[i], axis=1),
                    facecolors='none',
                    edgecolors='r',
                    marker='o',
                )

                axs[i].errorbar(
                    bins[i],
                    np.mean(probs[i], axis=1),
                    yerr=np.std(probs[i], axis=1) / np.sqrt(probs[i].shape[1]),
                    fmt='none', 
                    color='r', 
                    ecolor='r', 
                    elinewidth=1, 
                    capsize=2, 
                    alpha=0.5
                )

            # Set the x-axis
            axs[i].set_xlabel("$X_{i}$".format(i=i+1))
            axs[i].set_xlim(
                Xmin[i],
                Xmax[i]
            )

            # Set the yscale to log
            if logscale:
                axs[i].set_yscale("log")
        
            # Plot the theory
            if f_theory is not None:
                # Create the x values
                x_theory = np.linspace(Xmin[i], Xmax[i], num=100)

                # Get the theory
                p_theory = f_theory[i](x_theory)

                # Plot the theory
                axs[i].plot(
                    x_theory, 
                    p_theory, 
                    "k--", 
                    label='no TI'
                )

                # Set the legend
                axs[i].legend()
        
    # Set the layout
    fig.tight_layout()

    # Save the figure
    fig.savefig(output_file)

    # Close the figure
    plt.close(fig)

def plot_covariance(cov, output_file, theory=None):
    """Plot the covariance matrix.

    Parameters
    ----------
    cov : numpy.ndarray of shape (n_nodes, n_nodes)
        The covariance matrix.
    output_file : str
        The output file name.
    theory : function, optional
         (Default value = None)
        The theoretical solution.
    
    Returns
    -------
    None

    """
    # Set the labels
    labels = [
        '$\Sigma_{11}$', '$\Sigma_{12}$', '$\Sigma_{13}$',
        '$\Sigma_{21}$', '$\Sigma_{22}$', '$\Sigma_{23}$',
        '$\Sigma_{31}$', '$\Sigma_{32}$', '$\Sigma_{33}$'
    ]

    # Set the style of the plot
    plt.rcParams.update(
        MPL_CONFIG
    )

    # Create a figure
    fig, ax = plt.subplots()
    
    # Create violin plots for each categorical data
    parts = ax.violinplot(
        cov, 
        showmedians=False, 
        showmeans=False, 
        showextrema=False
    )

    # Customize the style of violin plots
    colors = [
        '#8c8cd1', '#7fb2e2', '#7bd4d7', 
        '#7cdd9e', '#92d874', '#b4d645', 
        '#d5ca47', '#f5b43d', '#f58b33'
    ]
    linewidths = [0.5] * 9

    # Set the color of each violin
    for i, pc in enumerate(parts['bodies']):
        pc.set_facecolor(colors[i])
        pc.set_edgecolor('black')
        pc.set_linewidths(linewidths[i])

    # Mean
    mean = np.mean(
        cov, 
        axis=0
    )

    # 25th, 50th, and 75th percentiles
    quartile1, medians, quartile3 = np.percentile(
        cov, 
        [25, 50, 75], 
        axis=0
    )
    
    # Min and max whiskers
    whiskers_min = np.min(
        cov, 
        axis=0
    )
    whiskers_max = np.max(
        cov, 
        axis=0
    )
    
    # Set the x-axis
    inds = np.arange(1, len(medians) + 1)
    
    # Plot the mean
    ax.scatter(
        inds, mean, 
        marker='.', 
        s=4, 
        color='white', 
        zorder=3
    )
    
    # Plot the percentiles
    ax.vlines(
        inds, 
        quartile1, quartile3, 
        color='gray', 
        linestyle='-', 
        lw=3
    )

    # Plot the whiskers
    ax.vlines(
        inds, 
        whiskers_min, 
        whiskers_max, 
        color='gray', 
        linestyle='-', 
        lw=.75
    )

    # Plot the median
    ax.hlines(
        medians, 
        inds-7.5e-2, inds+7.5e-2, 
        color='black', 
        linestyle='-', 
        lw=.5
    )

    # Plot the theoretical solution
    if theory is not None:
        ax.scatter(
            inds, 
            theory, 
            marker='x', 
            color='r', 
            label='no TI', 
            zorder=4
        )
        # Set the legend
        ax.legend()

    # Set the x-axis 
    ax.set_xticks(inds)
    ax.set_xticklabels(labels)
    ax.set_xlabel('$(i, j)$')
    
    # Set the y-axis
    ax.set_ylabel('Covariance $\Sigma_{ij}$')
    
    # Apply the layout
    fig.tight_layout()
    
    # Save the figure
    fig.savefig(output_file)

    # Close the figure
    plt.close(fig)

def plot_conditional_expectation(Xgrids, cond_exps, stds, orders, output_file=None, theory=None):
    """Plot the conditional expectation.
    
    Parameter
    ---------
    Xgrids : numpy.ndarray of shape (n_bins,) or list of numpy.ndarray of shape (n_bins,)
        The grid of the conditional variable.
    cond_exps : numpy.ndarray of shape (n_bins, n_samples) or list of numpy.ndarray of shape (n_bins, n_samples)
        The conditional expectations.
    std : numpy.ndarray of shape (n_bins, n_samples) or list of numpy.ndarray of shape (n_bins, n_samples)
        The standard deviation of the conditional expectations.
    orders : tuples or list of tuples
        The order of the nodes.
    output_file : str, optional
        The output file name.
    theory : function or list of functions, optional
            (Default value = None)
        The theoretical solutions.

    Returns
    -------
    None

    """
    # Set the style of the plot
    plt.rcParams.update(MPL_CONFIG)

    # If the input is an array
    if isinstance(Xgrids, list):
        # Set the number of columns
        n_cols = len(Xgrids)

        # Create a figure
        fig, ax = plt.subplots(
            nrows=2, 
            ncols=n_cols, 
            figsize=(2.5 * n_cols, 5)
        ) # sharex=True

        # Plot the conditional expectation
        for i in range(n_cols):
            for j in range(2):
                # Plot the conditional expectation and its standard deviation
                ax[j, i].scatter(
                    Xgrids[i], 
                    cond_exps[i][j], 
                    marker='o',
                    edgecolors='r',
                    facecolors='none'
                )
                ax[j, i].errorbar(
                    Xgrids[i], 
                    cond_exps[i][j], 
                    yerr=stds[i][j] / np.sqrt(stds[i][j].shape[0]),
                    fmt='none', 
                    color='r', 
                    ecolor='r', 
                    elinewidth=1, 
                    capsize=2, 
                    alpha=0.5
                )

                # Set the labels
                ax[j, i].set_ylabel(
                    '$\mathbb{E}$' + '$[X_{} \mid X_{}]$'.format(orders[i][j], orders[i][2])
                )

                if theory is not None:
                    # Plot the theoretical solution
                    ax[j, i].plot(
                        Xgrids[i], 
                        theory[i][j](Xgrids[i]), 
                        "k--",
                        label='no TI'
                    )
                    # Set the legend
                    ax[j, i].legend()

            # Set the x-axis
            ax[-1, i].set_xlabel(
                '$X_{}$'.format(orders[i][2])
            )
    
    # If the input is an array
    else:
        # Create a figure
        fig, ax = plt.subplots(
            ncols=2, 
            figsize=(6, 3), 
            sharex=True
        )
        # Plot the conditional expectation
        for i in range(2):
            # Plot the conditional expectation and its standard deviation
            ax[i].scatter(
                Xgrids, cond_exps[i], 
                yerr=stds[i], 
                marker='o',
                facecolors='none',
                edgecolors='r'
            )
            ax[i].errorbar(
                Xgrids, cond_exps[i], 
                yerr=stds[i] / np.sqrt(stds.shape[1]), 
                fmt='o', 
                color='r', 
                ecolor='r', 
                elinewidth=1, 
                capsize=2, 
                alpha=0.5
            )

            # Set the x-labels
            ax[i].set_xlabel('$X_{}$'.format(orders[2]))

            # Set the y-labels
            ax[i].set_ylabel('$\mathbb{E}$' + '$[X_{} \mid X_{}]$'.format(orders[i], orders[2]))
        
            # Plot the theoretical solution
            if theory is not None:
                ax[i].plot(
                    Xgrids, 
                    theory[i](Xgrids), 
                    color='k--', 
                    label='no TI'
                )
                # Set the legend
                ax[i].legend()
        
    # Apply the layout
    fig.tight_layout()

    # Save the figure
    fig.savefig(output_file)

    # Close the figure
    plt.close(fig)

def plot_conditional_correlation(Xgrids, cond_corr, order, output_file, std=False, Xrange=None, theory=None, f_supplement=None, threshold=None):
    """Plot the conditional correlation.
    
    Parameter
    ---------
    Xgrids : numpy.ndarray of shape (n_bins,) or list of numpy.ndarray of shape (n_bins,)
        The grid of the conditional variable.
    cond_corr : numpy.ndarray of shape (n_bins, n_samples) or list of numpy.ndarray of shape (n_bins, n_samples)
        The conditional correlation.
    order : tuples or list of tuples
        The order of the nodes.
    output_file : str
        The output file name.
    std : bool or  list of numpy.ndarray of shape (n_bins, n_samples), optional
         (default = False)
        If False, do not plot the standard error.
        If list, plot the standard error.
    Xrange : bool or list of tuples, optional
            (default = None)
        If None, do not set the range of the x-axis.
        If list, set the range of the x-axis.
    theory : function or list of functions, optional
            (default value = None)
        The theoretical solutions.
    f_supplement : function or list of functions, optional
            (default value = None)
        The supplementary functions.
    threshold : list of float, optional
            (default value = None)
        The threshold value
    Returns
    -------
    None

    """
    # Set the style of the plot
    plt.rcParams.update(MPL_CONFIG)

    # If the input is an array
    if isinstance(Xgrids, list):
        n_data = len(Xgrids)

        if Xrange is None:
            Xmin = [np.min(Xgrids[i]) for i in range(n_data)]
            Xmax = [np.max(Xgrids[i]) for i in range(n_data)]
        else:
            Xmin = [Xrange[i][0] for i in range(n_data)]
            Xmax = [Xrange[i][1] for i in range(n_data)]
        
        # Ymin = [theory[i](0) - 0.5 for i in range(n_data)]
        # Ymax = [theory[i](0) + 0.5 for i in range(n_data)]
        Ymin = [-1 for i in range(n_data)]
        Ymax = [1 for i in range(n_data)]
        
         
        # Create a figure
        fig, ax = plt.subplots(
            nrows=1, 
            ncols=len(Xgrids), 
            figsize=(len(Xgrids)*2.5, 2.5),
            # sharey=True
        )

        # Plot the conditional correlation
        for i in range(len(Xgrids)):
            # Plot the conditional correlation
            if cond_corr[i].ndim > 1:
                cond_corr_mean = np.nanmean(
                    cond_corr[i], 
                    axis=1
                )
                ax[i].scatter(
                    Xgrids[i], 
                    cond_corr_mean, 
                    color='r'
                )
            else:
                ax[i].scatter(
                    Xgrids[i], 
                    cond_corr[i], 
                    edgecolor='r',
                    facecolor='none',
                    # s=1
                )
                # If std is True
                if isinstance(std, list):
                    ax[i].errorbar(
                        Xgrids[i], 
                        cond_corr[i], 
                        yerr=std[i],
                        fmt='none', 
                        color='r', 
                        ecolor='r', 
                        elinewidth=1, 
                        capsize=2, 
                        alpha=0.5
                    )
            
            ax[i].set_xlim(
                Xmin[i],
                Xmax[i]
            )
            ax[i].set_ylim(
                Ymin[i],
                Ymax[i]
            )
            
            if theory is not None:
                # Plot the theoretical solution
                ax[i].plot(
                    Xgrids[i], 
                    theory[i](Xgrids[i]), 
                    'k--', 
                    label='no TI'
                )
            
            if f_supplement is not None:
                if isinstance(f_supplement, list):
                    if isinstance(f_supplement[i], types.FunctionType):
                        # Plot the theoretical solution
                        ax[i].plot(
                            Xgrids[i], 
                            f_supplement[i](Xgrids[i]), 
                            'k-.', 
                            label='supplement'
                        )
                    elif isinstance(f_supplement[i], tuple):
                        # Plot the theoretical solution
                        ax[i].plot(
                            Xgrids[i], 
                            f_supplement[i][0](Xgrids[i]), 
                            'k-.', 
                            label=f_supplement[i][1]
                        )
                elif isinstance(f_supplement, types.FunctionType):
                    # Plot the theoretical solution
                    ax[i].plot(
                        Xgrids[i], 
                        f_supplement(Xgrids[i]), 
                        'k-.', 
                        label='supplement'
                    )
                elif isinstance(f_supplement, dict):
                    if len(f_supplement) != len(Xgrids):
                        raise ValueError(
                            'The length of f_supplement must be the same as Xgrids if f_supplement is a dictionary.'
                        )
                    # Plot the theoretical solution
                    ax[i].plot(
                        Xgrids[i], 
                        f_supplement.values()[i](Xgrids[i]), 
                        'k-.', 
                        label=f_supplement.keys()[i]
                    )

            if threshold is not None:
                ax[i].axvline(threshold, linestyle=':', color='k')

            # Set the legend
            ax[i].legend(loc='lower right')
            
            # Set the labels
            ax[i].set_xlabel(
                '$X_{}$'.format(order[i][2])
            )
            ax[i].set_ylabel(
                r'$\rho(X_{}, X_{} \mid X_{})$'.format(
                    order[i][0], order[i][1], order[i][2]
                )
            )
        
    else:
        # Create a figure
        fig, ax = plt.subplots()
        
        # Ymin, Ymax = -1, 1
        
        if std is False:
            ax.scatter(
                Xgrids, 
                cond_corr, 
                edgecolor='r',
                facecolor='none'
            )
        else:
            ax.errorbar(
                Xgrids, 
                cond_corr_mean, 
                yerr=std, 
                fmt='none', 
                color='r', 
                ecolor='r', 
                elinewidth=1, 
                capsize=2, 
                alpha=0.5
            )
        
        
        if theory is not None:
            # Plot the theoretical solution
            ax.plot(
                Xgrids, 
                theory(Xgrids), 
                'k--', 
                label='no TI'
            )
            # Set the legend
            ax.legend()
            
        ax.set_xlim(
            np.min(Xgrids),
            np.max(Xgrids)
        )
        # ax.set_ylim(
        #     Ymin,
        #     Ymax
        # )

        # Set the labels
        ax.set_xlabel(
            '$X_{}$'.format(order[2])
        )
        ax.set_ylabel(
            r'$\rho(X_{}, X_{} \mid X_{})$'.format(order[0], order[1], order[2])
        )

    # Apply the layout
    fig.tight_layout()

    # Save the figure
    fig.savefig(output_file)
    
    # Close the figure
    plt.close(fig)

def plot_conditional_mutual_information(Xgrids, cmi, order, output_file, std=False, theory=None):
    """Plot conditional mutual information.
    
    Parameter
    ---------
    Xgrids : numpy.ndarray of shape (n_bins,) or list of numpy.ndarray of shape (n_bins,)
        The grid of the conditional variable.
    cmi : numpy.ndarray of shape (n_bins, n_samples) or list of numpy.ndarray of shape (n_bins, n_samples)
        The conditional mutual information.
    order : tuples or list of tuples
        The order of the nodes.
    output_file : str
        The output file name.
    std : bool, optional
         (default = False)
        If True, plot the standard deviation.
    theory : function or list of functions, optional
            (Default value = None)
        The theoretical solutions.

    Returns
    -------
    None

    """
    # Set the style of the plot
    plt.rcParams.update(MPL_CONFIG)

    # If the input is an array
    if isinstance(Xgrids, list):
        n_data = len(Xgrids)
        Xmin = [np.min(Xgrids[i]) for i in range(n_data)]
        Xmax = [np.max(Xgrids[i]) for i in range(n_data)]
        
        # Create a figure
        fig, ax = plt.subplots(
            nrows=1, 
            ncols=len(Xgrids), 
            figsize=(len(Xgrids)*2.5, 2.5),
            sharey=True
        )

        # Plot the conditional mutual information
        for i in range(len(Xgrids)):
            if len(cmi[i].shape) > 1:
                cmi_mean = np.mean(
                    cmi[i], 
                    axis=1
                )
                ax[i].scatter(
                    Xgrids[i], 
                    cmi_mean, 
                    edgecolor='r',
                    facecolor='none'
                )
                # If std is True
                if std:
                    # Plot the standard deviation
                    cmi_std = np.std(
                        cmi[i], 
                        axis=1
                    )
                    ax[i].errorbar(
                        Xgrids[i], 
                        cmi_mean, 
                        yerr=cmi_std / np.sqrt(cmi[i].shape[1]), 
                        fmt='none', 
                        color='r', 
                        ecolor='r', 
                        elinewidth=1, 
                        capsize=2, 
                        alpha=0.5
                    )
            else:
                ax[i].scatter(
                    Xgrids[i], 
                    cmi[i], 
                    edgecolor='r',
                    facecolor='none',
                    # s=1
                )
            # ax[i].axhline(0, color='k', linestyle='-', linewidth=0.5)
            
            if theory is not None:
                # Plot the theoretical solution
                ax[i].plot(
                    Xgrids[i], 
                    theory[i](Xgrids[i]), 
                    'k--', 
                    label='no TI'
                )
                # Set the legend
                ax[i].legend()
         
            ax[i].set_xlim(
                Xmin[i],
                Xmax[i]
            )
            
            # Set the labels
            ax[i].set_xlabel(
                '$X_{}$'.format(order[i][2])
            )
            ax[i].set_ylabel(
                '$I(X_{}; X_{} \mid X_{})$'.format(
                    order[i][0], order[i][1], order[i][2]
                )
            )
        
    else:
        # Create a figure
        fig, ax = plt.subplots()
        
        ax.scatter(
            Xgrids, 
            cmi, 
            edgecolor='r',
            facecolor='none'
        )
        if theory is not None:
            # Plot the theoretical solution
            ax.plot(
                Xgrids, 
                theory(Xgrids), 
                'k--', 
                label='no TI'
            )
            # Set the legend
            ax.legend()
        
        ax.set_xlim(
            np.min(Xgrids),
            np.max(Xgrids)
        )
        
        # Set the labels
        ax.set_xlabel(
            '$X_{}$'.format(order[2])
        )
        ax.set_ylabel(
            '$I(X_{}; X_{} \mid X_{})$'.format(order[0], order[1], order[2])
        )

    # Apply the layout
    fig.tight_layout()

    # Save the figure
    fig.savefig(output_file)
    
    # Close the figure
    plt.close(fig)

def visualise_evolution(evolution_data, x_grid, time_grid, output_file):
    """Visualise the evolution of probability density function.

    Parameters
    ----------
    evolution_data : numpy.ndarray of shape (n_nodes, n_bins, n_times)
        The evolution of probability density function.
    x_grid : numpy.ndarray of shape (n_bins,)
        The grid of the variable.
    time_grid : numpy.ndarray of shape (n_times,)
        The time grid.
    output_file : str
        The output file name.
    
    Returns
    -------
    None

    """
    # Set the style of the plot
    plt.rcParams.update(MPL_CONFIG)

    # plt.rcParams.update({
    #     'xtick.direction' : 'out',
    #     'xtick.top' : False,
    #     'ytick.direction' : 'out',
    #     'ytick.right' : False,
    # })

    norm = colors.LogNorm(
        vmin=np.min(evolution_data[evolution_data > 0.]), 
        vmax=np.max(evolution_data)
    )

    fig, ax = plt.subplots(nrows=3, figsize=(3,3.3))
    n_nodes = evolution_data.shape[0]

    for i in range(n_nodes):
        cax = ax[i].imshow(
            evolution_data[i], 
            cmap='inferno', 
            interpolation='none', 
            aspect='auto',
            norm=norm,
            extent=[
                np.min(time_grid), np.max(time_grid),
                np.min(x_grid), np.max(x_grid),
            ]
        )
        ax[i].set_ylabel("$X_{k}$".format(k=i+1))
        
        # ax[i].set_facecolor('k')
    
    cbar_ax = fig.add_axes([0.92, 0.12, 0.03, 0.75])
    # cbar_ax.set_visible(False)

    plt.colorbar(
        ax[2].get_images()[0], 
        cax=cbar_ax, 
        label='PDF $p(X_i, t)$', 
        orientation='vertical'
    )

    # ax[0].set_yticklabels(time_grid)
    ax[2].set_xlabel("$t$")

    # fig.tight_layout()
    
    # fig.tight_layout()
    fig.savefig(output_file)

"""End of file"""
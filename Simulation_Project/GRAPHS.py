import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
from scipy.stats import expon, uniform, poisson, gamma
from DATA import lambda_, meu


def GIAexpo(arr):
    # create the histogram
    plt.hist(arr, bins=np.max(arr), density=True, alpha=0.5, color='blue')
    # add labels and a title
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Inter Arrival [Exponential]')

    # add the function line for exponential distribution
    mean_ia = np.mean(arr)
    x = np.linspace(0, np.max(arr), 1000)
    y = lambda_ * np.exp(-lambda_ * x)

    # Plot exponential function line
    plt.plot(x, y, color='red', lw=2)

    # show the plot
    plt.show()


def GIAnorm(arr):
    # create the histogram
    plt.hist(arr, bins=np.max(arr), density=True, alpha=0.5, color='blue')

    # calculate mean and standard deviation
    IA_mean = np.mean(arr)
    IA_std = np.std(arr)

    # generate normal distribution with same mean and std as data
    x = np.linspace(np.min(arr), np.max(arr), 100)
    # y = scipy.stats.norm.pdf(x, loc=IA_mean, scale=IA_std)
    y = 1 / (IA_std * np.sqrt(2 * np.pi)) * np.exp(- (x - IA_mean) ** 2 / (2 * IA_std ** 2))

    # plot normal distribution function line
    plt.plot(x, y, 'r-', linewidth=2)

    # add labels and a title
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Inter Arrival [Normal]')

    # show the plot
    plt.show()


def GIAunif(arr):
    # create the histogram
    plt.hist(arr, bins=np.max(arr), density=True, alpha=0.5, color='blue')

    # add a function line for a uniform distribution
    a, b = np.min(arr), np.max(arr)
    x = np.linspace(a, b, 100)
    pdf = uniform.pdf(x, loc=a, scale=b - a)
    plt.plot(x, pdf, 'r-', lw=2)

    # add labels and a title
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Inter Arrival [Uniform]')

    # show the plot
    plt.show()


def GIApois(arr):
    # create the histogram
    plt.hist(arr, bins=np.max(arr), density=True, alpha=0.5, color='blue')

    # add a function line for a Poisson distribution
    mu = np.mean(arr)
    x = np.arange(0, np.max(arr))
    pmf = poisson.pmf(x, mu)
    plt.step(x, pmf, 'r-', lw=2)

    # add labels and a title
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Inter Arrival [Poisson]')

    # show the plot
    plt.show()


def GIAgamm(arr):
    # create the histogram
    plt.hist(arr, bins=np.max(arr), density=True, alpha=0.5, color='blue')

    # add a function line for a Gamma distribution
    shape, loc, scale = gamma.fit(arr)
    x = np.linspace(0, np.max(arr), 100)
    pdf = gamma.pdf(x, shape, loc=loc, scale=scale)
    plt.plot(x, pdf, 'r-', lw=2)

    # add labels and a title
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Inter Arrival [Gamma]')

    # show the plot
    plt.show()


def GSTexpo(arr):
    # create the histogram
    plt.hist(arr, bins=np.max(arr), density=True, alpha=0.5, color='grey')
    # add labels and a title
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Service Time [Exponential]')

    # add the function line for exponential distribution
    mean_st = np.mean(arr)
    x = np.linspace(0, np.max(arr), 1000)
    # plt.plot(x, expon.pdf(x, scale=mean_st), color='red', lw=2)
    y = meu * np.exp(-meu * x)

    # Plot exponential function line
    plt.plot(x, y, color='red', lw=2)

    # show the plot
    plt.show()


def GSTnorm(arr):
    # create the histogram
    plt.hist(arr, bins=np.max(arr), density=True, alpha=0.5, color='grey')

    # calculate mean and standard deviation
    ST_mean = np.mean(arr)
    ST_std = np.std(arr)

    # generate normal distribution with same mean and std as data
    x = np.linspace(np.min(arr), np.max(arr), 100)
    # y = scipy.stats.norm.pdf(x, loc=ST_mean, scale=ST_std)
    y = 1 / (ST_std * np.sqrt(2 * np.pi)) * np.exp(- (x - ST_mean) ** 2 / (2 * ST_std ** 2))
    # plot normal distribution function line
    plt.plot(x, y, 'r-', linewidth=2)

    # add labels and a title
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Service Time [Normal]')

    # show the plot
    plt.show()


def GSTunif(arr):
    # create the histogram
    plt.hist(arr, bins=np.max(arr), density=True, alpha=0.5, color='grey')

    # add a function line for a uniform distribution
    a, b = np.min(arr), np.max(arr)
    x = np.linspace(a, b, 100)
    pdf = uniform.pdf(x, loc=a, scale=b - a)
    plt.plot(x, pdf, 'r-', lw=2)

    # add labels and a title
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Service Time [Uniform]')

    # show the plot
    plt.show()


def GSTgamm(arr):
    # create the histogram
    plt.hist(arr, bins=np.max(arr), density=True, alpha=0.5, color='grey')

    # add a function line for a Gamma distribution
    shape, loc, scale = gamma.fit(arr)
    x = np.linspace(0, np.max(arr), 100)
    pdf = gamma.pdf(x, shape, loc=loc, scale=scale)
    plt.plot(x, pdf, 'r-', lw=2)

    # add labels and a title
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Service Time [Gamma]')

    # show the plot
    plt.show()


def GIA(dist, arr):
    if dist == 'Exponential':
        GIAexpo(arr)
    elif dist == 'Normal':
        GIAnorm(arr)
    elif dist == 'Uniform':
        GIAunif(arr)
    elif dist == 'Poisson':
        GIApois(arr)
    elif dist == 'Gamma':
        GIAgamm(arr)


def GST(dist, arr):
    if dist == 'Exponential':
        GSTexpo(arr)
    elif dist == 'Normal':
        GSTnorm(arr)
    elif dist == 'Uniform':
        GSTunif(arr)
    elif dist == 'Gamma':
        GSTgamm(arr)

from scipy.stats import norm

# distribution of sizes of adult males within populations (from https://ourworldindata.org/human-height)
mean = 1.784
std_dev = 0.0759

# probality to be 1.86 m or more
target = 1.86
p = 100.0 * (1.0 - norm.cdf(target, mean, std_dev))
print(f'probability of height equal to or greater than {target:.2f} m: {p:.2f} %')

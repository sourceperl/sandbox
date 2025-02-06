from scipy.stats import norm

# distribution of sizes of adult males within populations (from https://ourworldindata.org/human-height)
mean = 1.784
std_dev = 0.0759

# what is the probality to be 1.86 m or more ?
target_percent = 1.86
p = 100.0 * (1.0 - norm.cdf(target_percent, mean, std_dev))
print(f'probability of height equal to or greater than {target_percent:.2f} m: {p:.2f} %')

# what is the minimum height to be in the top 2% of tallest men ?
target_percent = 2.0
min_size = norm.ppf(1.0 - (target_percent/100), mean, std_dev)
print(f'the minimum height to be in the top {target_percent:.2f} % of tallest men is {min_size:.2f} m')

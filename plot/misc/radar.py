import matplotlib.pyplot as plt


# some function
def to_rad(deg_l: list) -> list:
    return [x/180.0*3.141593 for x in deg_l]


# data
radius = [40, 50, 75, 100]
ang_dg = [-60, 0, 75, 30]

# plot radar
ax = plt.subplot(111, projection='polar')
ax.set_theta_zero_location('N')
ax.set_thetamin(-90)
ax.set_thetamax(90)
ax.scatter(to_rad(ang_dg), radius, s=50, alpha=0.75)
plt.show()

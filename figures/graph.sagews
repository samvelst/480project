︠420026ea-44a1-4c42-a548-d48e5b550346s︠
import matplotlib.pyplot as plt

#New solution found with 17 volunteers and weight 94 in 0.0160090923309 seconds
#New solution found with 15 volunteers and weight 100 in 0.0322120189667 seconds
#New solution found with 15 volunteers and weight 108 in 0.454613924026 seconds
#New solution found with 15 volunteers and weight 110 in 0.671663045883 seconds
#New solution found with 15 volunteers and weight 118 in 0.76482796669 seconds
#New solution found with 14 volunteers and weight 108 in 1.02187299728 seconds
#New solution found with 14 volunteers and weight 114 in 7.10913991928 seconds
#New solution found with 14 volunteers and weight 124 in 9.84665799141 seconds
#New solution found with 14 volunteers and weight 140 in 24.3446891308 seconds
#New solution found with 14 volunteers and weight 144 in 58.2014439106 seconds

x = [0.016, 0.032, 0.45, 0.67, 0.76, 1.02, 7.1, 9.9, 24.4, 58.2]
y = [17, 15, 15, 15, 15, 14, 14, 14, 14, 14]
w = [94, 100, 108, 110, 118, 108, 114, 124, 140, 144]

plt.scatter(x,y, s=[((z-50)/5.0)**3 for z in w], alpha=.2, label="Total Weight")
plt.plot([0,60], [12,12], '--', label="Lower bound")

plt.title("Time to find optimal solution")
plt.xlabel('Computation time (in seconds)')
plt.ylabel('Volunteers Needed')
plt.axis([0,60, 11,18])

plt.legend(markerscale=0.1)


plt.show()











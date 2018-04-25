# This is a simple script that plots the Nbody results
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

system = "EPIC-210897587-2"
x = "e"     # plot on x axis
y = "m"     # plot on y axis

names = ["name","id","shadow","maxorbs","P1","sim_time","Energy_err","elapsed_time"]
data = pd.read_csv("systems/%s_data.csv"%system)
Nbody = pd.read_csv("systems/%s_Nbodyresults.csv"%system, names=names)

simtime = np.log10(Nbody["sim_time"].values/Nbody["P1"])
ids = Nbody["id"]

# plot distribution of results
colorbar = 'winter'
fontsize = 10
f, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=[13, 4])
ax1.scatter(data["%s1"%x][ids], data["%s1"%y][ids], c=simtime, cmap=colorbar, lw=0)
ax2.scatter(data["%s2"%x][ids], data["%s2"%y][ids], c=simtime, cmap=colorbar, lw=0)
c=ax3.scatter(data["%s3"%x][ids], data["%s3"%y][ids], c=simtime, cmap=colorbar, lw=0)

ax1.set_ylabel(y, fontsize=fontsize)
ax1.set_xlabel(x, fontsize=fontsize)
ax2.set_xlabel(x, fontsize=fontsize)
ax3.set_xlabel(x, fontsize=fontsize)
ax1.set_title("Planet 1")
ax2.set_title("Planet 2")
ax3.set_title("Planet 3")
cbar = plt.colorbar(c)
cbar.ax.set_ylabel("Number P1 Orbital Periods")  # vertically oriented colorbar
plt.savefig("output/images/%s_%s_vs_%s.png"%(system,x,y))
plt.close()

# plot histogram of Nbody results
_, _, _ = plt.hist(simtime)
plt.xlabel("log10(# orbital periods before instability)")
plt.ylabel("counts")
plt.title("Distribution of %d instability times for %s"%(len(simtime),system))
plt.savefig("output/images/%s_insta_times.png"%system)

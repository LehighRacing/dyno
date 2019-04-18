import sys

import matplotlib.pyplot as plt
import pandas


filepath = sys.argv[1]

data = pandas.read_csv(filepath, header=0, skipinitialspace=True)

rpm_range = range(0, 11001, 250)
rpm_range_ticks = range(0, 11001, 500)

data["rpm_bucket"] = pandas.cut(data["rpm"], pandas.Series(rpm_range), labels=False, include_lowest=True)

buckets = data.groupby("rpm_bucket")

med_rpm = buckets["rpm"].median()
max_hp = buckets["hp"].max()
max_torque = buckets["torque"].max()

table = med_rpm.to_frame().join([max_hp, max_torque])
print(table)

# print(table.join([table.index * 500]))

table = table.set_index('rpm')

table.plot()

ax = plt.gca()

# X Axis
plt.xticks(rpm_range_ticks)
ax.xaxis.set_major_locator(plt.MultipleLocator(1000))
ax.xaxis.set_minor_locator(plt.MultipleLocator(500))

# Y Axis
ax.yaxis.set_major_locator(plt.MultipleLocator(10))
ax.yaxis.set_minor_locator(plt.MultipleLocator(5))

plt.grid(which='both')
plt.savefig('{}.png'.format(filepath))

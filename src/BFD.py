# Implementation of the BFD (Best Fit Decreasing) algorithm
# Runs in poly-time, but not guaranteed to return optimal results
# BFD returns optimal roughly 95% of the time though...

import random
import math
import sswing_scheduler as SS

# Set Up
V = []
for x in xrange(1, 61):
    name = "Volunteer " + str(x)
    capacity = random.randint(2, 6)
    volunteer = SS.Volunteer(name, capacity)
    available_start = random.randint(0,18)
    volunteer.add_job(SS.Job("UNAVAILABLE", (0, available_start)))
    volunteer.add_job(SS.Job("UNAVAILABLE", (available_start+capacity, 24)))
    V.append(volunteer)

J = []
for y in xrange(1, 31):
   name = "Job " + str(y)
   time_interval = SS.rand_time_interval(0,21)
   job = SS.Job(name, time_interval)
   J.append(job)

total_cap = sum([v.capacity for v in V])
total_shift_hours = sum([j.length for j in J])

unassigned_jobs = []
J = sorted(J)

while len(J) > 0:
    job = J.pop(0)
    job_assigned = False
    V = sorted(V)

    for v in V:
        if v.can_take_job(job):
            v.add_job(job)
            job_assigned = True
            break

    if not job_assigned:
        unassigned_jobs.append(job)


# Output
if len(unassigned_jobs) == 0:
    min_v = sum([1 for x in V if x.is_used])
    print "Minimum number of volunteers needed: %d" % min_v
    print "Schedule produced..."
    SS.show_schedule(V)
else:
    print "There are unassigned jobs..."
    print unassigned_jobs



lower_bound_on_volunteers = float(total_cap)/total_shift_hours
print "Lower bound on volunteers: %s" % math.ceil(lower_bound_on_volunteers)

# Implementation of the BFD with randomization and balance.

import time
import random
import math
import copy
import sswing_scheduler as SS

def make_random_volunteers(num_of_volunteers, hour_range):
    V = []
    for x in xrange(1, num_of_volunteers+1):
        name = "Volunteer " + str(x)
        capacity = random.randint(hour_range[0], hour_range[1])
        volunteer = SS.Volunteer(name, capacity)
        available_start = random.randint(0,18)
        volunteer.add_job(SS.Job("UNAVAILABLE", (0, available_start)))
        volunteer.add_job(SS.Job("UNAVAILABLE", (available_start+capacity, 24)))
        V.append(volunteer)
    return V

def make_random_jobs(num_of_jobs):
    J = []
    for y in xrange(1, 31):
        name = "Job " + str(y)
        time_interval = SS.rand_time_interval(0, 21, random.randint(1,3))
        job = SS.Job(name, time_interval)
        J.append(job)
    return J


def assign_jobs(jobs, volunteers):
    unassigned_jobs = []
    J = sorted(jobs)
    V = volunteers

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

    return (V, unassigned_jobs)


volunteers = make_random_volunteers(60, (2,6))
jobs = make_random_jobs(30)

total_job_hours = sum([j.length for j in jobs])
avg_vol_capacity = sum([v.capacity for v in volunteers])/float(60)
rough_lower_bound = int(math.ceil(total_job_hours/avg_vol_capacity))

min_vol_list = []
best_vol_schedule = []
smallest = 60
print "Estimated Lower Bound: %s" % rough_lower_bound

print "Running on randomized volunteer sets..."
while(smallest > rough_lower_bound):
    j = jobs[:]
    V, uj = assign_jobs(j, volunteers)

    if len(uj) == 0:
        min_v = sum([1 for x in V if x.is_used])
        if min_v < smallest:
            smallest = min_v
            best_vol_schedule = copy.deepcopy(V)
            print "!!!!! NEW SMALLEST: %s !!!!!!!!!!!!!!!!!!!!!!" % smallest
            print "\n"
            SS.show_schedule(best_vol_schedule)
            print "\n\n"

    map(lambda x: x.clear_all(), volunteers)
    random.shuffle(volunteers)



# Now need to find an optimal way to balance the schedule

# OLD algo stuff...

# This approach probably won't work... Not sure how to generate undominated sets with jobs...
# simply generating subsets of 30 jobs blows the stack...
#
# Pseudo-code for Korf Algorithm:
#
# Compute BFD solution.
# Compute Lower-Bound with the wasted space method (*)
# If BFD Sol == Lower Bound then Stop -> return solution
# Else set BFD sol as current best complete solution
#      and start branch&bound search for strictly better solutions
#      pruning all partial solutions >= current best complete solution
#
# Branch and bound steps:
# Order elements in decreasing order
# For e in ordered_elements:
#   Find bin containing e
#   generate all undominated completions of bin (**)
#   if 0 or 1 undominated completion:
#     complete bin this way
#   else if more than 1 undominated completion:
#     order completions descending by sum
#     consider largest first, leave rest as branches
#     when complete solution is found and is better than current, update current best
#       -compute lower bound on partial solution (***)
#       - if worse than current best, prune partial solution
#
#
# (*) generating undominating terms:
# Generate subsets of feasible completion
# Test them for dominance

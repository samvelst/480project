import sys
import random
import copy
import Work as SS

import time

# Helper functions
def rand_time_interval(a_min, a_max, a_length):
    start = random.randint(a_min, a_max - a_length)
    return (start, start+a_length)


def show_schedule(volunteers):
    for v in volunteers:
        if v.is_used:
            v.print_schedule()


def make_random_volunteers(num_of_volunteers, capacity_range):
    V = []
    for x in xrange(1, num_of_volunteers+1):
        name = "Volunteer " + str(x)
        capacity = random.randint(capacity_range[0], capacity_range[1])
        volunteer = SS.Volunteer(name, capacity)
        available_start = random.randint(0, 24-capacity)
        volunteer.add_job(SS.JobShift("UNAVAILABLE", (0, available_start), -1))
        volunteer.add_job(SS.JobShift("UNAVAILABLE", (available_start+capacity, 24), -1))
        V.append(volunteer)
    return V


def make_random_jobs(num_of_jobs):
    J = []
    for x in xrange(1, num_of_jobs+1):
        id = x-1
        num_of_shifts = random.randint(1,6)
        start_time = random.randint(0, 21-num_of_shifts)
        for y in xrange(1, num_of_shifts+1):
            name = "Shift " + str(x) + "." + str(y)
            time_interval = (start_time+y-1, start_time+y)
            job = SS.JobShift(name, time_interval, id)
            J.append(job)
    return J


# BFD Algo: put largest item into bin with most stuff
def assign_jobs(jobs, volunteers):
    unassigned_jobs = []
    current_jobs = sorted(jobs)
    current_volunteers = volunteers

    while len(current_jobs) > 0:
        job = current_jobs.pop(0)
        current_volunteers = sorted(current_volunteers)
        job_assigned = False

        for volunteer in current_volunteers:
            if volunteer.can_take_job(job):
                volunteer.add_job(job)
                job_assigned = True
                break

        if not job_assigned:
            unassigned_jobs.append(job)

    return (current_volunteers, unassigned_jobs)


# Initialization of random volunteers and shifts
NUM_OF_JOBS = 15
NUM_OF_VOLUNTEERS = 60
volunteers = make_random_volunteers(NUM_OF_VOLUNTEERS, (2,6))
jobs = make_random_jobs(NUM_OF_JOBS)


# Compute the capacity based lower bound for volunteers
total_job_hours = sum([j.length for j in jobs])
avg_vol_capacity = sum([v.capacity for v in volunteers])/float(NUM_OF_VOLUNTEERS)
capacity_lower_bound = int((total_job_hours/avg_vol_capacity))


# Compute the overlapping intervals based lower bound for volunteers
overlap = dict.fromkeys(range(25), 0)
for j in jobs:
    for i in range(j.start, j.end):
        overlap[i] += 1

overlapping_lower_bound = max(overlap.values())

# Taking the larger of the two lower bounds to give us a realistic one
realistic_lower_bound = max(overlapping_lower_bound, capacity_lower_bound)

print "\n\n------------- Data ----------------------"
print "Total number of volunteers available: %s" % len(volunteers)
print "Total number of shifts that need assignment: %s" % len(jobs)
print "Total available hours of all volunteers: %s" % sum([v.capacity for v in volunteers])
print "Total hours of all jobs: %s" % sum([j.length for j in jobs])
print "Capacity lower bound %s" % capacity_lower_bound
print "Overlap lower bound %s (shifts at the same time)" % overlapping_lower_bound
print "Lower bound on the number of volunteers needed is roughly: %s" % realistic_lower_bound
print "-----------------------------------------"

print "\n\nAlgorithm will now run for 60 seconds."
print "Please terminate process whenever you see fit (Ctrl-c in terminal).\n"
print "Working...\n"

# Init tracking variables
current_best_schedule = []
current_best_weight = 0
min_volunteers_needed = NUM_OF_VOLUNTEERS


# Here we start randomizing the volunteer set to get different solutions
# we keep track of the smallest solution and store it
# we also keep track of the weight of each solution
# we will either get the current most optimal solution
# or an unfeasible, partial solution, with a list of anassignable jobs.
start = time.time()
end = 0
while (end <= 60):
    try:
        volunteers, unassigned_jobs = assign_jobs(jobs, volunteers)

        if len(unassigned_jobs) == 0:
            current_min = sum([1 for x in volunteers if x.is_used])
            total_weight = sum([v.get_weight() for v in volunteers])
            if current_min < min_volunteers_needed or \
              (current_min == min_volunteers_needed and total_weight > current_best_weight):
                min_volunteers_needed = current_min
                current_best_schedule = copy.deepcopy(volunteers)
                current_best_weight = total_weight
                t_length = time.time() - start
                print "New solution found with %s volunteers and weight %s in %s seconds" % (min_volunteers_needed, current_best_weight, t_length)
        else:
            print "Not able to find feasible solution"
            print "Unassigned jobs: %s" % unassigned_jobs
            print "Using %s volunteers" % sum([1 for x in volunteers if x.is_used])
            print "Current best schedule: "
            show_schedule(volunteers)
            break

        map(lambda x: x.clear_all(), volunteers)
        random.shuffle(volunteers)

        end = time.time() - start

    except KeyboardInterrupt:
        print "Terminating...\n\n"
        if len(unassigned_jobs) == 0:
            print "Volunteer count: %s" % min_volunteers_needed
            print "Job-type weight: %s" % current_best_weight
            print "Schedule produced: "
            show_schedule(current_best_schedule)
            print "\n"
        sys.exit()

print "Volunteer count: %s" % min_volunteers_needed
print "Job-type weight: %s" % current_best_weight
print "Schedule produced: "
show_schedule(current_best_schedule)
print "\n"

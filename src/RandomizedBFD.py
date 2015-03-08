import sys
import random
import copy
import Work as SS


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
        current_volunteers = sorted(current_volunteers) # This makes it a BFD instead of an FFD algo
        job_assigned = False

        for volunteer in current_volunteers:
            if volunteer.can_take_job(job):
                volunteer.add_job(job)
                job_assigned = True
                break

        if not job_assigned:
            unassigned_jobs.append(job)

    return (current_volunteers, unassigned_jobs)


NUM_OF_JOBS = 15
NUM_OF_VOLUNTEERS = 60
volunteers = make_random_volunteers(NUM_OF_VOLUNTEERS, (2,6))
jobs = make_random_jobs(NUM_OF_JOBS)

# estimating lower bound by dividing sum of shifts by average volunteer capacity
total_job_hours = sum([j.length for j in jobs])
avg_vol_capacity = sum([v.capacity for v in volunteers])/float(len(volunteers))
estimated_lower_bound = int((total_job_hours/avg_vol_capacity)+1)

current_best_schedule = []
min_volunteers_needed = 60

print "Estimated Lower Bound: %s..." % estimated_lower_bound

#CALCULATE EXACT LOWER BOUND FROM INTERVAL PARTITIONING VIEW
'''
min_volunteers = 0
open_volunteers = []
jobss = sorted(jobs)
for job in jobss:
    for volunteer in open_volunteers:
        if volunteer.can_take_job(job):
            volunteer.add_job(job)
            filled = True
    if not filled:
        min_volunteers += 1
        open_volunteers.append(SS.Volunteer("Bob", 24))
'''

# Here we start randomizing the volunteer set to get different solutions
# we keep track of the smallest solution and store it
# we can choose to terminate before the optimal sol is found
# we will either get the current most optimal solution
# or an unfeasible, partial solution, with a list of anassignable jobs.
while(min_volunteers_needed > estimated_lower_bound):
    try:
        volunteers, unassigned_jobs = assign_jobs(jobs, volunteers)

        if len(unassigned_jobs) == 0:
            current_min = sum([1 for x in volunteers if x.is_used])
            if current_min < min_volunteers_needed:
                min_volunteers_needed = current_min
                current_best_schedule = copy.deepcopy(volunteers)
                print "Current min volunteers needed: %s" % min_volunteers_needed

        map(lambda x: x.clear_all(), volunteers)
        random.shuffle(volunteers)

    except KeyboardInterrupt:
        print "Terminating...\n\n"
        if len(unassigned_jobs) == 0:
            print "Min # of volunteers found so far: %s" % min_volunteers_needed
            print "Schedule: "
            show_schedule(current_best_schedule)
            print "\n"
        else:
            print "Not able to find feasible solution"
            print "Unassigned jobs: %s" % unassigned_jobs
            print "Current best schedule: "
            show_schedule(volunteers)
        sys.exit()

print "Finished with optimal (%s) number of volunteers." % min_volunteers_needed
show_schedule(current_best_schedule)

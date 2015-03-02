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


def make_random_volunteers(num_of_volunteers, hour_range):
    V = []
    for x in xrange(1, num_of_volunteers+1):
        name = "Volunteer " + str(x)
        capacity = random.randint(hour_range[0], hour_range[1])
        volunteer = SS.Volunteer(name, capacity)
        available_start = random.randint(0,18)
        volunteer.add_job(SS.JobShift("UNAVAILABLE", (0, available_start)))
        volunteer.add_job(SS.JobShift("UNAVAILABLE", (available_start+capacity, 24)))
        V.append(volunteer)
    return V


def make_random_jobs(num_of_jobs):
    J = []
    for y in xrange(1, num_of_jobs+1):
        name = "Shift " + str(y)
        time_interval = rand_time_interval(0, 21, random.randint(1,3))
        job = SS.JobShift(name, time_interval)
        J.append(job)
    return J


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


volunteers = make_random_volunteers(60, (2,6))
jobs = make_random_jobs(30)

total_job_hours = sum([j.length for j in jobs])
avg_vol_capacity = sum([v.capacity for v in volunteers])/float(len(volunteers))
estimated_lower_bound = int((total_job_hours/avg_vol_capacity)+1)

current_best_schedule = []
min_volunteers_needed = 60

print "Estimated Lower Bound: %s..." % estimated_lower_bound
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

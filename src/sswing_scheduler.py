# Initial code for the scheduling algorith can go here.
# We can refactor as needed.

import random
import Queue
import sswing_scheduler as SS

# Object definitions
class Volunteer:
    def __init__(self, a_name="", a_capacity=4):
        self.name = a_name
        self.jobs = []
        self.capacity = a_capacity
        self.current_capacity = 0

    def __cmp__(self, other):
        return -cmp(self.current_capacity, other.current_capacity)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def add_job(self, a_job):
        self.jobs.append(a_job)
        self.current_capacity += a_job.length

    def can_take_job(self, a_job):
        if self.current_capacity + a_job.length > self.capacity:
            print "%s will put %s over capacity" % (a_job, self.name)
            return False
        elif len(self.jobs) == 0:
            return True
        else:
            for j in self.jobs:
                if a_job.conflicts_with(j):
                    return False
            return True

    def print_schedule(self):
        self.jobs = sorted(self.jobs, key=lambda x: x.start)
        print "Name: %s" % self.name
        for j in self.jobs:
            print "\t%s :: %s - %s" % (j.name, j.start, j.end)


class Job:
    def __init__(self, a_name, a_time_interval):
        self.name = a_name
        self.start, self.end  = a_time_interval
        self.length = self.end - self.start

    def __cmp__(self, other):
        return -cmp(self.length, other.length)

    def __repr__(self):
        return "%s :: %s - %s" % (self.name, self.start, self.end)

    def conflicts_with(self, another_job):
        if another_job.start == self.start or another_job.end == self.end:
            return True
        elif (self.start < another_job.start < self.end) or (self.start < another_job.end < self.end):
            return True
        else:
            return False


# test code

def rand_time_interval(a_min, a_max):
    a = random.randint(a_min, a_max-1)
    # b = random.randint(a+1, a_max)
    return (a, a+1)

def show_schedule(volunteers):
    for v in volunteers:
        v.print_schedule()

V = [SS.Volunteer(a_name="Volunteer " + str(z)) for z in xrange(1,11)]
J = sorted([SS.Job("Job "+str(z), rand_time_interval(0,4)) for z in xrange(1,21)])


# algorithm (greedy)
db_count = 1
while len(J) > 0:
    print "Current loop %s" % db_count
    j = J.pop(0)
    print "Assigning: %s" % j
    curr_job_assigned = False
    V = sorted(V)

    for v in V:
        print "Considering..."
        v.print_schedule()
        if v.can_take_job(j):
            v.add_job(j)
            print "Assigning job to: %s" % v
            curr_job_assigned = True
            break

    if not curr_job_assigned:
        print "Error: could not find assignment for %s" % j
        break

    db_count += 1

show_schedule(V)

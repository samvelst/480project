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
            return False
        elif len(self.jobs) == 0:
            return True
        else:
            for j in self.jobs:
                if j.start < a_job.start < j.end or j.start < a_job.end < j.end:
                    return False
                else:
                    return True

class Job:
    def __init__(self, a_name, a_time_interval):
        self.name = a_name
        self.start, self.end  = a_time_interval
        self.length = self.end - self.start

    def __cmp__(self, other):
        return -cmp(self.length, other.length)

    def __repr__(self):
        return "%s :: %s - %s" % (self.name, self.start, self.end)


# test code

def rand_time_interval(a_min, a_max):
    a = random.randint(a_min, a_max-1)
    b = random.randint(a+1, a_max)
    return (a, b)

def show_schedule(volunteers):
    for v in volunteers:
        if v.current_capacity != 0:
            print "Name: %s" % v.name
            for j in v.jobs:
                print "\t%s :: %s - %s" % (j.name, j.start, j.end)

V = [SS.Volunteer(a_name="Volunteer " + str(z)) for z in xrange(1,11)]
J = sorted([SS.Job("Job "+str(z), rand_time_interval(0,4)) for z in xrange(1,21)])


# algorithm (greedy)

for j in J:
    # do magic here

import random

class Volunteer:
    def __init__(self, a_name="", a_capacity=4):
        self.name = a_name
        self.jobs = []
        self.capacity = a_capacity
        self.current_capacity = 0
        self.is_used = False

    def __cmp__(self, other):
        return -cmp(self.current_capacity, other.current_capacity)

    def __repr__(self):
        return self.name

    def add_job(self, a_job):
        self.jobs.append(a_job)
        if not a_job.name.startswith("UNAVAILABLE"):
            self.current_capacity += a_job.length
            self.is_used = True

    def can_take_job(self, a_job):
        for j in self.jobs:
            if a_job.conflicts_with(j):
                return False

        if self.current_capacity + a_job.length > self.capacity:
            return False

        return True

    def print_schedule(self):
        self.jobs = sorted(self.jobs, key=lambda x: x.start)
        print "Name: %s :: Hours %s" % (self.name, self.capacity)
        for j in self.jobs:
            print "\t%s :: %s - %s" % (j.name, j.start, j.end)

    def clear_all(self):
        self.jobs = filter(lambda x: x.name.startswith('UNAVAILABLE'), self.jobs)
        self.current_capacity = 0
        self.is_used = False


class Job:
    def __init__(self, a_name, a_time_interval):
        self.name = a_name
        self.start, self.end  = a_time_interval
        self.interval = set(range(self.start, self.end+1))
        self.length = self.end - self.start

    def __cmp__(self, other):
        return -cmp(self.length, other.length)

    def __repr__(self):
        return "%s :: %s - %s" % (self.name, self.start, self.end)

    def conflicts_with(self, another_job):
        return len(self.interval & another_job.interval) > 1


# Helper Functions
def rand_time_interval(a_min, a_max, a_length):
    a = random.randint(a_min, a_max - a_length)
    return (a, a+a_length)

def show_schedule(volunteers):
    for v in volunteers:
        if v.is_used:
            v.print_schedule()

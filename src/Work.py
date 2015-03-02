#!/usr/bin/python
#
# Work objects
#


class Volunteer:
    """
    Represents a single volunteer
    String name - Name of the volunteer
    Int capacity - How many hours this volunteer has available
    Int current_capacity - How many available hours the volunteer current has
    [Job] jobs - Current list of jobs assigned to volunteer
    Boolean is_used - True if the volunteer's job list is not empty
    [Int] job_id_count - keeps count of how many shifts of each job ID a volunteer has
    """
    def __init__(self, a_name="", a_capacity=4):
        self.name = a_name
        self.capacity = a_capacity
        self.current_capacity = 0
        self.jobs = []
        self.is_used = False
        self.job_id_count = [0 for _ in xrange(15)] # this is a bad thing to do :-(

    def __cmp__(self, other):
        return -cmp(self.current_capacity, other.current_capacity)

    def __repr__(self):
        return self.name

    def add_job(self, a_job):
        self.jobs.append(a_job)
        if not a_job.name.startswith("UNAVAILABLE"):
            self.current_capacity += a_job.length
            self.job_id_count[a_job.id] += 1
            self.is_used = True

    def can_take_job(self, a_job):
        for current_job in self.jobs:
            if a_job.conflicts_with(current_job):
                return False

        if (self.current_capacity + a_job.length) > self.capacity:
            return False

        return True

    def get_weight(self):
        return sum([x**2 for x in self.job_id_count])

    def print_schedule(self):
        self.jobs = sorted(self.jobs, key=lambda x: x.start)
        print "Name: %s :: Hours %s" % (self.name, self.capacity)
        for j in self.jobs:
            print "\t%s :: %s - %s" % (j.name, j.start, j.end)

    def clear_all(self):
        self.jobs = filter(lambda x: x.name.startswith('UNAVAILABLE'), self.jobs)
        self.current_capacity = 0
        self.is_used = False


class JobShift:
    """
    Represents a single shift
    String name - name of the shift
    Int start - shift's start time
    Int end - shift's end time
    [Int] interval - all hours covered by this shift
    Int length - total number of hours for this shift
    Int id - represents this shifts job ID
    """
    def __init__(self, a_name, a_time_interval, an_id):
        self.name = a_name
        self.start, self.end  = a_time_interval
        self.interval = set(range(self.start, self.end+1))
        self.length = self.end - self.start
        self.id = an_id

    def __cmp__(self, other):
        return -cmp(self.length, other.length)

    def __repr__(self):
        return "%s :: %s - %s" % (self.name, self.start, self.end)

    def conflicts_with(self, another_job):
        return len(self.interval & another_job.interval) > 1

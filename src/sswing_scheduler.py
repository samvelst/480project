# Initial code for the scheduling algorith can go here.
# We can refactor as needed.


class Volunteer:
    def __init__(self, a_name, a_skillset=[]):
        """Represents a single volunteer that will have a set of jobs
            String a_name = name of the volunteer
            [String] a_skillset - skills that volunteer posesses. 
        """
        self.name = a_name
        self.skills = a_skillset
        self.jobs = []

    def add_job(self, a_job):
        #check if job conflicts with any other job in the set
        if not self.conflicts(a_job):
            self.jobs.append(a_job)

    def conflicts(self, a_job):
        # need some clever way to quickly calculate conflicting jobs
        return False 



class Job:
    def __init__(self, a_name, a_start_time, an_end_time, a_skillset, a_description=""):
        """Represents a single job that requires a single volunteer
            String a_name - Name of job
            String a_description - optional description of job
            Int a_start_time - [0000 - 2359] using standard military time
            Int an_end_time - [0000 - 2359] using standard military time
            [String] a_skillset - the list of qualifications required for this job
        """
        self.name = a_name
        self.start_time = a_start_time
        self.end_time = an_end_time
        self.skills = a_skillset
        self.description = a_description



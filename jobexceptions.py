class JobException(Exception):
    def __init__(self, job, msg=None):
        if msg is None:
            msg = f"An error with job '{job.name}' occured."
        super().__init__(msg)
        self.job = job


class ValueNotProvided(JobException):
    """Comparator other than 'ne' provided, but no value set"""
    def __init__(self, job):
        super().__init__(job,
             "Comparator other than 'ne' provided, but no value set" +
             f"(job: {job.name})")
        self.job = job

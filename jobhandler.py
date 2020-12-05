from job import Job
from jobexecutor import JobExecutor
from requests_html import HTMLSession
import yaml


class JobHandler():

    def __init__(self, *args):
        self.queue = []
        self.queue.extend(args)

    def __repr__(self):
        names = [str(i) for i in self.queue]
        return f"Queue length: {len(self.queue)}; Jobs: " +\
            f"{', '.join(names)}"

    @classmethod
    def fromYaml(cls, filename):
        jobs = []
        with open(filename, 'r') as f:
            for job in yaml.load_all(f, Loader=yaml.FullLoader):
                jobs.append(Job.fromDict(job))
        return cls(*jobs)

    def add(self, job):
        self.queue.append(job)

    def clear(self):
        self.queue.clear()

    def run(self):
        session = HTMLSession()
        je = JobExecutor(session)
        for job in self.queue:
            try:
#                job.printConfig()
                completed = je.runJob(job)
            except Exception as e:
                print(e)
                continue
            if completed:
                self.notify(job)
        session.close()
        self.queue.clear()

    def notify(self, job):
        print(f"'{job.name}' was good.")
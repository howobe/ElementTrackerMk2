from job import Job
from jobexecutor import JobExecutor
from requests_html import HTMLSession
import yaml
import logging
from notify import SlackNotification
import os
jhLog = logging.getLogger("jobhand")


class JobHandler():

    def __init__(self, *args):
        jhLog.info("Creating job queue")
        self.queue = []
        self.add(args)

    def __repr__(self):
        names = [str(i) for i in self.queue]
        return f"Queue length: {len(self.queue)}; Jobs: " +\
            f"{', '.join(names)}"

    @classmethod
    def fromYaml(cls, filename):
        jobs = []
        jhLog.info(f"Reading jobs from '{filename}'")
        with open(filename, 'r') as f:
            for job in yaml.load_all(f, Loader=yaml.FullLoader):
                jobs.append(Job.fromDict(job))
        return cls(*jobs)

    def add(self, *args):
        names = [i.name for i in args]
        s = ""
        if len(names) > 1:
            s = "s"
        jhLog.info(f"Adding {len(names)} job{s}: {', '.join(names)}")
        self.queue.extend(args)

    def clear(self):
        self.queue.clear()

    def run(self):
        jhLog.info("Starting jobs...")
        session = HTMLSession()
        jhLog.info("Session started...")
        je = JobExecutor(session)
        for job in self.queue:
            jhLog.debug(job.getConfig)
            try:
                completed = je.runJob(job)
            except Exception as e:
                print(e)
                continue
            if completed:
                self.notify(job)
        jhLog.info("Closing session...")
        session.close()
        self.queue.clear()

    def notify(self, job):
        sl = SlackNotification(os.environ["SLACK_API_TOKEN"])
        sl.setBody(f"Job '{job.name} detected a change! Go to {job.url}!")
        sl.send()

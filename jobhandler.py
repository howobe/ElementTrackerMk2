from job import Job, NOTIFICATION_LIMIT
from jobexecutor import JobExecutor
from requests_html import HTMLSession
import yaml
import logging
from notify import SlackNotification
import os
jhLog = logging.getLogger("jobhand")


class JobHandler():

    def __init__(self, filename=None, *args):
        jhLog.info("Creating job queue")
        self.filename = filename
        self.queue = []
        self.add(*args)

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
        return cls(filename, *jobs)

    @staticmethod
    def editYaml(jobName, key, value, filename):
        contents = []
        with open(filename, 'r') as f:
            for job in yaml.load_all(f, Loader=yaml.FullLoader):
                if job["name"] == jobName:
                    job[key] = value
                contents.append(job)
        with open(filename, 'w') as f:
            yaml.safe_dump_all(contents, f)

    def add(self, *args):
        names = [str(i) for i in args]
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
            jhLog.debug(str(job.getConfig()))
            try:
                completed = je.runJob(job)
            except Exception as e:
                jhLog.exception(e)
                continue
            if completed and job.count < NOTIFICATION_LIMIT:
                self.notify(job)
                job.increment()
                self.editYaml(job.name, "count", job.count, self.filename)
        jhLog.info("Closing session...")
        session.close()
        self.queue.clear()

    def notify(self, job):
        sl = SlackNotification(os.environ["SLACK_API_TOKEN"])
        sl.setBody(f"Job '{job.name}' detected a change: {job.value} => {job.newValue}!\nGo to {job.url}")
        sl.send()

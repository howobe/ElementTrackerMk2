import logging
jeLog = logging.getLogger('jobexec')

class JobExecutor():

    def __init__(self, session):
        self.session = session
        jeLog.info("JobExecutor handed session...")

    def prepare(self):
        pass

    def runJob(self, job):
        resp = self.get(job)
        roi = self.find(resp, job)
        return self.checkCondition(roi, job)

    def get(self, job):
        return self.session.get(job.url)
        jeLog.debug("Making get request to " + job.url)

    def find(self, response, job):
        if job.render:
            jeLog.debug("Preparing to render js")
            response.html.render(timeout=20)
        roi = response.html.xpath(job.element)

        if isinstance(roi, list):
            if len(roi) == 0:
                jeLog.warning("Element no longer exists")
                roi = True
            else:
                roi = roi[0]
                jeLog.info("Element found")
        return roi

    def checkCondition(self, roi, job):
        if isinstance(roi, bool):
            return roi
        if job.key is None:
            jeLog.debug("Extracting text")
            objoi = roi.text
        else:
            attrdict = roi.attrs
            jeLog.debug("Gathering attribute")
            objoi = attrdict[job.key]
        jeLog.info("Object of interest value: " + objoi)
        if getattr(objoi, job.comparator)(job.value):
            return True
        return False

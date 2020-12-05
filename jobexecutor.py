class JobExecutor():

    def __init__(self, session):
        self.session = session

    def prepare(self):
        pass

    def runJob(self, job):
        resp = self.get(job)
        roi = self.find(resp, job)
        return self.checkCondition(roi, job)

    def get(self, job):
        return self.session.get(job.url)

    def find(self, response, job):
        if job.render:
            response.html.render(timeout=20)
        roi = response.html.xpath(job.element)

        if isinstance(roi, list):
            if len(roi) == 0:
                roi = True
            else:
                roi = roi[0]
        return roi

    def checkCondition(self, roi, job):
        if isinstance(roi, bool):
            return roi
        if job.key is None:
            objoi = roi.text
        else:
            attrdict = roi.attrs
            objoi = attrdict[job.key]
        print(objoi)
        if getattr(objoi, job.comparator)(job.value):
            return True
        return False

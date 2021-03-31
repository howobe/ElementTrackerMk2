from jobexceptions import JobException, ValueNotProvided

NOTIFICATION_LIMIT = 3

class Job():

    newValue=None

    def __init__(self, url=None, element=None, key=None, value=None,
                 comparator="ne", forceRender=False, name="Unnamed job",
                 count=0):
        self.name = name
        self.count = count
        self.setUrl(url)
        self.setElementPosition(element)
        self.setCondition(key, value, comparator)
        self.setForceRender(forceRender)

    @classmethod
    def fromDict(cls, dictionary):
        return cls(**dictionary)

    def __repr__(self):
        return self.name

    def setUrl(self, url):
        self.url = url

    def setElementPosition(self, element):
        self.element = element

    def setCondition(self, key=None, value=None, comparator="ne"):
        self.comparator = "__" + comparator + "__"
        self.key = key
        self.value = value
#        if self.comparator != "__ne__" and value is None:
#            raise ValueNotProvided(self)

    def checkState(self):
        if not (self.url is None and self.element is None and self.value is
             not None):
            self.state = "gcv"
        elif not(self.url is None and self.element is None and self.value is
               None):
            self.state = "ready"

    def setForceRender(self, boolean):
        self.render = boolean

    def increment(self):
        self.count += 1

    def printConfig(self):
        print(self.name)
        print(self.element)
        print(self.url)
        print(self.key)
        print(self.value)
        print(self.comparator)
        print(self.render)

    def getConfig(self):
        deets = {}
        deets["name"] = self.name
        deets["url"] = self.url
        deets["element"] = self.element
        deets["comparator"] = self.comparator
        deets["key"] = self.key
        deets["value"] = self.value
        deets["forceRender"] = self.render
        return deets

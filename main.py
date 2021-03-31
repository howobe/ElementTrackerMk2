from job import Job
from jobhandler import JobHandler
import logging
from logging import config as logconfig
import yaml


with open('log.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logconfig.dictConfig(config)

jh = JobHandler.fromYaml("jobs2.yaml")
jh.run()

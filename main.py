from job import Job
from jobhandler import JobHandler
import logging
from logging import config as logconfig
import yaml


with open('log.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logconfig.dictConfig(config)

#a = Job(url="https://www.scan.co.uk/products/amd-ryzen-5-5600x-am4-zen-3-6-core-12-thread-37ghz-46ghz-turbo-35mb-cache-pcie-40-65w-cpu",
#        element="/html/body/div[2]/div[3]/div[2]/div[1]/div[2]/div[1]/div/div/div[1]/span[1]",
#        key="content", value="99999.99", name="scan")
#
#b = Job(url="https://www.box.co.uk/100-100000031BOX-AMD-Ryzen-5-3600-Gen3-(Socket-AM4)_2606581.html",
#        element="/html/body/form/div[1]/div[5]/div/div[2]/div[2]/ajaxsection/div[2]/div",
#        key="title", value="Buy now", name="box")
#
#c = Job(url="https://www.currys.co.uk/gbuk/computing-accessories/components-upgrades/processors/amd-ryzen-5-5600x-processor-10216691-pdt.html#rr_placement_1",
#        element="/html/body/div[2]/div[2]/div[3]/div[2]/section/div[4]/div[4]/div/ul/li[1]",
#        value="Sorry this item is out of stock", forceRender=True, name="currys")

jh = JobHandler.fromYaml("jobs.yaml")
jh.run()

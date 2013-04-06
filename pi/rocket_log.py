__author__ = 'andriod'

import logging
import uuid


logging.basicConfig(filename="rocket_"+uuid.uuid4().get_hex()+".log",level=logging.INFO,
                    format="%(created)f %(filename)s:%(lineno)d: %(message)s")
log = logging.getLogger(__name__)

while(True):
    log.info("System Operating")
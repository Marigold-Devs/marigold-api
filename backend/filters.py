""" """
import json
import logging


class RequestDataFilter(logging.Filter):
    """ """

    def filter(self, record):
        """ """
        record.request_data = None

        if record.request.POST:
            record.request_data = json.dumps(record.request.POST)

        return True

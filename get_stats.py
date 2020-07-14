#!/usr/bin/env python3

import logging
import argparse
from datetime import datetime, timedelta


class Statistics(object):
    def __init__(self):
        self._domain_list = []
        self._status_codes = None

    @property
    def domain_list(self):
        """I'm the 'x' property."""
        return self._domain_list

    @property
    def status_codes(self):
        """I'm the 'x' property."""
        return self._status_codes

    @domain_list.setter
    def domain_list(self, value):
        print("setter of x called")
        self._domain_list = value

    @status_codes.setter
    def status_codes(self, value):
        self._status_codes = value

    @domain_list.deleter
    def domain_list(self):
        del self._domain_list

    @status_codes.deleter
    def status_codes(self):
        del self._status_codes


def configure_logger():
    """
    Configure and setup baseline python logger, format is date - time - level - message

    :return:
    Logger with format and baseline configuration
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    return logging.getLogger(__name__)


def main():
    # Initialize logger
    logger = configure_logger()
    parser = argparse.ArgumentParser(description='Vimeo log statistic parser!')

    parser.add_argument('--start_date',
                        default=datetime.now() - timedelta(hours=1),
                        help='Start date to search from, defaults to 1 hour before now')
    parser.add_argument('--end_date',
                        default=datetime.now(),
                        help='End date to search up until, defaults to now')

    args = parser.parse_args()
    current_stats = Statistics()

    # logger.info(args)
    # This will pass with glory
    # c = Statistics()
    # c.domain_list = 'foo'  # setter called
    # foo = c.domain_list  # getter called
    # del c.domain_list  # deleter called

    # Reads file line by line, avoids loading into memory as file could be >=10Gb
    with open("log_sample.txt") as infile:
        for line in infile:
            parsed_message = line.split('|')

            # Get iso timestamp from position 0
            date = datetime.fromtimestamp(float(parsed_message[0]))

            # Get domain from position 2
            domain = parsed_message[2]

            # Get http status code from position 4
            status = parsed_message[4]

            logger.info("{0} - {1} - {2}".format(date, domain, status))


if __name__ == '__main__':
    main()

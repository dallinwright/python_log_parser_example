#!/usr/bin/env python3

import logging
import argparse
import sys
from datetime import datetime, timedelta


class Statistics(object):
    def __init__(self):
        self._domains = {}

    @property
    def domains(self):
        return self._domains

    @domains.setter
    def domains(self, value):
        self._domains = value

    @domains.deleter
    def domains(self):
        del self._domains

    def add_domain(self, domain):
        self._domains[domain] = {
            'total': 0,
            'error': 0
        }


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
    # Initialize parser
    parser = argparse.ArgumentParser(description='Vimeo log statistic parser!')

    parser.add_argument('--start_date',
                        default=datetime.now() - timedelta(hours=1),
                        help='Start date to search from, defaults to 1 hour before now')
    parser.add_argument('--end_date',
                        default=datetime.now(),
                        help='End date to search up until, defaults to now')

    args = parser.parse_args()
    current_stats = Statistics()

    # Reads file line by line, avoids loading into memory as file could be >=10Gb
    with open("log_sample.txt") as infile:
        for line in infile:
            parsed_message = line.split('|')

            try:
                # Get iso timestamp from position 0
                date = datetime.fromtimestamp(float(parsed_message[0]))
                # Get domain from position 2, strip all whitespace
                domain = parsed_message[2].replace(" ", "")
                # Get http status code from position 4, parse string as int
                status = int(parsed_message[4])

                # If domain not in current dict, create stat entry
                if domain not in current_stats.domains:
                    logger.info('Encountered new domain - {0}'.format(domain))
                    current_stats.add_domain(domain)

                # Increment 500 count for domain
                if status >= 500:
                    error_count = current_stats.domains[domain].get('error')

            except IndexError as e:
                logger.error("Invalid log format, aborting!")
                sys.exit(1)

        logger.info(current_stats.domains)


if __name__ == '__main__':
    main()

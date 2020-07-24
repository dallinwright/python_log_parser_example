#!/usr/bin/env python3

import logging
import argparse
import sys
from datetime import datetime, timedelta

# Global logger config
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


class Statistics(object):
    def __init__(self, start, end):
        """
        Create a stat tracker class
        :param start: datetime from which to start looking
        :param end: datetime to look until
        """
        self._domains = {}
        self._start = datetime.fromtimestamp(float(start))
        self._end = datetime.fromtimestamp(float(end))

    @property
    def domains(self):
        return self._domains

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @domains.setter
    def domains(self, value):
        self._domains = value

    @domains.deleter
    def domains(self):
        del self._domains

    @start.setter
    def start(self, value):
        self._start = value

    @end.setter
    def end(self, value):
        self._end = value

    def add_domain(self, domain):
        """
        Creates a entry in the dict with the baseline stats we want to track
        :param domain: Name of domain to start tracking
        :return: None
        """
        self._domains[domain] = {
            'total': 0,
            'error': 0
        }

    def add_error(self, domain):
        """
        Helper function to increment error count for domain
        :param domain: Name of domain to increment errors for
        :return: None
        """
        try:
            self._domains[domain]['error'] = self._domains.get(domain, {}).get('error') + 1
        except TypeError:
            logger.error("Error updating {0} error count".format(domain))

    def add_count(self, domain):
        """
        Helper function to increment error count for domain
        :param domain: Name of domain to increment total count for
        :return: None
        """
        try:
            self._domains[domain]['total'] = self._domains.get(domain, {}).get('total') + 1
        except TypeError:
            logger.error("Error updating {0} total count".format(domain))

    def display_summary(self):
        """
        Display summary of all stats
        :return: None
        """
        print('Between time {0} and time {1}:'.format(self._start, self._end))

        for domain in self._domains:
            # Fail safe for division by 0
            if self._domains.get(domain, {}).get('total') != 0:
                # Calculate percent 5xx errors
                percent = self._domains[domain]['error'] / self._domains[domain]['total'] * 100
                # Round percent to 2 decimals, pretty it up by forcing two decimal points
                pretty_percent = "{:.2f}".format(round(percent, 2))
                # Print summary for domain
                print("{0} returned {1}% 5xx errors".format(domain, pretty_percent))


def main():
    """
    Main script logic for vimeo stat tracker
    :return: None
    """
    
    # Initialize parser
    parser = argparse.ArgumentParser(description='Vimeo log statistic parser!')

    # Datetime now, to be absolutely exact. Two calculation for date in different spots in here will be different.
    now = datetime.now()

    parser.add_argument('--start',
                        default=(now - timedelta(hours=1)).timestamp(),
                        help='Start date to search from, defaults to 1 hour before now')
    parser.add_argument('--end',
                        default=now.timestamp(),
                        help='End date to search up until, defaults to now')
    parser.add_argument('filename',
                        default=now.timestamp(),
                        help='End date to search up until, defaults to now')

    args = parser.parse_args()

    # Create stat tracker
    current_stats = Statistics(args.start, args.end)

    logger.info('Searching from time {0}'.format(args.start))
    logger.info('Searching from time {0}'.format(args.end))

    # Reads file line by line, avoids loading into memory as file could be >=10Gb
    with open(args.filename) as infile:
        for line in infile:
            # Split log file on char |, this is not robust
            parsed_message = line.split('|')

            try:
                # Get iso timestamp from position 0
                date = datetime.fromtimestamp(float(parsed_message[0]))

                if current_stats.start <= date < current_stats.end:
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
                        current_stats.add_error(domain)

                    # Increment count for domain
                    current_stats.add_count(domain)

            except IndexError:
                logger.critical("Invalid log format, aborting!")
                sys.exit(1)

    logger.info('Vimeo statistic aggregator complete.')

    current_stats.display_summary()


if __name__ == '__main__':
    """
    Main function, allows python script to be called by name
    """
    main()

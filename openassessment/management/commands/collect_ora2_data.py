"""
Command to retrieve all ORA2 data for a course in a .csv.


This command differs from upload_oa_data in that it places all the data into one file.

Generates the same format as the instructor dashboard downloads.
"""
from __future__ import absolute_import

import os

import six

from django.core.management.base import BaseCommand, CommandError

from openassessment.data import OraAggregateData
from openassessment.management.commands import write_csv


class Command(BaseCommand):
    """
    Query aggregated open assessment data, write to .csv
    """

    help = ("Usage: collect_ora2_data <course_id> --output-dir=<output_dir>")

    def add_arguments(self, parser):
        parser.add_argument('course_id', nargs='+', type=six.text_type)
        parser.add_argument(
            '-o',
            '--output-dir',
            action='store',
            dest='output_dir',
            default=None,
            help="Write output to a directory rather than stdout"
        )
        parser.add_argument(
            '-n',
            '--file-name',
            action='store',
            dest='file_name',
            default=None,
            help="Write CSV file to the given name"
        )

    def handle(self, *args, **options):
        """
        Run the command.
        """
        if not options.get('course_id'):
            raise CommandError("One or more Course IDs must be specified to fetch data")

        course_ids = options['course_id']

        for course_id in course_ids:
            if options['file_name']:
                file_name = options['file_name']
            else:
                file_name = ("%s-ora2.csv" % course_id).replace("/", "-")

            if options['output_dir']:
                csv_file = open(os.path.join(options['output_dir'], file_name), 'w')
            else:
                csv_file = self.stdout

            header, rows = OraAggregateData.collect_ora2_data(course_id)
            write_csv(csv_file, header, rows)

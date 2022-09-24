import os

from django.core.management.base import BaseCommand
from django.apps import apps
from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent


class Command(BaseCommand):
    help = "Creating Location counties names"

    def add_arguments(self, parser):
        parser.add_argument('--app_name', type=str, help='application that is involved in saving')

    def handle(self, *args, **options):
        model = apps.get_model(options['app_name'], 'CountyModel')
        file_path = os.path.join(BASE_DIR, 'counties.csv')
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            header = next(reader)
            for row in reader:
                county, _ = model.objects.get_or_create(Name=" ".join(row[1].split()))
                # county.save()

        print('** All Counties succesfully setup **')

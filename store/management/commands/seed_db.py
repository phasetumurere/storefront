from pathlib import Path
from django.core.management.base import BaseCommand
import os

from django.db import connection

class Command(BaseCommand):
    help = 'Populate the database with Collections and Products'
    
    def handle(self, *args, **options):
        print('Populating database..')
        current_dir = os.path.dirname(__file__)
        # print(current_dir)
        file_path = os.path.join(current_dir, 'seed.sql')
        sql = Path(file_path).read_text()
        with connection.cursor() as cursor:
            cursor.execute(sql)
    
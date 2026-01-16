import csv
from django.core.management.base import BaseCommand
from history.models import History


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name',
            type=str,
            help='Nome do arquivo CSV com o historico',
        )


    def handle(self, *args, **options):
        file_name = options['file_name']

        with open(file_name, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                entity = row['entity']
                record = row['record']
                new_tax = row['new_tax']

                self.stdout.write(self.style.NOTICE(entity))

                History.objects.create(
                    entity=entity,
                    record=record,
                    new_tax=new_tax,
                )

        self.stdout.write(self.style.SUCCESS('HISTORICOS IMPORTADOS COM SUCESSO!'))

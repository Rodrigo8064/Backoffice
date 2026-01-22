import csv
from django.core.management.base import BaseCommand
from category.models import Category

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name',
            type=str,
            help='Nome do arquivo CSV com os tipos de produto'
        )

    def handle(self, *args, **options):
        file_name = options['file_name']
        self.stdout.write(self.style.SUCCESS(f'Iniciando importação de {file_name}...'))

        created_count = 0
        updated_count = 0

        with open(file_name, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                name_subcategory = row['subcategoria']
                url = row['url']
                name_father = row['parent']

                parent_object = None

                if name_father:
                    try:
                        parent_object = Category.objects.get(name=name_father)
                    except Category.DoesNotExist:
                        self.stdout.write(self.style.ERROR(
                            f"Pai '{name_father}' para o produto '{name_subcategory}' não encontrado. "
                            f"Este produto será criado como um item raiz."
                        ))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Erro ao buscar pai '{name_father}': {e}"))
                        continue

                subcategory, created = Category.objects.get_or_create(
                    name=name_subcategory,
                    url=url,
                    defaults={'parent': parent_object},
                )

                if not created:

                    if subcategory.parent != parent_object:
                        subcategory.parent = parent_object
                        subcategory.save()
                        updated_count += 1
                else:
                    created_count += 1

        self.stdout.write(self.style.WARNING("Importação concluída. Reconstruindo a árvore MPTT..."))
        Category.objects.rebuild()

        self.stdout.write(self.style.SUCCESS(
            f'Árvore reconstruída! {created_count} produtos criados, {updated_count} atualizados.'
        ))

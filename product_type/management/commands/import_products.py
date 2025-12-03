import csv
from django.core.management.base import BaseCommand
from product_type.models import ProductType

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
                nome_produto = row['product']
                nome_pai = row['parent']

                parent_object = None

                if nome_pai:
                    try:
                        parent_object = ProductType.objects.get(nome=nome_pai)
                    except ProductType.DoesNotExist:
                        self.stdout.write(self.style.ERROR(
                            f"Pai '{nome_pai}' para o produto '{nome_produto}' não encontrado. "
                            f"Este produto será criado como um item raiz."
                        ))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Erro ao buscar pai '{nome_pai}': {e}"))
                        continue

                product, created = ProductType.objects.get_or_create(
                    nome=nome_produto,
                    defaults={'parent': parent_object}
                )

                if not created:

                    if product.parent != parent_object:
                        product.parent = parent_object
                        product.save()
                        updated_count += 1
                else:
                    created_count += 1

        self.stdout.write(self.style.WARNING("Importação concluída. Reconstruindo a árvore MPTT..."))
        ProductType.objects.rebuild()

        self.stdout.write(self.style.SUCCESS(
            f'Árvore reconstruída! {created_count} produtos criados, {updated_count} atualizados.'
        ))

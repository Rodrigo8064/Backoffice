"""
Management command para importar atributos de um arquivo CSV.

Uso:
    python manage.py import_attributes caminho/para/arquivo.csv
    python manage.py import_attributes caminho/para/arquivo.csv --user admin
    python manage.py import_attributes caminho/para/arquivo.csv --dry-run

Formato esperado do CSV:
    name,expected_value,sources,families
    cor,Azul,Shopify|Magalu,Casa e Jardim|Vestuário
    tamanho,G,Shopify,Vestuário
    voltagem,,Magalu,Eletrodomésticos

Regras:
    - Separador de colunas: vírgula (,)
    - Separador de múltiplos valores em sources e families: pipe (|)
    - expected_value é opcional — deixe a célula vazia
    - sources e families devem existir previamente no banco
    - O comando pode ser executado múltiplas vezes sem duplicar dados
"""
import csv
import os
import typing

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from attributes.models import Attribute
from category.models import Family, Source

User = get_user_model()


class Command(BaseCommand):
    help = 'Importa atributos de um arquivo CSV para o banco de dados.'

    @typing.override
    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Caminho para o arquivo CSV a ser importado.',
        )
        parser.add_argument(
            '--user',
            type=str,
            default=None,
            help='Username do usuário que será vinculado aos atributos criados.'
                 'Se não informado, usa o primeiro superusuário encontrado.',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            default=False,
            help='Simula a importação sem salvar nada no banco.'
                 'Útil para validar o CSV antes de importar de verdade.',
        )
        parser.add_argument(
            '--delimiter',
            type=str,
            default=',',
            help='Delimitador de colunas do CSV. Padrão: vírgula (,).',
        )
        parser.add_argument(
            '--separator',
            type=str,
            default='|',
            help='Separador de múltiplos valores. Padrão: pipe (|).',
        )

    def handle(self, *args, **options):
        csv_path = options['csv_file']
        username = options['user']
        dry_run = options['dry_run']
        delimiter = options['delimiter']
        separator = options['separator']

        # ── Validar arquivo ──────────────────────────────────────────────
        if not os.path.exists(csv_path):
            raise CommandError(f'Arquivo não encontrado: {csv_path}')

        if not csv_path.endswith('.csv'):
            raise CommandError('O arquivo deve ter extensão .csv')

        # ── Resolver usuário ─────────────────────────────────────────────
        user = self._get_user(username)
        self.stdout.write(
            f'Usuário vinculado: {self.style.SUCCESS(user.username)}'
        )

        if dry_run:
            self.stdout.write(self.style.WARNING(
                '\n⚠  MODO DRY-RUN — nenhum dado será salvo no banco.\n'
            ))

        # ── Pré-carregar fontes e famílias do banco ──────────────────────
        sources_db = {s.name.lower(): s for s in Source.objects.filter(is_active=True)}
        families_db = {f.name.lower(): f for f in Family.objects.filter(
            is_active=True
        )}

        if not sources_db:
            raise CommandError(
                'Nenhuma fonte ativa encontrada no banco. '
                'Cadastre as fontes via admin antes de importar.'
            )
        if not families_db:
            raise CommandError(
                'Nenhuma família ativa encontrada no banco. '
                'Cadastre as famílias via admin antes de importar.'
            )

        # ── Contadores ───────────────────────────────────────────────────
        total = 0
        created = 0
        updated = 0
        skipped = 0
        errors = []

        # ── Processar CSV ────────────────────────────────────────────────
        self.stdout.write('\nProcessando linhas...\n')

        with open(csv_path, encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=delimiter)

            # Validar colunas obrigatórias
            required_cols = {'name', 'sources', 'families'}
            if not required_cols.issubset(set(reader.fieldnames or [])):
                missing = required_cols - set(reader.fieldnames or [])
                raise CommandError(
                    f'Colunas obrigatórias ausentes no CSV: {", ".join(missing)}\n'
                    f'Colunas encontradas: {", ".join(reader.fieldnames or [])}'
                )

            try:
                with transaction.atomic():
                    for line_num, row in enumerate(reader, start=2):  # start=2 pois linha 1 é header
                        total += 1

                        # Limpar valores
                        name = row.get('name', '').strip()
                        expected_value = row.get('expected_value', '').strip() or None
                        sources_raw = row.get('sources', '').strip()
                        families_raw = row.get('families', '').strip()

                        # Validar nome
                        if not name:
                            errors.append(f'  Linha {line_num}: nome vazio — ignorado.')
                            skipped += 1
                            continue

                        # Resolver sources
                        source_names = [s.strip() for s in sources_raw.split(separator) if s.strip()]
                        if not source_names:
                            errors.append(f'  Linha {line_num} [{name}]: sem fonte informada — ignorado.')
                            skipped += 1
                            continue

                        source_objs, source_errors = self._resolve_m2m(
                            source_names, sources_db, 'fonte', name, line_num
                        )
                        if source_errors:
                            errors.extend(source_errors)
                            skipped += 1
                            continue

                        # Resolver families
                        family_names = [f.strip() for f in families_raw.split(separator) if f.strip()]
                        if not family_names:
                            errors.append(f'  Linha {line_num} [{name}]: sem família informada — ignorado.')
                            skipped += 1
                            continue

                        family_objs, family_errors = self._resolve_m2m(
                            family_names, families_db, 'família', name, line_num
                        )
                        if family_errors:
                            errors.extend(family_errors)
                            skipped += 1
                            continue

                        # Criar ou atualizar atributo
                        if not dry_run:
                            attr, was_created = Attribute.objects.get_or_create(
                                name=name,
                                user=user,
                                defaults={'expected_value': expected_value, 'is_active': True},
                            )

                            # Se já existia, atualiza o expected_value se mudou
                            if not was_created and attr.expected_value != expected_value:
                                attr.expected_value = expected_value
                                attr.save(update_fields=['expected_value', 'updated_at'])

                            # Sincroniza M2M (adiciona sem remover os existentes)
                            attr.sources.set(source_objs)
                            attr.families.set(family_objs)

                            if was_created:
                                created += 1
                                status = self.style.SUCCESS('CRIADO ')
                            else:
                                updated += 1
                                status = self.style.WARNING('EXISTIA')
                        else:
                            # Dry-run: só conta como seria criado
                            exists = Attribute.objects.filter(name=name, user=user).exists()
                            if exists:
                                updated += 1
                                status = self.style.WARNING('EXISTIA')
                            else:
                                created += 1
                                status = self.style.SUCCESS('CRIADO ')

                        src_names = ', '.join(s.name for s in source_objs)
                        fam_names = ', '.join(f.name for f in family_objs)
                        self.stdout.write(
                            f'  [{status}] Linha {line_num:>4} | {name:<30} | '
                            f'Fontes: {src_names} | Famílias: {fam_names}'
                        )

                    # Se dry-run, faz rollback explícito
                    if dry_run:
                        transaction.set_rollback(True)

            except Exception as e:
                raise CommandError(f'Erro inesperado durante a importação: {e}')

        # ── Relatório final ──────────────────────────────────────────────
        self.stdout.write('\n' + '─' * 60)
        self.stdout.write(self.style.SUCCESS('  RELATÓRIO FINAL'))
        self.stdout.write('─' * 60)
        self.stdout.write(f'  Total de linhas processadas : {total}')
        self.stdout.write(f'  Criados                     : {self.style.SUCCESS(str(created))}')
        self.stdout.write(f'  Já existiam (atualizados)   : {self.style.WARNING(str(updated))}')
        self.stdout.write(f'  Ignorados com erro          : {self.style.ERROR(str(skipped))}')

        if errors:
            self.stdout.write('\n' + self.style.ERROR('  ERROS ENCONTRADOS:'))
            for err in errors:
                self.stdout.write(self.style.ERROR(err))

        if dry_run:
            self.stdout.write('\n' + self.style.WARNING(
                '  ⚠  Dry-run concluído. Nenhum dado foi salvo.'
            ))
        else:
            self.stdout.write('\n' + self.style.SUCCESS('  ✓  Importação concluída com sucesso.'))

        self.stdout.write('─' * 60 + '\n')

    # ── Helpers ──────────────────────────────────────────────────────────

    def _get_user(self, username):
        """Resolve o usuário que será vinculado aos atributos."""
        if username:
            try:
                return User.objects.get(username=username)
            except User.DoesNotExist:
                raise CommandError(
                    f'Usuário "{username}" não encontrado. '
                    f'Usuários disponíveis: {", ".join(User.objects.values_list("username", flat=True))}'
                )

        # Sem username informado: usa primeiro superusuário
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            raise CommandError(
                'Nenhum superusuário encontrado. '
                'Informe um usuário com --user <username> ou crie um superusuário primeiro.'
            )
        return user

    def _resolve_m2m(self, names, db_dict, field_label, attr_name, line_num):
        """
        Resolve uma lista de nomes para objetos do banco.
        Retorna (lista_de_objetos, lista_de_erros).
        Se houver qualquer erro, retorna lista vazia e erros preenchidos.
        """
        objs = []
        errors = []

        for name in names:
            obj = db_dict.get(name.lower())
            if obj is None:
                errors.append(
                    f'  Linha {line_num} [{attr_name}]: '
                    f'{field_label} "{name}" não encontrada no banco ou inativa. '
                    f'Disponíveis: {", ".join(db_dict.keys())}'
                )
            else:
                objs.append(obj)

        if errors:
            return [], errors
        return objs, []

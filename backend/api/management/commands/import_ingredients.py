import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загружает ингредиенты из сsv файла.'

    def handle(self, *args, **options):
        with open(
            'api/data/ingredients.csv',
            'r', encoding='utf-8'
        ) as file:
            reader = csv.reader(file)
            Ingredient.objects.all().delete
            for row in reader:
                name, measurement_unit = row
                Ingredient.objects.get_or_create(
                    name=name, measurement_unit=measurement_unit
                )

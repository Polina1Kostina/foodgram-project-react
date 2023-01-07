import csv

from django.core.management import BaseCommand

from foodgram import settings
from recipes.models import Ingredient

MODELS_FILES = {
    Ingredient: 'ingredients.csv',
}


class Command(BaseCommand):
    help = 'Загрузка из csv файла'

    def handle(self, *args, **kwargs):
        data_path = settings.BASE_DIR
        with open(
            f'{data_path}/data/ingredients.csv',
            'r',
            encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                _, created = Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1],
                    )
        self.stdout.write(self.style.SUCCESS('Ингридиенты загружены.'))

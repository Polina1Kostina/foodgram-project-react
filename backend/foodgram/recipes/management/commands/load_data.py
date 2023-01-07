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
            Ingredient.objects.bulk_create(
                Ingredient(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('Ингридиенты загружены.'))

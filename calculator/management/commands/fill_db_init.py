from django.core.management.base import BaseCommand
from calculator.models import FoodCategory, FoodItem
import pandas


CATEGORIES_TO_INSERT = ["Baked Foods", "Meats", "Vegetables", "Fruits", "Snacks"]


class Command(BaseCommand):
    help = 'Fill database with initial data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        df = pandas.read_excel('calculator/management/commands/dataset.xls')
        categories_series = df["Food Group"]
        categories_series.drop_duplicates(keep='first', inplace=True)
        for category in categories_series.values:
            if category not in CATEGORIES_TO_INSERT:
                continue
            if FoodCategory.objects.filter(name=category).first():
                continue
            self.stdout.write(self.style.SUCCESS(f'Category to insert {category}'))
            FoodCategory(name=category).save()
        for index, row in df.iterrows():
            category = FoodCategory.objects.filter(name=row["Food Group"]).first()
            if not category:
                continue
            self.stdout.write(self.style.SUCCESS(f'Food item to insert {row["name"]}'))
            FoodItem(category=category,
                     carbohydrate=row["Carbohydrate (g)"],
                     fats=row["Fat (g)"],
                     protein=row["Protein (g)"],
                     calorie=row["Calories"],
                     name=row["name"]).save()
        self.stdout.write(self.style.SUCCESS('Successfully filled database'))


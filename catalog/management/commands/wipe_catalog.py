from django.core.management.base import BaseCommand
from catalog.models import Category, Item, Person, UserInteraction
from django.db import connection

class Command(BaseCommand):
    help = "Supprime toutes les données du catalogue (sans affecter les comptes)"

    def handle(self, *args, **options):
        # On supprime dans un ordre logique (relations FK d’abord)
        self.stdout.write("Suppression des interactions...")
        UserInteraction.objects.all().delete()

        self.stdout.write("Suppression des items...")
        Item.objects.all().delete()

        self.stdout.write("Suppression des personnes (auteurs, producteurs)...")
        Person.objects.all().delete()

        self.stdout.write("Suppression des catégories...")
        Category.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("✅ Catalogue vidé avec succès (hors comptes)"))

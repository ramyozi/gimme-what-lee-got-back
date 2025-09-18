# catalog/management/commands/populate_catalog.py
import requests
import random
from django.core.management.base import BaseCommand
from catalog.models import Category, Item, Person
from accounts.models import Account


class Command(BaseCommand):
    help = "Peuple le catalogue avec des comics Marvel/DC (focus Batman inclus)"

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=50, help="Nombre d'items à récupérer (par défaut 50)")

    def handle(self, *args, **options):
        publishers = ["Marvel", "DC Comics"]
        categories = {p: Category.objects.get_or_create(name=p)[0] for p in publishers}

        user, _ = Account.objects.get_or_create(username="admin", defaults={"role": "admin"})

        urls = [
            f"https://openlibrary.org/search.json?q=batman&limit={options['limit']}",
            f"https://openlibrary.org/search.json?q=marvel&limit={options['limit']}",
            f"https://openlibrary.org/search.json?q=dc+comics&limit={options['limit']}",
        ]

        for url in urls:
            response = requests.get(url)
            data = response.json()

            for doc in data.get("docs", []):
                title = doc.get("title")
                description = doc.get("first_sentence") if isinstance(doc.get("first_sentence"), str) else ""
                publisher_name = (doc.get("publisher") or ["DC Comics"])[0]  # fallback DC
                category = categories["Marvel"] if "marvel" in publisher_name.lower() else categories["DC Comics"]

                # Image OpenLibrary (covers)
                image_url = None
                if "cover_i" in doc:
                    image_url = f"https://covers.openlibrary.org/b/id/{doc['cover_i']}-L.jpg"

                # URL externe
                key = doc.get("key")
                external_url = f"https://openlibrary.org{key}" if key else None

                # Tags basiques : mots du titre + publisher
                tags = title.split(" ") if title else []
                if publisher_name:
                    tags.append(publisher_name)

                # Création ou mise à jour
                item, created = Item.objects.update_or_create(
                    title=title,
                    category=category,
                    defaults={
                        "description": description or "Pas de description disponible",
                        "created_by": user,
                        "image": image_url,
                        "url": external_url,
                        "tags": tags,
                    },
                )

                # Associer auteurs
                for author_name in doc.get("author_name", []):
                    author, _ = Person.objects.get_or_create(name=author_name)
                    item.authors.add(author)

                item.save()

                action = "✅ Créé" if created else "♻️ Mis à jour"
                self.stdout.write(f"{action} : {title} ({publisher_name})")

        self.stdout.write(self.style.SUCCESS("🎉 Catalogue enrichi avec Marvel/DC Comics !"))

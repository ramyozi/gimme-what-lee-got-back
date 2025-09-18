# catalog/management/commands/populate_catalog.py
import requests
from django.core.management.base import BaseCommand
from catalog.models import Category, Item, Person
from accounts.models import Account
from core.settings import env  # <- use your environ setup

class Command(BaseCommand):
    help = "Populate the catalog with comics from ComicVine"

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=25, help="Number of comics to fetch")
        parser.add_argument("--query", type=str, default="", help="Search query (e.g., 'batman')")

    def handle(self, *args, **options):
        API_KEY = env("COMICVINE_API_KEY", default=None)
        if not API_KEY:
            self.stdout.write(self.style.ERROR("❌ COMICVINE_API_KEY not set in .env"))
            return

        query = options["query"]
        limit = options["limit"]

        user, _ = Account.objects.get_or_create(username="admin", defaults={"role": "admin"})

        url = f"https://comicvine.gamespot.com/api/issues/?api_key={API_KEY}&format=json&filter=name:{query}&limit={limit}"
        headers = {"User-Agent": "MyDjangoApp/1.0"}

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"❌ API request failed: {response.status_code}"))
            self.stdout.write(self.style.ERROR(response.text))
            return

        try:
            data = response.json()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Failed to decode JSON: {e}"))
            self.stdout.write(self.style.ERROR(response.text))
            return

        for issue in data.get("results", []):
            title = issue.get("name") or "Untitled"
            description = issue.get("description") or "No description available"
            category_name = issue.get("volume", {}).get("name") or "Misc"
            category, _ = Category.objects.get_or_create(name=category_name)

            image_url = issue.get("image", {}).get("original_url")
            external_url = issue.get("site_detail_url")

            tags = [category_name]
            if title:
                tags += title.split(" ")

            item, created = Item.objects.update_or_create(
                title=title,
                category=category,
                defaults={
                    "description": description,
                    "created_by": user,
                    "image": image_url,
                    "url": external_url,
                    "tags": tags,
                },
            )

            # Add people (authors, editors, etc.)
            for person_data in issue.get("person_credits", []) + issue.get("story_arc_credits", []):
                name = person_data.get("name")
                if name:
                    person, _ = Person.objects.get_or_create(name=name)
                    item.authors.add(person)

            item.save()
            action = "✅ Created" if created else "♻️ Updated"
            self.stdout.write(f"{action}: {title} ({category_name})")

        self.stdout.write(self.style.SUCCESS(f"🎉 Catalog populated with {len(data.get('results', []))} comics!"))

# catalog/management/commands/populate_catalog.py
import requests
from django.core.management.base import BaseCommand
from catalog.models import Category, Item, Person
from accounts.models import Account


class Command(BaseCommand):
    help = "Populate the catalog with items from Open Library"

    def add_arguments(self, parser):
        parser.add_argument(
            "--query",
            type=str,
            default="comics",
            help="Search query (e.g., 'batman', 'superhero')",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=25,
            help="Number of items to fetch from Open Library",
        )

    def handle(self, *args, **options):
        query = options["query"]
        limit = options["limit"]

        url = f"https://openlibrary.org/search.json?q={query}&limit={limit}"
        self.stdout.write(f"📡 Fetching from: {url}")

        resp = requests.get(url)
        if resp.status_code != 200:
            self.stdout.write(self.style.ERROR(f"❌ Request failed: {resp.status_code}"))
            return

        data = resp.json()
        docs = data.get("docs", [])
        if not docs:
            self.stdout.write(self.style.WARNING("⚠️ No results returned"))
            return

        # Ensure admin user exists
        user, _ = Account.objects.get_or_create(
            username="admin", defaults={"role": "admin"}
        )

        created_count = 0
        updated_count = 0

        for doc in docs:
            title = doc.get("title") or "Untitled"
            if not title.strip() or title.lower() == "untitled":
                continue  # skip useless items

            description = (
                doc.get("first_sentence")
                or doc.get("subtitle")
                or "No description available"
            )

            category_name = "Books/Comics"
            category, _ = Category.objects.get_or_create(name=category_name)

            external_url = f"https://openlibrary.org{doc.get('key')}"
            tags = doc.get("subject", [])[:5]

            item, created = Item.objects.update_or_create(
                title=title,
                category=category,
                defaults={
                    "description": str(description),
                    "created_by": user,
                    "url": external_url,
                    "tags": tags,
                },
            )

            # Add authors
            for author_name in doc.get("author_name", []):
                person, _ = Person.objects.get_or_create(name=author_name)
                item.authors.add(person)

            if created:
                created_count += 1
                self.stdout.write(f"✅ Created: {title}")
            else:
                updated_count += 1
                self.stdout.write(f"♻️ Updated: {title}")

        self.stdout.write(
            self.style.SUCCESS(
                f"🎉 Done! {created_count} new items, {updated_count} updated."
            )
        )

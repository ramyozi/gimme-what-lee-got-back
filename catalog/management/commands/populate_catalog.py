import requests, random
from django.core.management.base import BaseCommand
from django.conf import settings
from catalog.models import Category, Item, Person
from accounts.models import Account


class Command(BaseCommand):
    help = "Populate the catalog with comics (Marvel/DC) using ComicVine API"

    def handle(self, *args, **opts):
        # ─────────── Check ComicVine API Key ───────────
        if not getattr(settings, "COMICVINE_API_KEY", None):
            self.stderr.write("❌ ComicVine API key missing in .env.")
            return

        # ─────────── Select Universe ───────────
        available = ["marvel", "dc"]
        print("\n📚 Available universes:")
        for i, lib in enumerate(available, 1):
            print(f"  {i}. {lib.capitalize()}")

        while True:
            universe = input(f"Select a universe ({'/'.join(available)}): ").strip().lower()
            if universe in available:
                break
            print("⚠️ Invalid choice. Try again.")

        # ─────────── Example Searches ───────────
        examples = {
            "marvel": ["iron man", "spider-man", "x-men", "captain america", "doctor strange"],
            "dc": ["batman", "superman", "wonder woman", "flash", "green lantern"],
        }[universe]

        print("\n💡 Example searches:")
        for ex in examples:
            print(f"  • {ex}")

        query = input(f"Enter a search term (default '{examples[0]}'): ").strip() or examples[0]

        # ─────────── Limit ───────────
        while True:
            try:
                limit = int(input("How many items? (max 25): ").strip() or 10)
                if 1 <= limit <= 25:
                    break
                print("⚠️ Please enter a number between 1 and 25.")
            except ValueError:
                print("⚠️ Please enter a valid number.")

        # ─────────── Populate via ComicVine ───────────
        self._populate_comicvine(query, limit, universe)

    # ────────────────────────────────────────────────────────
    # ComicVine population logic
    # ────────────────────────────────────────────────────────
    def _populate_comicvine(self, query, limit, universe="marvel"):
        base_url = settings.COMICVINE_BASE_URL.rstrip("/")
        url = f"{base_url}/search/"
        params = {
            "api_key": settings.COMICVINE_API_KEY,
            "format": "json",
            "resources": "issue",
            "query": query,
            "limit": limit,
        }
        headers = {
            "User-Agent": getattr(settings, "COMICVINE_USER_AGENT", "django-catalog-bot/1.0"),
            "Accept": "application/json",
        }

        self.stdout.write(f"🔎 Searching ComicVine for '{query}' ({universe}) ...")
        try:
            r = requests.get(url, params=params, headers=headers, timeout=25)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            self.stderr.write(f"❌ ComicVine request failed: {e}")
            return

        results = data.get("results", [])
        if not results:
            self.stderr.write(f"⚠️ No results found for '{query}' on ComicVine.")
            return

        user, _ = Account.objects.get_or_create(username="admin", defaults={"role": "admin"})
        cat, _ = Category.objects.get_or_create(name=f"{universe.capitalize()} Comics")

        imported = 0
        for res in results:
            if self._save_item(res, cat, user, universe):
                imported += 1

        self.stdout.write(f"✅ {imported} comics imported successfully from ComicVine ({universe}).")

    # ────────────────────────────────────────────────────────
    # Shared save logic
    # ────────────────────────────────────────────────────────
    def _save_item(self, data, category, user, universe):
        try:
            title = data.get("name") or data.get("volume", {}).get("name")
            desc = data.get("deck") or data.get("description") or "No description available."
            url = data.get("site_detail_url")
            image = data.get("image", {}).get("super_url") or data.get("image", {}).get("thumb_url")

            creators = data.get("person_credits", []) or data.get("creators", {}).get("items", [])
            rating = round(random.uniform(3.0, 5.0), 2)
            nratings = random.randint(10, 300)
            popularity = nratings * rating / 10

            item, _ = Item.objects.update_or_create(
                title=title or "Untitled",
                category=category,
                defaults={
                    "description": desc,
                    "created_by": user,
                    "url": url,
                    "image": image,
                    "tags": [universe],
                    "rating": rating,
                    "number_of_ratings": nratings,
                    "popularity_score": popularity,
                },
            )

            for c in creators:
                name = c.get("name") if isinstance(c, dict) else str(c)
                role = (c.get("role") if isinstance(c, dict) else "").lower()
                if not name:
                    continue
                person, _ = Person.objects.get_or_create(name=name)
                if "writer" in role or "author" in role:
                    item.authors.add(person)
                elif "editor" in role or "producer" in role:
                    item.producers.add(person)
                else:
                    item.contributors.add(person)

            return True

        except Exception as e:
            self.stderr.write(f"⚠️ Error saving item: {e}")
            return False

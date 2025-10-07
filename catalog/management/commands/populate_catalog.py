import requests, hashlib, time, random
from django.core.management.base import BaseCommand
from django.conf import settings
from catalog.models import Category, Item, Person
from accounts.models import Account


class Command(BaseCommand):
    help = "Interactively populate the catalog from Marvel or DC (ComicVine) APIs"

    def handle(self, *args, **opts):
        has_marvel = bool(settings.MARVEL_PUBLIC_KEY and settings.MARVEL_PRIVATE_KEY)
        has_dc = bool(settings.COMICVINE_API_KEY)

        # ─────────── No data available ───────────
        if not has_marvel and not has_dc:
            self.stderr.write(
                "❌ Neither Marvel nor ComicVine API keys are configured. "
                "Please add them in your .env file first."
            )
            return

        # ─────────── Choose library ───────────
        available = []
        if has_marvel:
            available.append("marvel")
        if has_dc:
            available.append("dc")

        print("\n📚 Available libraries:")
        for i, lib in enumerate(available, 1):
            print(f"  {i}. {lib.capitalize()}")
        while True:
            choice = input(f"Select a library ({'/'.join(available)}): ").strip().lower()
            if choice in available:
                universe = choice
                break
            print("⚠️ Invalid choice. Try again.")

        # ─────────── Choose query ───────────
        if universe == "marvel":
            examples = ["spider-man", "iron man", "black widow", "x-men", "doctor strange"]
        else:
            examples = ["batman", "superman", "wonder woman", "peacemaker", "booster gold"]

        print("\n💡 Example searches:")
        for ex in examples:
            print(f"  • {ex}")

        query = input(f"Enter a search term (default '{examples[0]}'): ").strip() or examples[0]
        # ─────────── Choose limit ───────────
        while True:
            try:
                limit = int(input("How many items? (max 25): ").strip() or 10)
                if 1 <= limit <= 25:
                    break
                print("⚠️ Please enter a number between 1 and 25.")
            except ValueError:
                print("⚠️ Please enter a valid number.")

        if universe == "marvel":
            self._populate_marvel(query, limit)
        else:
            self._populate_comicvine(query, limit)

    # ────────── Marvel ──────────
    def _auth_params(self):
        ts = str(int(time.time()))
        h = hashlib.md5((ts + settings.MARVEL_PRIVATE_KEY + settings.MARVEL_PUBLIC_KEY).encode()).hexdigest()
        return {"ts": ts, "apikey": settings.MARVEL_PUBLIC_KEY, "hash": h}

    def _populate_marvel(self, query, limit):
        base = settings.MARVEL_BASE_URL.rstrip("/")
        url = f"{base}/comics"
        params = self._auth_params() | {"titleStartsWith": query, "limit": limit}
        r = requests.get(url, params=params, timeout=20)
        if r.status_code != 200:
            self.stderr.write(f"❌ Marvel {r.status_code}: {r.text[:300]}")
            return
        comics = r.json().get("data", {}).get("results", [])
        user, _ = Account.objects.get_or_create(username="admin", defaults={"role": "admin"})
        cat, _ = Category.objects.get_or_create(name="Marvel Comics")
        for c in comics:
            self._save_item(c, cat, user, "marvel")

    # ────────── ComicVine / DC ──────────
    def _populate_comicvine(self, query, limit):
        if not settings.COMICVINE_API_KEY:
            self.stderr.write("❌ Missing ComicVine key")
            return
        url = f"{settings.COMICVINE_BASE_URL.rstrip('/')}/search/"
        params = {
            "api_key": settings.COMICVINE_API_KEY,
            "format": "json",
            "resources": "issue",
            "query": query,
            "limit": limit,
        }
        headers = {
            "User-Agent": getattr(settings, "COMICVINE_USER_AGENT", "gimme-what-lee-got/1.0"),
            "Accept": "application/json",
        }
        r = requests.get(url, params=params, headers=headers, timeout=20)
        if r.status_code != 200:
            self.stderr.write(f"❌ ComicVine {r.status_code}: {r.text[:300]}")
            return
        results = r.json().get("results", [])
        user, _ = Account.objects.get_or_create(username="admin", defaults={"role": "admin"})
        cat, _ = Category.objects.get_or_create(name="DC Comics")
        for res in results:
            self._save_item(res, cat, user, "dc")

    # ────────── Shared save logic ──────────
    def _save_item(self, data, category, user, universe):
        if universe == "marvel":
            title = data.get("title")
            desc = data.get("description") or "No description"
            urls = data.get("urls", [])
            url = urls[0]["url"] if urls else None
            thumb = data.get("thumbnail") or {}
            image = None
            if thumb and not thumb.get("path", "").endswith("image_not_available"):
                image = f"{thumb['path']}.{thumb['extension']}"
            creators = data.get("creators", {}).get("items", [])
        else:
            title = data.get("name") or data.get("volume", {}).get("name")
            desc = data.get("deck") or data.get("description") or "No description"
            url = data.get("site_detail_url")
            image = data.get("image", {}).get("super_url") or data.get("image", {}).get("thumb_url")
            creators = data.get("person_credits", []) or data.get("creators", {}).get("items", [])

        rating = round(random.uniform(3.0, 5.0), 2)
        nratings = random.randint(20, 500)
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

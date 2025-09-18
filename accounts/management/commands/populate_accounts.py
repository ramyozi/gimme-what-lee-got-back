# accounts/management/commands/populate_accounts.py
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from accounts.models import Account


class Command(BaseCommand):
    help = "Crée un admin et 3 utilisateurs de test (admin / admin, userX / password)"

    def add_arguments(self, parser):
        # Option pour reset les comptes existants
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Supprime les comptes de test existants avant de les recréer",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            self.stdout.write("🗑 Suppression des comptes de test existants...")
            Account.objects.filter(
                username__in=["admin", "user1", "user2", "user3"]
            ).delete()

        # Création de l'admin
        admin, created = Account.objects.get_or_create(
            username="admin",
            defaults={
                "password": make_password("admin"),
                "role": "admin",
                "is_superuser": True,
                "is_staff": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS("✅ Admin créé (admin / admin)"))
        else:
            self.stdout.write("♻️ Admin déjà existant")

        # Création des 3 utilisateurs
        for i in range(1, 4):
            username = f"user{i}"
            user, created = Account.objects.get_or_create(
                username=username,
                defaults={
                    "password": make_password("password"),
                    "role": "member",
                },
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Utilisateur créé ({username} / password)")
                )
            else:
                self.stdout.write(f"♻️ Utilisateur {username} déjà existant")

        self.stdout.write(self.style.SUCCESS("🎉 Comptes de test disponibles"))

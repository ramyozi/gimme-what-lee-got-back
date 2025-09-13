from accounts.models import Account, Role
from catalog.models import Category, Item, UserInteraction

# Supprimer toutes les interactions
UserInteraction.objects.all().delete()

# Supprimer tous les items
Item.objects.all().delete()

# Supprimer toutes les catégories
Category.objects.all().delete()

# Supprimer tous les utilisateurs sauf le superuser actuel si besoin
Account.objects.exclude(is_superuser=True).delete()

# Supprimer tous les rôles si tu veux repartir de zéro
Role.objects.all().delete()

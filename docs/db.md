# Account
### créer rapidement un admin et 3 utilisateurs de test
#### (user1, password) (user2, password) (user3, password) (admin, admin)
``` python manage.py populate_accounts ```

### Supprimer tt les comptes existants puis recréer ces comptes ^^
``` python manage.py populate_accounts --reset```

# Catalog
## Nettoyer avant si nécessaire :
``` python manage.py wipe_catalog```

## Peupler avec 50 items :
``` python manage.py populate_catalog --limit 50```


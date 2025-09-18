
import uuid
from django.db import migrations, models


def fill_uuids(apps, schema_editor):
    Account = apps.get_model('accounts', 'Account')
    for account in Account.objects.all():
        if not account.uuid:
            account.uuid = uuid.uuid4()
            account.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_add_uuid_field'),
    ]

    operations = [
        migrations.RunPython(fill_uuids, reverse_code=migrations.RunPython.noop),

        migrations.RemoveField(
            model_name='account',
            name='id',
        ),

        migrations.RenameField(
            model_name='account',
            old_name='uuid',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='account',
            name='id',
            field=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False),
        ),
    ]

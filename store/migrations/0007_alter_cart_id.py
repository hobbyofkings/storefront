from django.db import migrations, models
import uuid

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20210903_1318'),
    ]

    operations = [
        # Drop the table if there is no data to preserve.
        migrations.DeleteModel(
            name='Cart',
        ),
        # Recreate the Cart table with UUID as the primary key.
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)),
                # Add other fields here that the 'Cart' model has.
                # Example: ('user', models.ForeignKey(on_delete=models.CASCADE, to='auth.User')),
                # Add all the necessary fields here.
            ],
        ),
    ]
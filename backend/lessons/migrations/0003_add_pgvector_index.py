from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("lessons", "0002_use_vector_embeddings"),
    ]

    operations = []

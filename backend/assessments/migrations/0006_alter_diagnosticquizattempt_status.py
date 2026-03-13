from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0005_seed_structured_diagnostic_quiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnosticquizattempt',
            name='status',
            field=models.CharField(choices=[('NOT_STARTED', 'NOT_STARTED'), ('IN_PROGRESS', 'IN_PROGRESS'), ('COMPLETED', 'COMPLETED'), ('CANCELLED', 'CANCELLED'), ('INVALID', 'INVALID')], default='NOT_STARTED', max_length=20),
        ),
    ]


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0009_user_diagnostic_completed_user_engagement_score_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserTopicBehavior",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("topic", models.CharField(max_length=255)),
                ("velocity_avg", models.FloatField(default=0.0)),
                ("last_mastery", models.FloatField(blank=True, null=True)),
                ("last_mastery_at", models.DateTimeField(blank=True, null=True)),
                ("failure_streak", models.IntegerField(default=0)),
                ("avg_response_time", models.FloatField(default=0.0)),
                ("avg_hints_used", models.FloatField(default=0.0)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.user")),
            ],
        ),
        migrations.CreateModel(
            name="DifficultyShift",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("topic", models.CharField(max_length=255)),
                ("from_difficulty", models.CharField(max_length=50)),
                ("to_difficulty", models.CharField(max_length=50)),
                ("reason", models.CharField(max_length=100)),
                ("mastery", models.FloatField(blank=True, null=True)),
                ("velocity", models.FloatField(blank=True, null=True)),
                ("failure_streak", models.IntegerField(default=0)),
                ("avg_response_time", models.FloatField(blank=True, null=True)),
                ("avg_hints_used", models.FloatField(blank=True, null=True)),
                ("success", models.BooleanField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.user")),
            ],
        ),
    ]

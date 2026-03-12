from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0009_user_diagnostic_completed_user_engagement_score_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="RecommendationStrategyAssignment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("strategy_name", models.CharField(max_length=50)),
                ("strategy_version", models.CharField(default="v1", max_length=20)),
                ("assigned_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="core.user")),
            ],
        ),
        migrations.CreateModel(
            name="RecommendationEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("strategy_name", models.CharField(max_length=50)),
                ("strategy_version", models.CharField(max_length=20)),
                ("algorithm_name", models.CharField(max_length=100)),
                ("recommended_lesson_id", models.IntegerField(blank=True, null=True)),
                ("recommended_topic", models.CharField(blank=True, max_length=255, null=True)),
                ("recommendation_confidence", models.FloatField(default=0.0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.user")),
            ],
        ),
        migrations.CreateModel(
            name="RecommendationOutcome",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("accepted", models.BooleanField(default=False)),
                ("completed", models.BooleanField(default=False)),
                ("completion_rate", models.FloatField(default=0.0)),
                ("mastery_before", models.FloatField(blank=True, null=True)),
                ("mastery_after", models.FloatField(blank=True, null=True)),
                ("mastery_delta", models.FloatField(blank=True, null=True)),
                ("accepted_at", models.DateTimeField(blank=True, null=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("event", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="evaluation.recommendationevent")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.user")),
            ],
        ),
    ]

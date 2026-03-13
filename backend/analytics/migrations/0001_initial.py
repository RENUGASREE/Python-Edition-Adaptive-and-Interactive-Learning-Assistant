from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0014_auto_20260312_1114'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearningPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
                ('recommended_modules', models.JSONField(blank=True, default=list)),
                ('recommended_lessons', models.JSONField(blank=True, default=list)),
                ('reasoning', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='learning_plans', to='core.user')),
            ],
        ),
        migrations.CreateModel(
            name='SkillGapAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(db_index=True, max_length=255)),
                ('accuracy', models.FloatField(default=0.0)),
                ('status', models.CharField(max_length=20)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skill_gaps', to='core.user')),
            ],
            options={
                'unique_together': {('user', 'topic')},
            },
        ),
        migrations.AddIndex(
            model_name='skillgapanalysis',
            index=models.Index(fields=['user', 'topic'], name='analytics_skill_user_topic_idx'),
        ),
        migrations.AddIndex(
            model_name='skillgapanalysis',
            index=models.Index(fields=['user', 'status'], name='analytics_skill_user_status_idx'),
        ),
        migrations.AddIndex(
            model_name='learningplan',
            index=models.Index(fields=['user', 'generated_at'], name='analytics_plan_user_gen_idx'),
        ),
    ]


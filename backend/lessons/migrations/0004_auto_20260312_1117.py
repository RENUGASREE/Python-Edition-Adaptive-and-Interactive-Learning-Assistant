from django.db import migrations, connection, OperationalError, models
from django.conf import settings
try:
    import pgvector.django
except ImportError:
    pgvector = None

class SafeRunSQL(migrations.RunSQL):
    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        if schema_editor.connection.vendor == 'postgresql':
            # Check if vector extension exists
            with schema_editor.connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM pg_type WHERE typname = 'vector';")
                if not cursor.fetchone():
                    return
            try:
                super().database_forwards(app_label, schema_editor, from_state, to_state)
            except (OperationalError, Exception):
                pass

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        if schema_editor.connection.vendor == 'postgresql':
            try:
                super().database_backwards(app_label, schema_editor, from_state, to_state)
            except (OperationalError, Exception):
                pass

class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('lessons', '0003_add_pgvector_index'),
        ('core', '0014_auto_20260312_1114'),
    ]

    operations = [
        SafeRunSQL(
            sql=[
                "ALTER TABLE lessons_lessonprofile ALTER COLUMN embedding_vector TYPE vector(1536) USING embedding_vector::vector(1536);",
                "ALTER TABLE lessons_lessonchunk ALTER COLUMN embedding_vector TYPE vector(1536) USING embedding_vector::vector(1536);"
            ],
            reverse_sql=[
                "ALTER TABLE lessons_lessonprofile ALTER COLUMN embedding_vector TYPE jsonb USING embedding_vector::jsonb;",
                "ALTER TABLE lessons_lessonchunk ALTER COLUMN embedding_vector TYPE jsonb USING embedding_vector::jsonb;"
            ],
            state_operations=[
                migrations.AlterField(
                    model_name='lessonprofile',
                    name='embedding_vector',
                    field=pgvector.django.VectorField(blank=True, dimensions=1536, null=True) if pgvector else models.JSONField(blank=True, null=True),
                ),
                migrations.AlterField(
                    model_name='lessonchunk',
                    name='embedding_vector',
                    field=pgvector.django.VectorField(blank=True, dimensions=1536, null=True) if pgvector else models.JSONField(blank=True, null=True),
                ),
            ]
        )
    ]

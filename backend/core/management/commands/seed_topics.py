from django.core.management.base import BaseCommand
from core.models import Topic

class Command(BaseCommand):
    help = 'Seed predefined topics for learning analytics'

    def handle(self, *args, **options):
        topics = [
            {'name': 'Variables & Data Types', 'canonical_name': 'variables', 'order': 1, 'description': 'Basic variable assignment, data types, type conversion'},
            {'name': 'Conditionals', 'canonical_name': 'conditions', 'order': 2, 'description': 'if/elif/else statements, comparison operators, logical operators'},
            {'name': 'Loops', 'canonical_name': 'loops', 'order': 3, 'description': 'for/while loops, range(), break/continue, list comprehensions'},
            {'name': 'Functions', 'canonical_name': 'functions', 'order': 4, 'description': 'Function definition, parameters, return values, scope, lambda functions'},
            {'name': 'Data Structures', 'canonical_name': 'data_structures', 'order': 5, 'description': 'Lists, tuples, dictionaries, sets, string methods'},
            {'name': 'Object-Oriented Programming', 'canonical_name': 'oop', 'order': 6, 'description': 'Classes, objects, inheritance, methods, encapsulation'},
        ]

        created = 0
        for topic_data in topics:
            topic, created_new = Topic.objects.get_or_create(
                canonical_name=topic_data['canonical_name'],
                defaults=topic_data
            )
            if created_new:
                created += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded/updated {created} topics. Total topics: {Topic.objects.count()}'
            )
        )

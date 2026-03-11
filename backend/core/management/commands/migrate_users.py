from django.core.management.base import BaseCommand
from django.db import connection, transaction
from core.models import User, Module, Lesson, Quiz, Question, Challenge, DiagnosticQuestionMeta
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Migrate users from Node.js users table to Django core_user table'

    def add_arguments(self, parser):
        parser.add_argument(
            '--seed-placement-quiz',
            action='store_true',
            help='Seed placement quiz questions for the first lesson',
        )
        parser.add_argument(
            '--seed-adaptive-curriculum',
            action='store_true',
            help='Seed adaptive lessons, module quizzes, and challenges',
        )
        parser.add_argument(
            '--seed-diagnostic-quiz',
            action='store_true',
            help='Seed the 30-question diagnostic quiz and tags',
        )

    def handle(self, *args, **kwargs):
        if kwargs.get('seed_placement_quiz'):
            self.seed_placement_quiz()
            return
        if kwargs.get('seed_adaptive_curriculum'):
            self.seed_adaptive_curriculum()
            return
        if kwargs.get('seed_diagnostic_quiz'):
            self.seed_diagnostic_quiz()
            return

        with connection.cursor() as cursor:
            # Check if users table exists
            cursor.execute("SELECT to_regclass('public.users')")
            if not cursor.fetchone()[0]:
                self.stdout.write(self.style.ERROR('users table not found'))
                return

            # Fetch all users from Node.js table
            cursor.execute("SELECT id, email, first_name, last_name, password_hash, created_at FROM users")
            rows = cursor.fetchall()

            for row in rows:
                user_id, email, first_name, last_name, password_hash, created_at = row
                
                if not email:
                    self.stdout.write(self.style.WARNING(f'Skipping user {user_id} with no email'))
                    continue

                if User.objects.filter(email=email).exists():
                    self.stdout.write(self.style.WARNING(f'User {email} already exists'))
                    # Update original_uuid if missing
                    u = User.objects.get(email=email)
                    if not u.original_uuid:
                        u.original_uuid = user_id
                        u.save()
                    continue

                try:
                    # Create Django user
                    # We set a default password because we can't easily port the custom scrypt hash.
                    user = User(
                        username=email, # Use email as username
                        email=email,
                        first_name=first_name or '',
                        last_name=last_name or '',
                        password=make_password('password123'),
                        original_uuid=user_id,
                        is_active=True
                    )
                    user.save()
                    
                    # Update date_joined if available
                    if created_at:
                        user.date_joined = created_at
                        user.save()

                    self.stdout.write(self.style.SUCCESS(f'Successfully migrated user {email}. Password set to "password123"'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to migrate user {email}: {str(e)}'))

    def seed_placement_quiz(self):
        module = Module.objects.order_by('order').first()
        if module:
            lesson = Lesson.objects.filter(module_id=module.id).order_by('order').first()
        else:
            lesson = Lesson.objects.order_by('id').first()

        if not lesson:
            self.stdout.write(self.style.ERROR('No lesson found to attach placement quiz'))
            return

        quiz, _ = Quiz.objects.get_or_create(lesson_id=lesson.id, title='Placement Quiz')
        Question.objects.filter(quiz_id=quiz.id).delete()

        questions = [
            {
                "text": "What is the output of print(2 + 3 * 4)?",
                "options": [
                    {"text": "20", "correct": False},
                    {"text": "14", "correct": True},
                    {"text": "24", "correct": False},
                    {"text": "9", "correct": False},
                ],
                "points": 10,
            },
            {
                "text": "Which syntax creates a list of three zeros?",
                "options": [
                    {"text": "[0, 0, 0]", "correct": False},
                    {"text": "[0] * 3", "correct": True},
                    {"text": "list(0, 0, 0)", "correct": False},
                    {"text": "{0, 0, 0}", "correct": False},
                ],
                "points": 10,
            },
            {
                "text": "What is the type of the value \"3\" in Python?",
                "options": [
                    {"text": "int", "correct": False},
                    {"text": "float", "correct": False},
                    {"text": "str", "correct": True},
                    {"text": "bool", "correct": False},
                ],
                "points": 10,
            },
            {
                "text": "Which is a valid Python variable name?",
                "options": [
                    {"text": "1st_value", "correct": False},
                    {"text": "my-var", "correct": False},
                    {"text": "my_var1", "correct": True},
                    {"text": "class", "correct": False},
                ],
                "points": 10,
            },
            {
                "text": "Which built-in function returns the number of items in a list?",
                "options": [
                    {"text": "count()", "correct": False},
                    {"text": "size()", "correct": False},
                    {"text": "len()", "correct": True},
                    {"text": "length()", "correct": False},
                ],
                "points": 10,
            },
            {
                "text": "What is the result of list(range(3))?",
                "options": [
                    {"text": "[1, 2, 3]", "correct": False},
                    {"text": "[0, 1, 2]", "correct": True},
                    {"text": "[0, 1, 2, 3]", "correct": False},
                    {"text": "[3, 2, 1]", "correct": False},
                ],
                "points": 10,
            },
            {
                "text": "Which creates a dictionary with keys \"a\" and \"b\"?",
                "options": [
                    {"text": "{'a': 1, 'b': 2}", "correct": True},
                    {"text": "['a': 1, 'b': 2]", "correct": False},
                    {"text": "('a': 1, 'b': 2)", "correct": False},
                    {"text": "{'a', 'b'}", "correct": False},
                ],
                "points": 10,
            },
            {
                "text": "How many times does this loop run? for i in range(1, 4):",
                "options": [
                    {"text": "2", "correct": False},
                    {"text": "3", "correct": True},
                    {"text": "4", "correct": False},
                    {"text": "It runs forever", "correct": False},
                ],
                "points": 10,
            },
            {
                "text": "Which defines a function with a default parameter?",
                "options": [
                    {"text": "def f(x = 5):", "correct": True},
                    {"text": "def f(x == 5):", "correct": False},
                    {"text": "def f(x): = 5", "correct": False},
                    {"text": "def f(x): default 5", "correct": False},
                ],
                "points": 10,
            },
            {
                "text": "Which list comprehension squares numbers 0 through 4?",
                "options": [
                    {"text": "[x*x for x in range(5)]", "correct": True},
                    {"text": "[x^2 for x in range(1,5)]", "correct": False},
                    {"text": "map(x*x, range(5))", "correct": False},
                    {"text": "{x*x for x in range(5)}", "correct": False},
                ],
                "points": 10,
            },
            {
                "text": "What does a try/except block handle in Python?",
                "options": [
                    {"text": "Syntax rules", "correct": False},
                    {"text": "Runtime exceptions", "correct": True},
                    {"text": "Variable creation", "correct": False},
                    {"text": "Loop iteration", "correct": False},
                ],
                "points": 10,
            },
            {
                "text": "What is the purpose of __init__ in a class?",
                "options": [
                    {"text": "It is called when an object is created", "correct": True},
                    {"text": "It deletes an object", "correct": False},
                    {"text": "It creates a static method", "correct": False},
                    {"text": "It imports a module", "correct": False},
                ],
                "points": 10,
            },
        ]

        with transaction.atomic():
            Question.objects.bulk_create([
                Question(
                    quiz_id=quiz.id,
                    text=q["text"],
                    type="multiple_choice",
                    options=q["options"],
                    points=q["points"],
                )
                for q in questions
            ])

        self.stdout.write(self.style.SUCCESS(f'Placement quiz seeded with {len(questions)} questions for lesson {lesson.id}'))

    def seed_adaptive_curriculum(self):
        level_order = ["Beginner", "Intermediate", "Pro"]
        modules = Module.objects.all().order_by('order')
        if not modules:
            self.stdout.write(self.style.ERROR('No modules found to seed adaptive curriculum'))
            return

        for module in modules:
            module_lessons = Lesson.objects.filter(module_id=module.id).order_by('order', 'id')
            if not module_lessons:
                continue

            base_lessons = [l for l in module_lessons if (l.difficulty or '').strip().lower() not in ['intermediate', 'pro']]
            if not base_lessons:
                base_lessons = list(module_lessons)

            for base_lesson in base_lessons:
                base_content = base_lesson.content
                base_lesson.difficulty = "Beginner"
                base_lesson.content = self.build_lesson_content(base_content, module.title, base_lesson.title, "Beginner")
                base_lesson.save(update_fields=["difficulty", "content"])

                for level in level_order[1:]:
                    slug = f"{base_lesson.slug}-{level.lower()}"
                    title = f"{base_lesson.title} ({level})"
                    content = self.build_lesson_content(base_content, module.title, base_lesson.title, level)
                    existing = Lesson.objects.filter(module_id=module.id, slug=slug).first()
                    if existing:
                        existing.title = title
                        existing.difficulty = level
                        existing.content = content
                        existing.order = base_lesson.order
                        existing.duration = base_lesson.duration
                        existing.save(update_fields=["title", "difficulty", "content", "order", "duration"])
                        self.clone_challenge(base_lesson, existing, level)
                    else:
                        new_lesson = Lesson.objects.create(
                            module_id=module.id,
                            title=title,
                            slug=slug,
                            content=content,
                            order=base_lesson.order,
                            difficulty=level,
                            duration=base_lesson.duration,
                        )
                        self.clone_challenge(base_lesson, new_lesson, level)

            for level in level_order:
                first_lesson = Lesson.objects.filter(module_id=module.id, difficulty=level).order_by('order', 'id').first()
                if not first_lesson:
                    continue
                quiz, _ = Quiz.objects.get_or_create(lesson_id=first_lesson.id, title="Module Quiz")
                Question.objects.filter(quiz_id=quiz.id).delete()
                questions = self.build_module_questions(module, level)
                Question.objects.bulk_create([
                    Question(
                        quiz_id=quiz.id,
                        text=q["text"],
                        type="multiple_choice",
                        options=q["options"],
                        points=q["points"],
                    )
                    for q in questions
                ])

        self.stdout.write(self.style.SUCCESS('Adaptive curriculum seeded successfully'))

    def seed_diagnostic_quiz(self):
        module = Module.objects.order_by('order').first()
        if module:
            lesson = Lesson.objects.filter(module_id=module.id).order_by('order').first()
        else:
            lesson = Lesson.objects.order_by('id').first()

        if not lesson:
            self.stdout.write(self.style.ERROR('No lesson found to attach diagnostic quiz'))
            return

        quiz, _ = Quiz.objects.get_or_create(lesson_id=lesson.id, title='Diagnostic Quiz')
        existing_questions = list(Question.objects.filter(quiz_id=quiz.id))
        if existing_questions:
            DiagnosticQuestionMeta.objects.filter(question_id__in=[q.id for q in existing_questions]).delete()
            Question.objects.filter(quiz_id=quiz.id).delete()

        modules = [
            ("Basics", 6),
            ("Control Flow", 5),
            ("Loops", 5),
            ("Functions", 5),
            ("Data Structures", 5),
            ("OOPS", 4),
        ]
        difficulties = ["easy", "medium", "hard"]
        questions = []

        for module_name, count in modules:
            for idx in range(count):
                difficulty = difficulties[idx % len(difficulties)]
                correct_text = f"{module_name} concept {idx + 1}"
                options = [
                    {"text": f"{correct_text} correct usage", "correct": True},
                    {"text": f"{module_name} concept {idx + 1} incorrect usage", "correct": False},
                    {"text": "Unrelated Python topic", "correct": False},
                    {"text": "Invalid syntax choice", "correct": False},
                ]
                questions.append({
                    "text": f"[{module_name}] Select the correct statement for question {idx + 1}.",
                    "options": options,
                    "difficulty": difficulty,
                    "module_tag": module_name,
                })

        with transaction.atomic():
            created_questions = Question.objects.bulk_create([
                Question(
                    quiz_id=quiz.id,
                    text=q["text"],
                    type="multiple_choice",
                    options=q["options"],
                    points=10,
                )
                for q in questions
            ])

            DiagnosticQuestionMeta.objects.bulk_create([
                DiagnosticQuestionMeta(
                    question_id=question.id,
                    module_tag=questions[idx]["module_tag"],
                    difficulty=questions[idx]["difficulty"],
                )
                for idx, question in enumerate(created_questions)
            ])

        self.stdout.write(self.style.SUCCESS(f'Diagnostic quiz seeded with {len(questions)} questions for lesson {lesson.id}'))

    def build_lesson_content(self, base_content, module_title, lesson_title, level):
        focus = {
            "Beginner": [
                "Focus on core concepts and syntax.",
                "Practice reading and writing short Python expressions.",
                "Build intuition with small, predictable examples."
            ],
            "Intermediate": [
                "Connect concepts across lessons and explain why they work.",
                "Use slightly larger examples with multiple steps.",
                "Identify common pitfalls and how to avoid them."
            ],
            "Pro": [
                "Apply concepts to real-world problem patterns.",
                "Reason about edge cases and trade-offs.",
                "Write concise, efficient solutions and explain design choices."
            ]
        }
        focus_lines = focus.get(level, focus["Beginner"])
        focus_block = "\n".join([f"- {line}" for line in focus_lines])
        return "\n".join([
            base_content.strip(),
            "",
            f"## {level} Focus",
            focus_block,
            "",
            f"## {level} Practice",
            f"Rewrite one example from this lesson in your own words, then code it.",
            "",
            f"## {level} Check",
            f"Explain how {lesson_title} supports the goals of the {module_title} module."
        ]).strip()

    def build_module_questions(self, module, level):
        lessons = list(Lesson.objects.filter(module_id=module.id, difficulty="Beginner").order_by('order', 'id'))
        lesson_titles = [l.title for l in lessons] or [module.title]
        questions = []
        for idx in range(5):
            title = lesson_titles[idx % len(lesson_titles)]
            correct = f"Understand the core idea of {title} in Python."
            options = [
                {"text": correct, "correct": True},
                {"text": "Configure a production web server for deployment.", "correct": False},
                {"text": "Design a UI layout using HTML and CSS.", "correct": False},
                {"text": "Manage operating system processes and threads.", "correct": False},
            ]
            questions.append({
                "text": f"[{level}] Which statement best reflects the goal of {title}?",
                "options": options,
                "points": 10,
            })
        return questions

    def clone_challenge(self, base_lesson, new_lesson, level):
        base_challenge = Challenge.objects.filter(lesson_id=base_lesson.id).first()
        if not base_challenge:
            return
        title = f"{base_challenge.title} ({level})"
        description = "\n".join([
            base_challenge.description.strip(),
            "",
            f"Level: {level}. Provide a clean solution and explain your approach."
        ]).strip()
        existing = Challenge.objects.filter(lesson_id=new_lesson.id).first()
        if existing:
            existing.title = title
            existing.description = description
            existing.initial_code = base_challenge.initial_code
            existing.solution_code = base_challenge.solution_code
            existing.test_cases = base_challenge.test_cases
            existing.points = base_challenge.points
            existing.save(update_fields=["title", "description", "initial_code", "solution_code", "test_cases", "points"])
            return
        Challenge.objects.create(
            lesson_id=new_lesson.id,
            title=title,
            description=description,
            initial_code=base_challenge.initial_code,
            solution_code=base_challenge.solution_code,
            test_cases=base_challenge.test_cases,
            points=base_challenge.points,
        )

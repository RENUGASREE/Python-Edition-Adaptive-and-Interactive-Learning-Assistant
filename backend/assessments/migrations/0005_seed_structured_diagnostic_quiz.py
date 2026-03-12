from django.db import migrations, transaction


def seed_structured_diagnostic_quiz(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    DiagnosticQuiz = apps.get_model("assessments", "DiagnosticQuiz")
    DiagnosticQuestion = apps.get_model("assessments", "DiagnosticQuestion")
    DiagnosticOption = apps.get_model("assessments", "DiagnosticOption")

    quiz, _ = DiagnosticQuiz.objects.using(db_alias).get_or_create(title="Python Placement Diagnostic")
    if DiagnosticQuestion.objects.using(db_alias).filter(quiz=quiz).exists():
        return

    def q(text, opts, correct_letter, difficulty, topic, points):
        letter_to_index = {"A": 0, "B": 1, "C": 2, "D": 3}
        return {
            "text": text.strip(),
            "options": opts,
            "correct_index": letter_to_index[correct_letter],
            "difficulty": difficulty,
            "topic": topic,
            "points": points,
        }

    questions = [
        q("What is the correct way to assign a value to a variable?", ["int x = 5", "x = 5", "var x = 5", "let x = 5"], "B", "easy", "Python Basics", 1),
        q("What is the output of print(type(3.14)) ?", ["float", "<class 'float'>", "decimal", "number"], "B", "easy", "Python Basics", 1),
        q("Which data type is immutable?", ["list", "dictionary", "tuple", "set"], "C", "medium", "Python Basics", 2),
        q('What is the result of "5" + "5" ?', ["10", "55", "Error", "5"], "B", "medium", "Python Basics", 2),
        q("What is output?\nx = 10\ndef func():\n    x = 5\nfunc()\nprint(x)", ["5", "10", "Error", "None"], "B", "hard", "Python Basics", 3),
        q("Which keyword is used for condition checking?", ["switch", "if", "case", "loop"], "B", "easy", "Control Flow", 1),
        q("What prints?\nif 0:\n    print(\"Yes\")\nelse:\n    print(\"No\")", ["Yes", "No", "Error", "Nothing"], "B", "medium", "Control Flow", 2),
        q("Equality operator?", ["=", "==", ":=", "!="], "B", "medium", "Control Flow", 2),
        q("What does pass do?", ["Skips program", "Placeholder statement", "Ends loop", "Continues loop"], "B", "hard", "Control Flow", 3),
        q("Nested loop complexity n x n?", ["O(n)", "O(log n)", "O(n^2)", "O(1)"], "C", "hard", "Control Flow", 3),
        q("range(3) produces?", ["1,2,3", "0,1,2", "0,1,2,3", "3 values undefined"], "B", "easy", "Loops", 1),
        q("break does what?", ["Stops loop entirely", "Skips iteration", "Pauses loop", "Restarts loop"], "A", "medium", "Loops", 2),
        q("continue does what?", ["Ends program", "Skips current iteration", "Restarts loop", "Stops loop"], "B", "medium", "Loops", 2),
        q("Infinite loop example?", ["while True:", "for i in range(0)", "if True", "break"], "A", "hard", "Loops", 3),
        q("Output of for i in range(1,4)?", ["1 2 3", "0 1 2", "1 2 3 4", "Error"], "A", "easy", "Loops", 1),
        q("Correct function definition?", ["function myFunc()", "def myFunc():", "define myFunc():", "func myFunc():"], "B", "easy", "Functions", 1),
        q("Return without value returns?", ["0", "None", "False", "Error"], "B", "medium", "Functions", 2),
        q("Lambda is?", ["Loop", "Anonymous function", "Class", "Module"], "B", "medium", "Functions", 2),
        q("Default mutable argument issue example?", ["It resets each call", "It persists between calls", "It raises error", "It returns copy"], "B", "hard", "Functions", 3),
        q("Recursion means?", ["Loop", "Function calling itself", "Condition", "Class"], "B", "hard", "Functions", 3),
        q("Dictionary lookup average time?", ["O(n)", "O(1)", "O(log n)", "O(n^2)"], "B", "hard", "Data Structures", 3),
        q("Set allows duplicates?", ["Yes", "No", "Sometimes", "Only numbers"], "B", "medium", "Data Structures", 2),
        q("List comprehension creates?", ["Loop", "New list", "Tuple", "Set"], "B", "medium", "Data Structures", 2),
        q('What does dict.get("x",0) return if x not present?', ["Error", "None", "0", "False"], "C", "medium", "Data Structures", 2),
        q("Tuple is?", ["Mutable", "Immutable", "Dynamic", "Dictionary"], "B", "easy", "Data Structures", 1),
        q("Class is?", ["Object", "Blueprint for objects", "Variable", "Loop"], "B", "easy", "OOP", 1),
        q("__init__ is?", ["Destructor", "Constructor", "Loop", "Variable"], "B", "medium", "OOP", 2),
        q("Inheritance means?", ["Copy code", "Child derives from parent", "Delete class", "Override variable"], "B", "medium", "OOP", 2),
        q("Method overriding means?", ["Duplicate method", "Child redefines parent method", "Delete method", "None"], "B", "hard", "OOP", 3),
        q("Encapsulation means?", ["Hide internal implementation", "Delete variables", "Loop logic", "Multiple inheritance"], "A", "hard", "OOP", 3),
    ]

    with transaction.atomic(using=db_alias):
        for spec in questions:
            qobj = DiagnosticQuestion.objects.using(db_alias).create(
                quiz=quiz,
                topic=spec["topic"],
                difficulty=spec["difficulty"],
                text=spec["text"],
                options=spec["options"],
                correct_index=spec["correct_index"],
                points=spec["points"],
            )
            for i, text in enumerate(spec["options"]):
                DiagnosticOption.objects.using(db_alias).create(
                    question=qobj,
                    text=text,
                    is_correct=(i == spec["correct_index"]),
                )


class Migration(migrations.Migration):
    dependencies = [
        ("assessments", "0004_alter_diagnosticquestion_options_diagnosticoption"),
    ]

    operations = [
        migrations.RunPython(seed_structured_diagnostic_quiz, migrations.RunPython.noop),
    ]


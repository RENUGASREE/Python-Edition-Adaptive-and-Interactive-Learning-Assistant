from django.core.management.base import BaseCommand
from django.db import transaction

from assessments.models import DiagnosticOption, DiagnosticQuestion, DiagnosticQuiz


class Command(BaseCommand):
    help = "Seed a 50-question placement quiz across modules 1-6 with a beginner/intermediate/pro mix."

    def handle(self, *args, **options):
        quiz, _ = DiagnosticQuiz.objects.get_or_create(title="Python Placement Diagnostic")
        DiagnosticOption.objects.filter(question__quiz=quiz).delete()
        DiagnosticQuestion.objects.filter(quiz=quiz).delete()

        def q(topic, difficulty, text, options, correct_index):
            points_map = {"easy": 1, "medium": 2, "hard": 3}
            return DiagnosticQuestion(
                quiz=quiz,
                topic=topic,
                difficulty=difficulty,
                text=text.strip(),
                options=options,
                correct_index=correct_index,
                points=points_map[difficulty],
            )

        questions = [
            # Module 1: Introduction (8)
            q("mod-introduction", "easy", "Which function displays output in Python?", ["print()", "input()", "type()", "len()"], 0),
            q("mod-introduction", "easy", "What does `input()` return before casting?", ["A string", "An integer", "A list", "A boolean"], 0),
            q("mod-introduction", "medium", "What is printed by `print('A', 'B', sep='-')`?", ["A B", "A-B", "AB", "['A', 'B']"], 1),
            q("mod-introduction", "hard", "Why use `flush=True` with `print()`?", ["To force buffered output immediately", "To uppercase text", "To read stdin", "To suppress newline"], 0),
            q("mod-introduction", "medium", "What is `type(5).__name__`?", ["'int'", "'type'", "'number'", "'integer'"], 0),
            q("mod-introduction", "hard", "Which statement about CPython is correct?", ["It compiles source to bytecode before VM execution", "It only interprets raw source", "Bytecode runs only in notebooks", "It emits machine code directly for every script"], 0),
            q("mod-introduction", "easy", "Which is a valid Python comment?", ["# note", "// note", "/* note */", "-- note"], 0),
            q("mod-introduction", "medium", "What does `\\n` represent?", ["A tab", "A newline", "A quote", "A backslash"], 1),

            # Module 2: Data Types and Variables (8)
            q("mod-data-types", "easy", "Which variable name is valid?", ["2score", "user-name", "user_score", "class"], 2),
            q("mod-data-types", "easy", "What is the type of `3.14`?", ["int", "float", "Decimal", "complex"], 1),
            q("mod-data-types", "medium", "What happens in `x, y = y, x`?", ["Values are swapped", "Syntax error", "Both become tuples", "Only `x` changes"], 0),
            q("mod-data-types", "medium", "Which collection stores unique unordered items?", ["list", "tuple", "set", "dict"], 2),
            q("mod-data-types", "hard", "Why can two names reference the same list?", ["Assignment binds names to objects", "Lists auto-copy on assignment", "Python blocks copying lists", "Lists are immutable"], 0),
            q("mod-data-types", "hard", "What is `bool([])`?", ["True", "False", "[]", "None"], 1),
            q("mod-data-types", "medium", "What does `dict.get('missing', 0)` return when absent?", ["KeyError", "None", "0", "False"], 2),
            q("mod-data-types", "easy", "Which creates an empty dictionary?", ["[]", "{}", "()", "dict[]"], 1),

            # Module 3: Control Flow (8)
            q("mod-control-flow", "easy", "Which keyword starts a conditional block?", ["if", "when", "switch", "match"], 0),
            q("mod-control-flow", "easy", "Which operator checks equality?", ["=", "==", ":=", "is"], 1),
            q("mod-control-flow", "medium", "What is printed by `if 0: print('Yes') else: print('No')`?", ["Yes", "No", "0", "Nothing"], 1),
            q("mod-control-flow", "medium", "What does `elif` mean?", ["else if", "every if", "end if", "equal if"], 0),
            q("mod-control-flow", "hard", "What does `is` compare?", ["Numeric value", "Object identity", "String length", "Truthiness"], 1),
            q("mod-control-flow", "hard", "De Morgan: `not (A or B)` equals:", ["`not A and not B`", "`not A or not B`", "`A and B`", "`A or B`"], 0),
            q("mod-control-flow", "medium", "Main benefit of a guard clause?", ["Avoids deep nesting via early exit", "Makes variables global", "Converts `if` to `while`", "Disables exceptions"], 0),
            q("mod-control-flow", "hard", "In `match`, what does `case _:` do?", ["Repeats previous case", "Matches anything remaining", "Raises an error", "Compares identity"], 1),

            # Module 4: Loops (8)
            q("mod-loops-iteration", "easy", "Best loop when iteration count is known?", ["while", "for", "do-while", "repeat"], 1),
            q("mod-loops-iteration", "easy", "What does `range(3)` produce?", ["1,2,3", "0,1,2", "0,1,2,3", "3"], 1),
            q("mod-loops-iteration", "medium", "What does `continue` do?", ["Stops loop", "Skips to next iteration", "Restarts program", "Repeats current iteration forever"], 1),
            q("mod-loops-iteration", "medium", "What does `break` do?", ["Skips one iteration", "Exits the loop", "Raises syntax error", "Rewinds counter"], 1),
            q("mod-loops-iteration", "hard", "Nested loops both run `n` times. Complexity?", ["O(1)", "O(log n)", "O(n)", "O(n^2)"], 3),
            q("mod-loops-iteration", "hard", "When does loop `else` run?", ["Always after first iteration", "Only if loop ends without `break`", "Only on empty iterables", "Only after `continue`"], 1),
            q("mod-loops-iteration", "medium", "Common cause of infinite `while` loop?", ["Using `range()`", "Not updating loop condition", "Printing inside loop", "Too many variables"], 1),
            q("mod-loops-iteration", "easy", "What does `for ch in 'abc':` iterate over?", ["Indexes", "Whole string once", "Each character", "Only vowels"], 2),

            # Module 5: Functions (9)
            q("mod-functions-scope", "easy", "How do you define `greet`?", ["function greet():", "def greet():", "func greet():", "define greet():"], 1),
            q("mod-functions-scope", "easy", "Which keyword sends a value back?", ["yield", "pass", "return", "break"], 2),
            q("mod-functions-scope", "medium", "What does `*args` collect?", ["Extra keyword args", "Extra positional args", "Only integers", "Return values"], 1),
            q("mod-functions-scope", "medium", "Default return value without `return`?", ["0", "False", "Empty string", "None"], 3),
            q("mod-functions-scope", "hard", "Why are mutable default args risky?", ["Re-created every call", "Same object reused across calls", "Break recursion", "Can only hold strings"], 1),
            q("mod-functions-scope", "hard", "In LEGB, what does `E` mean?", ["External", "Enclosing", "Evaluated", "Exported"], 1),
            q("mod-functions-scope", "medium", "What is a lambda?", ["Loop helper", "Small anonymous function", "Module import", "Class decorator"], 1),
            q("mod-functions-scope", "hard", "What is recursion?", ["Looping over a list", "Function calling itself", "Importing module twice", "Passing tuple to a function"], 1),
            q("mod-functions-scope", "medium", "What is a pure function?", ["One that prints output", "One that mutates global state", "One with deterministic output and no side effects", "One that must be recursive"], 2),

            # Module 6: OOP, Files, and Modules (9)
            q("mod-modules-packages", "easy", "What does `self` represent in an instance method?", ["Parent class", "Current object instance", "Global namespace", "Constructor return value"], 1),
            q("mod-modules-packages", "easy", "Which method initializes object state?", ["__start__", "__init__", "__new__", "__build__"], 1),
            q("mod-modules-packages", "medium", "What is inheritance?", ["Hiding private data", "Creating class from existing class", "Calling methods together", "Comparing objects"], 1),
            q("mod-modules-packages", "medium", "What does `with open(path) as f:` guarantee?", ["File is encrypted", "File is closed automatically", "File becomes read-only", "File loads fully into memory"], 1),
            q("mod-modules-packages", "hard", "Why prefer `pathlib.Path` over raw path strings?", ["Object-oriented cross-platform path operations", "Works only on Linux", "Required for JSON", "Bypasses permissions"], 0),
            q("mod-modules-packages", "hard", "What is polymorphism?", ["Child class redefining behavior through a shared interface", "Class with no methods", "Copying all attributes", "Making every attribute private"], 0),
            q("mod-modules-packages", "medium", "What does encapsulation focus on?", ["Repeating logic", "Bundling data with controlled access", "Removing constructors", "Converting methods to loops"], 1),
            q("mod-modules-packages", "hard", "When prefer composition over inheritance?", ["Build behavior from reusable parts without strict is-a relationship", "Need fewer files", "Avoid objects", "Class has only one method"], 0),
            q("mod-modules-packages", "medium", "Which import loads only `Path`?", ["import pathlib.Path", "from pathlib import Path", "include pathlib.Path", "using pathlib.Path"], 1),
        ]

        with transaction.atomic():
            DiagnosticQuestion.objects.bulk_create(questions)
            saved_questions = list(DiagnosticQuestion.objects.filter(quiz=quiz).order_by("id"))
            for question in saved_questions:
                for idx, option_text in enumerate(question.options or []):
                    DiagnosticOption.objects.create(
                        question=question,
                        text=option_text,
                        is_correct=(idx == question.correct_index),
                    )

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(questions)} structured diagnostic questions"))

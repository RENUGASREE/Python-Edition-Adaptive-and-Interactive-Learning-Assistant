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
            q("mod-introduction", "easy", "Which function displays output in Python?", ["print()", "input()", "type()", "len()"], 0),
            q("mod-introduction", "easy", "What does `input()` return before you cast it?", ["A string", "An integer", "A list", "A boolean"], 0),
            q("mod-introduction", "medium", "What is printed by `print('A', 'B', sep='-')`?", ["A B", "A-B", "AB", "['A', 'B']"], 1),
            q("mod-introduction", "hard", "Why would you use `flush=True` with `print()`?", ["To force buffered output to appear immediately", "To convert text to uppercase", "To read from stdin", "To suppress the newline"], 0),
            q("mod-introduction", "medium", "What is the result of `type(5).__name__`?", ["'int'", "'type'", "'number'", "'integer'"], 0),
            q("mod-introduction", "hard", "Which statement about Python execution is correct?", ["CPython compiles source to bytecode before the VM executes it", "Python always interprets source without compilation", "Bytecode runs only in Jupyter notebooks", "Python converts every file directly to machine code"], 0),
            q("mod-introduction", "easy", "Which line is a valid Python comment?", ["# note", "// note", "/* note */", "-- note"], 0),
            q("mod-introduction", "medium", "What does the escape sequence `\\n` represent?", ["A tab", "A newline", "A quote", "A backslash"], 1),

            q("mod-variables-types", "easy", "Which name follows Python variable naming rules?", ["2score", "user-name", "user_score", "class"], 2),
            q("mod-variables-types", "easy", "What is the type of `3.14`?", ["int", "float", "Decimal", "complex"], 1),
            q("mod-variables-types", "medium", "What happens in `x, y = y, x`?", ["The values are swapped", "A syntax error occurs", "Both variables become tuples", "Only `x` changes"], 0),
            q("mod-variables-types", "medium", "Which collection is unordered and stores unique values?", ["list", "tuple", "set", "dict"], 2),
            q("mod-variables-types", "hard", "Why can two variables sometimes reference the same list object?", ["Assignment binds another name to the same object", "Lists are copied automatically", "Python forbids copying lists", "Because lists are immutable"], 0),
            q("mod-variables-types", "hard", "What is the result of `bool([])`?", ["True", "False", "[]", "None"], 1),
            q("mod-variables-types", "medium", "What does `dict.get('missing', 0)` return if the key is absent?", ["KeyError", "None", "0", "False"], 2),
            q("mod-variables-types", "easy", "Which expression creates an empty list?", ["{}", "[]", "()", "set()"], 1),

            q("mod-control-flow", "easy", "Which keyword starts a conditional block?", ["if", "when", "switch", "match"], 0),
            q("mod-control-flow", "easy", "Which operator checks equality?", ["=", "==", ":=", "is"], 1),
            q("mod-control-flow", "medium", "What is printed by `if 0: print('Yes') else: print('No')`?", ["Yes", "No", "0", "Nothing"], 1),
            q("mod-control-flow", "medium", "What does `elif` mean in Python?", ["else if", "every if", "end if", "equal if"], 0),
            q("mod-control-flow", "hard", "What does the `is` operator compare?", ["Numeric value", "Identity of two objects", "String length", "Boolean truthiness"], 1),
            q("mod-control-flow", "hard", "According to De Morgan's law, `not (A or B)` is equivalent to:", ["`not A and not B`", "`not A or not B`", "`A and B`", "`A or B`"], 0),
            q("mod-control-flow", "medium", "What is the main benefit of a guard clause?", ["It avoids deep nesting by returning early", "It makes all variables global", "It converts `if` to `while`", "It disables exceptions"], 0),
            q("mod-control-flow", "hard", "What does `case _:` mean in structural pattern matching?", ["Repeat the previous case", "Match any remaining input", "Raise an error", "Compare object identity"], 1),

            q("mod-loops-iteration", "easy", "Which loop is best when you know the iteration count?", ["while", "for", "do-while", "repeat"], 1),
            q("mod-loops-iteration", "easy", "What does `range(3)` produce?", ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "3"], 1),
            q("mod-loops-iteration", "medium", "What does `continue` do inside a loop?", ["Stops the loop permanently", "Skips to the next iteration", "Restarts the program", "Repeats the same iteration forever"], 1),
            q("mod-loops-iteration", "medium", "What does `break` do inside a loop?", ["Skips one iteration", "Exits the loop", "Raises a syntax error", "Rewinds the loop counter"], 1),
            q("mod-loops-iteration", "hard", "What is the time complexity of a nested loop where both loops run `n` times?", ["O(1)", "O(log n)", "O(n)", "O(n^2)"], 3),
            q("mod-loops-iteration", "hard", "When does the `else` block on a loop run?", ["Always after the first iteration", "Only if the loop ends without `break`", "Only on empty iterables", "Only after `continue`"], 1),
            q("mod-loops-iteration", "medium", "What is a common cause of an infinite `while` loop?", ["Using `range()`", "Forgetting to update the loop condition", "Printing inside the loop", "Declaring too many variables"], 1),
            q("mod-loops-iteration", "easy", "What does `for ch in 'abc':` iterate over?", ["Indexes", "The whole string once", "Each character", "Only vowels"], 2),

            q("mod-functions-scope", "easy", "How do you define a function named `greet`?", ["function greet():", "def greet():", "func greet():", "define greet():"], 1),
            q("mod-functions-scope", "easy", "Which keyword sends a value back from a function?", ["yield", "pass", "return", "break"], 2),
            q("mod-functions-scope", "medium", "What does `*args` collect?", ["Extra keyword arguments", "Extra positional arguments", "Only integers", "Return values"], 1),
            q("mod-functions-scope", "medium", "What value is returned when a function finishes without `return`?", ["0", "False", "An empty string", "None"], 3),
            q("mod-functions-scope", "hard", "Why is a mutable default argument risky?", ["It is re-created on every call", "The same object is reused across calls", "It makes recursion impossible", "It can only hold strings"], 1),
            q("mod-functions-scope", "hard", "In LEGB name resolution, what does `E` stand for?", ["External", "Enclosing", "Evaluated", "Exported"], 1),
            q("mod-functions-scope", "medium", "What is a lambda in Python?", ["A loop helper", "A small anonymous function", "A module import", "A class decorator"], 1),
            q("mod-functions-scope", "hard", "What is recursion?", ["Looping over a list", "A function calling itself", "Importing a module twice", "Passing a tuple to a function"], 1),

            q("mod-data-types", "easy", "Which list method adds one item to the end?", ["append()", "push()", "add()", "extenditem()"], 0),
            q("mod-data-types", "easy", "Which data structure stores key-value pairs?", ["set", "tuple", "dictionary", "string"], 2),
            q("mod-data-types", "medium", "What does `[x*x for x in range(3)]` produce?", ["[1, 4, 9]", "[0, 1, 4]", "[0, 2, 4]", "(0, 1, 4)"], 1),
            q("mod-data-types", "medium", "Which statement about tuples is correct?", ["Tuples are mutable", "Tuples preserve order and are immutable", "Tuples remove duplicates", "Tuples only store numbers"], 1),
            q("mod-data-types", "hard", "What is the average-time lookup complexity for a dictionary key?", ["O(1)", "O(log n)", "O(n)", "O(n^2)"], 0),
            q("mod-data-types", "hard", "Why would you choose a set over a list for membership tests on large data?", ["Sets keep insertion order better", "Sets usually provide faster membership checks", "Sets allow duplicates", "Sets are indexed"], 1),
            q("mod-data-types", "medium", "What does `'a,b,c'.split(',')` return?", ["'abc'", "['a', 'b', 'c']", "('a', 'b', 'c')", "{'a', 'b', 'c'}"], 1),
            q("mod-data-types", "hard", "What does `zip(names, scores)` conceptually do?", ["Sorts both sequences", "Pairs items from the sequences by position", "Flattens nested lists", "Removes duplicates"], 1),
            q("mod-data-types", "easy", "Which expression creates an empty dictionary?", ["[]", "{}", "()", "dict[]"], 1),

            q("mod-modules-packages", "easy", "What does `self` represent in an instance method?", ["The parent class", "The current object instance", "A global namespace", "A constructor return value"], 1),
            q("mod-modules-packages", "easy", "Which method usually initializes object state?", ["__start__", "__init__", "__new__", "__build__"], 1),
            q("mod-modules-packages", "medium", "What is inheritance?", ["Hiding private data", "Creating a class from an existing class", "Calling two methods together", "Comparing two objects"], 1),
            q("mod-modules-packages", "medium", "What does `with open(path) as f:` guarantee?", ["The file is encrypted", "The file is closed automatically", "The file becomes read-only", "The file loads into memory"], 1),
            q("mod-modules-packages", "hard", "Why is `pathlib.Path` often preferred over raw string path handling?", ["It provides object-oriented, cross-platform path operations", "It only works on Linux", "It is required for JSON files", "It bypasses file permissions"], 0),
            q("mod-modules-packages", "hard", "What is polymorphism in OOP?", ["A child class redefining behavior behind a common interface", "A class with no methods", "Copying all attributes between classes", "Making every attribute private"], 0),
            q("mod-modules-packages", "medium", "What does encapsulation focus on?", ["Repeating logic", "Bundling data and controlling how it is accessed", "Removing constructors", "Converting methods to loops"], 1),
            q("mod-modules-packages", "hard", "When should you prefer composition over inheritance?", ["When you want to build behavior from reusable parts without a strict is-a relationship", "When you need fewer files", "When you want to avoid objects entirely", "When a class has only one method"], 0),
            q("mod-modules-packages", "medium", "Which import style loads only `Path` from `pathlib`?", ["import pathlib.Path", "from pathlib import Path", "include pathlib.Path", "using pathlib.Path"], 1),
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

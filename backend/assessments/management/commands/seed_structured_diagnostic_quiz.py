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
            # Module 1: mod-introduction (Python Basics) - 8 questions
            q("mod-introduction", "easy", "Which is a valid dynamic variable assignment in Python?", ["x = 5", "int x = 5;", "var x := 5", "declare x = 5"], 0),
            q("mod-introduction", "easy", "What built-in function receives direct text input from the user?", ["input()", "read()", "scan()", "getline()"], 0),
            q("mod-introduction", "medium", "What happens when you reassign a typed variable: `y = 10; y = 'hello'`?", ["Python updates `y` to refer to the string", "Syntax error", "Type error", "Memory leak"], 0),
            q("mod-introduction", "medium", "What is the primary role of the CPython garbage collector?", ["Managing memory automatically via reference counting", "Compiling machine code", "Parsing SQL queries", "Handling networking"], 0),
            q("mod-introduction", "hard", "How does Python execute scripts under the hood?", ["Compiles source to bytecode, then evaluates in the Python Virtual Machine", "Compiles directly to CPU machine code", "Evaluates source directly over the OS kernel", "Executes as shell scripts natively"], 0),
            q("mod-introduction", "hard", "What happens to the ID of a variable `name` if reassigned to an entirely new string?", ["`id(name)` changes to point to the new string object", "`id(name)` remains the same", "Strings are mutable so memory stays identical", "Raises NameError"], 0),
            q("mod-introduction", "easy", "How do you output standard text to the terminal?", ["print('text')", "echo 'text'", "console.log('text')", "write('text')"], 0),
            q("mod-introduction", "medium", "Which operand allows casting a string to an integer securely?", ["int('5')", "eval('5')", "parse('5')", "str('5')"], 0),

            # Module 2: mod-data-types - 8 questions
            q("mod-data-types", "easy", "Which collection type preserves ordered sequence and allows mutation?", ["list", "set", "tuple", "string"], 0),
            q("mod-data-types", "easy", "Which literal defines an empty dictionary?", ["{}", "[]", "()", "{null}"], 0),
            q("mod-data-types", "medium", "Why are tuples preferred over lists for dictionary keys?", ["Tuples are immutable, allowing them to be cryptographically hashed", "Tuples are faster to sort", "Lists use too much memory", "You can't loop over lists"], 0),
            q("mod-data-types", "medium", "What does a Set guarantee about its elements?", ["All elements are strictly unique", "They are sorted alphabetically", "They are thread-safe", "Elements preserve insertion order"], 0),
            q("mod-data-types", "hard", "What happens when you append to a list referenced by two different variables?", ["Both variables reflect the appended data since they reference the same object", "Only the first variable reflects it", "A shallow copy is automatically made", "Python blocks the action"], 0),
            q("mod-data-types", "hard", "What is the time complexity of searching a dictionary by key under normal circumstances?", ["O(1)", "O(N)", "O(log N)", "O(N^2)"], 0),
            q("mod-data-types", "easy", "How do you extract the first character of `text = 'hello'`?", ["text[0]", "text(1)", "text.charAt(0)", "text{0}"], 0),
            q("mod-data-types", "medium", "Which method adds a key-value mapping to an existing dictionary `map` safely?", ["map['key'] = 'val'", "map.add('key', 'val')", "map.push('key', 'val')", "map.insert('key', 'val')"], 0),

            # Module 3: mod-control-flow - 8 questions
            q("mod-control-flow", "easy", "Which block guarantees code runs whether an exception occurs or not?", ["finally", "except", "catch", "else"], 0),
            q("mod-control-flow", "easy", "Which statement correctly checks if `node` is strictly `None`?", ["if node is None:", "if node = None:", "if node == None:", "if node equal None:"], 0),
            q("mod-control-flow", "medium", "Why are guard clauses preferred over heavily nested `if-else` blocks?", ["They allow an early function exit preventing code compression", "They execute faster natively", "They force typing enforcement", "They bypass error handling automatically"], 0),
            q("mod-control-flow", "medium", "What differentiates Python 3.10 `match-case` from standard `switch`?", ["It allows structural pattern matching to unpack data", "It is only string-compatible", "It requires explicit `break` keys", "It triggers automatic recursion"], 0),
            q("mod-control-flow", "hard", "What does short-circuit evaluation mean in `A or B`?", ["If A is truthy, B is never evaluated", "A and B run in parallel execution", "Both are evaluated locally regardless", "B overrides A exclusively"], 0),
            q("mod-control-flow", "hard", "How do you catch multiple exception types simultaneously in one except block?", ["except (TypeError, ValueError):", "except TypeError, ValueError:", "catch TypeError or ValueError:", "except [TypeError, ValueError]:"], 0),
            q("mod-control-flow", "medium", "What is the truthy value of `[]`?", ["False", "True", "None", "Error"], 0),
            q("mod-control-flow", "easy", "How do you execute an alternate code path if `if` fails?", ["else", "otherwise", "catch", "default"], 0),

            # Module 4: mod-loops-iteration - 8 questions
            q("mod-loops-iteration", "easy", "Which syntax constructs a list of squares using comprehensions?", ["[x*x for x in data]", "list(x*x if data)", "{x*x loop x}", "for x in data [x*x]"], 0),
            q("mod-loops-iteration", "easy", "What is the most pythonic way to execute a block 10 times?", ["for i in range(10):", "while 10:", "loop 10:", "for (int i=0; i<10; i++):"], 0),
            q("mod-loops-iteration", "medium", "What executes if a `for` loop completes normally without encountering a `break`?", ["An attached `else` block", "An attached `finally` block", "A `catch` block", "It throws an IterationEnd block"], 0),
            q("mod-loops-iteration", "medium", "What does `continue` signify inside a loop?", ["Skip the rest of the current iteration and proceed to the next", "Terminate the entire loop", "Pause the program explicitly", "Rewind the iteration backwards"], 0),
            q("mod-loops-iteration", "hard", "How do generator expressions `(x for x in data)` differ from list comprehensions memory-wise?", ["Generators yield lazily, consuming O(1) memory footprint", "Generators compile faster", "They return a cached tuple", "There is no difference"], 0),
            q("mod-loops-iteration", "hard", "What internal method does a `for` loop utilize to step through objects?", ["__next__()", "__iter_next__()", "__loop__()", "__get__()"], 0),
            q("mod-loops-iteration", "medium", "What loop handles execution continuously until exactly met by condition state?", ["while", "do...while", "for...in", "repeat"], 0),
            q("mod-loops-iteration", "easy", "Can you use multiple variables inside a loop `for key, val in...`?", ["Yes, if unwrapping pairs e.g. .items()", "No, for loops accept only scalars", "Only when utilizing lambda", "Only with external plugins"], 0),

            # Module 5: mod-functions-scope - 9 questions
            q("mod-functions-scope", "easy", "How do you specify arbitrary keyword arguments in a function definition?", ["**kwargs", "*args", "&kwargs", "...args"], 0),
            q("mod-functions-scope", "easy", "What keyword creates small anonymous inline functions?", ["lambda", "def", "inline", "anon"], 0),
            q("mod-functions-scope", "medium", "What does the `global` keyword achieve?", ["Permits modifying an outer module-level variable inside local scope", "Makes a variable accessible over HTTP", "Exports a function to other files", "Instantiates a class singleton"], 0),
            q("mod-functions-scope", "medium", "What is a 'pure' function mathematically and programmatically?", ["Outputs only depend on inputs, causing zero side-effects", "A function utilizing only native libraries", "A function without arguments", "A function triggering no errors permanently"], 0),
            q("mod-functions-scope", "hard", "What is a 'closure' in Python?", ["An inner function remembering state from its enclosing lexical scope", "A function that has stopped running", "A method returning False", "A garbage collected scope"], 0),
            q("mod-functions-scope", "hard", "Why shouldn't you define mutable defaults like `def handle(items=[])`?", ["The list object binds at function definition time, accumulating data across calls", "It violates PEP 8 strict syntax", "Lists cannot be modified inside arguments", "The compiler throws a Syntax Warning"], 0),
            q("mod-functions-scope", "medium", "How do you force the user to pass arguments via keyword exclusively?", ["Using a bare `*` preceding the arguments", "Prefixing the parameter with `&`", "Annotating parameter with @kw", "Adding a global restriction"], 0),
            q("mod-functions-scope", "medium", "What built-in maps a function concurrently over an iterable sequence?", ["map()", "filter()", "reduce()", "apply()"], 0),
            q("mod-functions-scope", "easy", "Which stops function execution and transmits data back?", ["return", "break", "yield", "pass"], 0),

            # Module 6: mod-modules-packages - 9 questions
            q("mod-modules-packages", "easy", "What parameter strictly represents the instance bounded context inside methods?", ["self", "this", "ctx", "parent"], 0),
            q("mod-modules-packages", "easy", "Which special method initializes a class schema when instantiated?", ["__init__", "__start__", "__main__", "__new__"], 0),
            q("mod-modules-packages", "medium", "Explain Polymorphism architecturally.", ["Unified interface execution treating subclasses interchangeably", "Encrypting global variable memory footprints", "Preventing child classes from altering variables", "Overriding standard language keywords"], 0),
            q("mod-modules-packages", "medium", "How do you restrict modification to internal state representing encapsulation?", ["Prefixing attributes with double underscores `__`", "Deploying the @private decorator", "Appending `.private()` during invocation", "Locking the file descriptor locally"], 0),
            q("mod-modules-packages", "hard", "Why is preferring 'Composition over Inheritance' typically safer behaviorally?", ["It avoids deep brittle class hierarchies, enabling decoupled interchangeable behaviors", "Memory limits prevent inheriting class logic", "Inheritance performs notably slower", "Python only allows single inheritance exclusively"], 0),
            q("mod-modules-packages", "hard", "What is the primary role of the `__mro__` mechanism?", ["Resolving hierarchical method execution order across multiple inherited base abstractions", "Monitoring Runtime Overflows during calculation", "Handling Memory Release Operations internally", "None of these"], 0),
            q("mod-modules-packages", "medium", "What does a `@classmethod` receive as its first implicit semantic argument?", ["The class itself (cls)", "The bounded object (self)", "Environmental globals", "Zero implicit arguments"], 0),
            q("mod-modules-packages", "easy", "How do you access native properties dynamically using property logic without parentheses?", ["@property", "@getter", "def get()", "return native()"], 0),
            q("mod-modules-packages", "medium", "Which Python capability lets you intercept standard operators like `+` within classes?", ["Dunder/Magic methods like `__add__`", "The Operations module", "Standard arithmetic wrappers", "Operator inheritance overriding"], 0),
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

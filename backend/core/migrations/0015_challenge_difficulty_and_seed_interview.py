from django.db import migrations, models
from django.utils import timezone


def seed_interview_challenges(apps, schema_editor):
    Challenge = apps.get_model("core", "Challenge")
    samples = [
        {
            "title": "Two Sum",
            "difficulty": "Easy",
            "description": "Return indices of the two numbers that add up to target.",
            "initial_code": "def two_sum(nums, target):\n    # Write your code here\n    pass",
            "solution_code": "def two_sum(nums, target):\n    seen = {}\n    for i, v in enumerate(nums):\n        need = target - v\n        if need in seen:\n            return [seen[need], i]\n        seen[v] = i\n    return []",
            "test_cases": [{"input": "", "expected": ""}],  # Execution handled by custom runner using provided code
            "points": 10,
        },
        {
            "title": "Palindrome Checker",
            "difficulty": "Easy",
            "description": "Check if a string is a palindrome, ignoring non-alphanumeric.",
            "initial_code": "def is_palindrome(s):\n    # Write your code here\n    pass",
            "solution_code": "def is_palindrome(s):\n    t = ''.join(ch.lower() for ch in s if ch.isalnum())\n    return t == t[::-1]",
            "test_cases": [{"input": "", "expected": ""}],
            "points": 8,
        },
        {
            "title": "FizzBuzz Variation",
            "difficulty": "Medium",
            "description": "Print numbers 1..n with 'Fizz' for multiples of 3, 'Buzz' for 5, 'FizzBuzz' for both.",
            "initial_code": "def fizzbuzz(n):\n    # Write your code here\n    pass",
            "solution_code": "def fizzbuzz(n):\n    out = []\n    for i in range(1, n+1):\n        s = ''\n        if i % 3 == 0:\n            s += 'Fizz'\n        if i % 5 == 0:\n            s += 'Buzz'\n        out.append(s or str(i))\n    return out",
            "test_cases": [{"input": "", "expected": ""}],
            "points": 12,
        },
        {
            "title": "String Compression",
            "difficulty": "Medium",
            "description": "Compress a string using counts of repeated characters.",
            "initial_code": "def compress(s):\n    # Write your code here\n    pass",
            "solution_code": "def compress(s):\n    if not s:\n        return ''\n    out = []\n    count = 1\n    prev = s[0]\n    for ch in s[1:]:\n        if ch == prev:\n            count += 1\n        else:\n            out.append(prev + str(count))\n            prev = ch\n            count = 1\n    out.append(prev + str(count))\n    res = ''.join(out)\n    return res if len(res) < len(s) else s",
            "test_cases": [{"input": "", "expected": ""}],
            "points": 14,
        },
        {
            "title": "Prime Number Generator",
            "difficulty": "Hard",
            "description": "Generate all primes up to n using Sieve of Eratosthenes.",
            "initial_code": "def primes(n):\n    # Write your code here\n    pass",
            "solution_code": "def primes(n):\n    sieve = [True]*(n+1)\n    p = 2\n    out = []\n    while p*p <= n:\n        if sieve[p]:\n            for i in range(p*p, n+1, p):\n                sieve[i] = False\n        p += 1\n    for i in range(2, n+1):\n        if sieve[i]:\n            out.append(i)\n    return out",
            "test_cases": [{"input": "", "expected": ""}],
            "points": 20,
        },
    ]
    for item in samples:
        Challenge.objects.get_or_create(
            title=item["title"],
            defaults={
                "lesson_id": 0,
                "description": item["description"],
                "initial_code": item["initial_code"],
                "solution_code": item["solution_code"],
                "test_cases": item["test_cases"],
                "points": item["points"],
                "difficulty": item["difficulty"],
            }
        )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20260312_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='difficulty',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.RunPython(seed_interview_challenges, migrations.RunPython.noop),
    ]


"""
Verify the per-module adaptive difficulty logic end-to-end.
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from assessments.services import _module_difficulty_tier
from core.models import User
from assessments.models import DiagnosticQuizAttempt
from recommendation.services import _get_module_difficulty

# TEST 1: Threshold mapping
print("TEST 1: Score-to-difficulty tier mapping")
print("-" * 45)
test_cases = [
    (0.75, "Pro"),
    (0.80, "Pro"),
    (1.00, "Pro"),
    (0.50, "Intermediate"),
    (0.60, "Intermediate"),
    (0.74, "Intermediate"),
    (0.49, "Beginner"),
    (0.25, "Beginner"),
    (0.00, "Beginner"),
]
all_pass = True
for score, expected in test_cases:
    result = _module_difficulty_tier(score)
    status = "PASS" if result == expected else "FAIL"
    if status == "FAIL": all_pass = False
    print(f"  [{status}] {score:.0%} -> expected={expected}, got={result}")
print(f"\n  Result: {'ALL PASS' if all_pass else 'SOME FAILURES'}")

# TEST 2: Mastery vector check
print("\nTEST 2: Per-module difficulty in mastery_vector")
print("-" * 45)
for user in User.objects.all():
    attempt = DiagnosticQuizAttempt.objects.filter(user=user, status="COMPLETED").order_by("-created_at").first()
    if not attempt:
        print(f"  [{user.username}] No completed attempt")
        continue
    mv = user.mastery_vector or {}
    md_map = mv.get("_module_difficulty", {})
    if not md_map:
        print(f"  [{user.username}] _module_difficulty NOT found")
        continue
    print(f"\n  User: {user.username} | Overall: {attempt.overall_score:.1%} | Level: {user.level}")
    for topic, score in (attempt.module_scores or {}).items():
        expected = _module_difficulty_tier(float(score))
        stored = md_map.get(topic, "MISSING")
        ok = "PASS" if expected == stored else "FAIL"
        print(f"  [{ok}] {topic:<35} {score:.0%} => expected={expected}, stored={stored}")

# TEST 3: _get_module_difficulty resolution
print("\nTEST 3: _get_module_difficulty resolves correctly")
print("-" * 45)
for user in User.objects.all():
    md_map = (user.mastery_vector or {}).get("_module_difficulty", {})
    if not md_map:
        continue
    print(f"\n  User: {user.username}")
    for topic, tier in md_map.items():
        resolved = _get_module_difficulty(user, topic)
        ok = "PASS" if resolved == tier else "FAIL"
        print(f"  [{ok}] {topic:<35} stored={tier}, resolved={resolved}")

print("\nVerification complete.")

"""
Backfill per-module difficulty tiers for existing users who have already
completed the placement quiz but don't yet have the '_module_difficulty'
key in their mastery_vector.

Logic:
  >= 75%  -> Pro
  >= 50%  -> Intermediate
  <  50%  -> Beginner
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import User
from assessments.models import DiagnosticQuizAttempt


def _module_difficulty_tier(score: float) -> str:
    if score >= 0.75:
        return "Pro"
    if score >= 0.50:
        return "Intermediate"
    return "Beginner"


def backfill_user(user):
    attempt = DiagnosticQuizAttempt.objects.filter(
        user=user, status="COMPLETED"
    ).order_by("-created_at").first()

    if not attempt:
        print(f"  [SKIP] No completed attempt for {user.username}")
        return

    module_scores = attempt.module_scores or {}
    if not module_scores:
        print(f"  [SKIP] Empty module_scores for {user.username}")
        return

    mastery_vector = user.mastery_vector or {}
    module_difficulty_map = {}

    for topic, score in module_scores.items():
        tier = _module_difficulty_tier(float(score))
        module_difficulty_map[topic] = tier

    mastery_vector["_module_difficulty"] = module_difficulty_map
    user.mastery_vector = mastery_vector
    user.save(update_fields=["mastery_vector"])

    print(f"\n  User: {user.username}")
    print(f"  Overall Score: {attempt.overall_score:.1%}  |  Global Tier: {attempt.difficulty_tier}")
    print("  Per-module difficulty assignments:")
    for topic, tier in module_difficulty_map.items():
        score = module_scores.get(topic, 0)
        symbol = "🔴" if tier == "Pro" else "🟡" if tier == "Intermediate" else "🟢"
        print(f"    {symbol} {topic:35s} {score:.0%}  =>  {tier}")


print("=" * 60)
print("Backfilling per-module difficulty tiers")
print("=" * 60)

for user in User.objects.all():
    backfill_user(user)

print("\nDone. All users updated.")

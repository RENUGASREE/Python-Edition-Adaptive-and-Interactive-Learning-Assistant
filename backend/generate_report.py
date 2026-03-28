import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from assessments.models import DiagnosticQuizAttempt
from core.models import User

username = 'editionpython@gmail.com'
try:
    user = User.objects.get(username=username)
    attempt = DiagnosticQuizAttempt.objects.filter(user=user).order_by('-created_at').first()
    
    if attempt:
        md_content = f"""# Performance Report: {user.username}
        
## Summary
- **Overall Score:** {attempt.overall_score:.1%}
- **Difficulty Tier:** {attempt.difficulty_tier}
- **Status:** {attempt.status}
- **Completed At:** {attempt.completed_at}

## Module-wise Performance
"""
        for mod, score in attempt.module_scores.items():
            status = "STRONG" if score >= 0.8 else ("IMPROVING" if score >= 0.5 else "WEAK")
            md_content += f"- **{mod}:** {score:.1%} ({status})\n"
            
        with open("performance_report.md", "w", encoding="utf-8") as f:
            f.write(md_content)
        print("Report generated: performance_report.md")
    else:
        print(f"No attempt found for {username}")
except Exception as e:
    print(f"Error: {e}")

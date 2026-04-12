import os
import time
from django.core.management.base import BaseCommand
from core.models import Lesson, Module
from openai import OpenAI

SYSTEM_PROMPT = """You are generating lesson content for an AI-powered Adaptive Learning Platform.
This is NOT simple content generation. You must produce high-quality, consistent, structured educational material.
Depth > Speed. Clarity > Creativity. Consistency across ALL lessons is mandatory.

SECTION RULES:
1. Definition (MANDATORY): Technical definition, 1-2 lines, no metaphors.
2. Why This Matters: Practical usage in software systems.
3. Concept Explanation: Step-by-step. Beginner=simple, Intermediate=patterns, Pro=internals/performance.
4. Mental Model: Exactly one simple helpful model.
5. Code Example: 1 clean example with line-by-line explanation of what each line does and why.
6. Real-World Application: 1 strong realistic use-case.
7. Common Mistakes: Min 2 real beginner mistakes.
8. Best Practices: Min 3 practical rules.
9. Knowledge Check: EXACTLY 2 MCQs, 4 options each, 1 correct.
10. Lesson Challenge: Problem statement + expected behavior.

STRUCTURE (MANDATORY MARKDOWN HEADERS):
## Title
## 1. Definition
## 2. Why This Matters
## 3. Concept Explanation
## 4. Mental Model
## 5. Code Example
## 6. Real-World Application
## 7. Common Mistakes
## 8. Best Practices
## 9. Knowledge Check
## 10. Lesson Challenge
"""

class Command(BaseCommand):
    help = "Generates high-quality AI content for all lessons using OpenAI"

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=180, help='Limit number of lessons to process')
        parser.add_argument('--force', action='store_true', help='Regenerate even if content exists')

    def handle(self, *args, **options):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            self.stdout.write(self.style.ERROR("OPENAI_API_KEY not found in environment"))
            return

        client = OpenAI(api_key=api_key)
        
        lessons = Lesson.objects.all().order_by('module_id', 'order')
        if not options['force']:
            lessons = lessons.filter(content__isnull=True) | lessons.filter(content="") | lessons.filter(content__icontains="placeholder")

        count = 0
        limit = options['limit']

        for lesson in lessons:
            if count >= limit:
                break
            
            module = Module.objects.filter(id=lesson.module_id).first()
            module_name = module.title if module else "Python Programming"
            
            self.stdout.write(f"Generating content for: {lesson.title} ({lesson.difficulty}) in {module_name}...")
            
            user_prompt = f"Topic: {lesson.title}\nModule: {module_name}\nDifficulty: {lesson.difficulty}\n\nPlease generate the full lesson content."
            
            try:
                response = client.chat.completions.create(
                    model="gpt-4o", # Using a high-quality model for depth
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7
                )
                
                content = response.choices[0].message.content
                lesson.content = content
                lesson.save()
                
                self.stdout.write(self.style.SUCCESS(f"Successfully updated {lesson.title}"))
                count += 1
                
                # Small delay to avoid aggressive rate limits
                time.sleep(1)
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to generate for {lesson.title}: {str(e)}"))
                time.sleep(5) # Backoff

        self.stdout.write(self.style.SUCCESS(f"Finished. Generated {count} lessons."))

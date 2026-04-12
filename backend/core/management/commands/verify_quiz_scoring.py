"""Management command to verify quiz scoring integrity."""
from django.core.management.base import BaseCommand
from assessments.models import DiagnosticQuestion
from assessments.serializers import DiagnosticQuestionSerializer
from assessments.services import score_diagnostic
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Verify quiz option ordering and scoring correctness'

    def handle(self, *args, **options):
        User = get_user_model()
        u = User.objects.filter(is_staff=False).first()
        questions = list(DiagnosticQuestion.objects.filter(quiz_id=3).prefetch_related('choices'))
        serialized = DiagnosticQuestionSerializer(questions, many=True).data

        self.stdout.write('=== Option Order vs correct_index Verification ===')
        mismatches = 0
        for q_data, q_obj in zip(serialized, questions):
            opts = q_data['options']
            correct_ids = [str(c.id) for c in q_obj.choices.all() if c.is_correct]
            ci = q_obj.correct_index if q_obj.correct_index is not None else 0
            opt_at_ci = opts[ci] if ci < len(opts) else None
            if opt_at_ci:
                match = str(opt_at_ci['id']) in correct_ids
                status = self.style.SUCCESS('OK') if match else self.style.ERROR('MISMATCH')
                self.stdout.write(f'  Q{q_obj.id}: correct_index={ci}, opt_id={opt_at_ci["id"]}, is_correct={match} [{status}]')
                if not match:
                    mismatches += 1
            else:
                self.stdout.write(self.style.WARNING(f'  Q{q_obj.id}: correct_index={ci} out of range ({len(opts)} opts)'))

        self.stdout.write('')
        if mismatches == 0:
            self.stdout.write(self.style.SUCCESS(f'PASS: All {len(questions)} questions have correct alignment'))
        else:
            self.stdout.write(self.style.ERROR(f'FAIL: {mismatches} mismatches found!'))

        # Test scoring with all-correct answers
        self.stdout.write('\n=== Score Test (All Correct via optionId) ===')
        mock = []
        for q in questions:
            correct_c = next((c for c in q.choices.all() if c.is_correct), None)
            mock.append({
                'questionId': q.id,
                'selectedIndex': q.correct_index,
                'selectedOptionId': str(correct_c.id) if correct_c else None,
            })

        scores, raw, weighted, tier = score_diagnostic(u, 3, mock, update_user=False)
        self.stdout.write(f'  raw={raw}, weighted={weighted}, tier={tier}')
        for mod, sc in scores.items():
            self.stdout.write(f'  {mod}: {sc:.2f}')

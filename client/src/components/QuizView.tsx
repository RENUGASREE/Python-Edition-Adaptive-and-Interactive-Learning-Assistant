import { useState } from "react";
import { cn } from "@/lib/utils";

interface QuizOption {
  text: string;
  correct?: boolean;
}

interface QuizViewProps {
  questions: any[];
  onSubmit: (answers: Record<string, number>) => void;
}

export default function QuizView({ questions, onSubmit }: QuizViewProps) {
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [feedback, setFeedback] = useState<Record<string, { correct: boolean; selected: number }>>({});

  const handleSelect = (questionId: string, optionIndex: number) => {
    if (feedback[questionId]) return; // Already answered

    const question = questions.find((q: any) => q.id === questionId);
    if (!question) return;

    const options: QuizOption[] = Array.isArray(question.options) ? question.options : [];
    const selectedOption = options[optionIndex];
    const isCorrect = selectedOption?.correct || false;

    setAnswers((prev) => ({ ...prev, [questionId]: optionIndex }));
    setFeedback((prev) => ({ ...prev, [questionId]: { correct: isCorrect, selected: optionIndex } }));
  };

  const handleSubmit = () => {
    const unansweredCount = questions.filter(q => answers[q.id] === undefined).length;
    if (unansweredCount > 0) {
      alert(`Please answer all questions before submitting. (${unansweredCount} remaining)`);
      return;
    }
    onSubmit(answers);
  };

  return (
    <div className="space-y-8">
      {questions.map((q: any, qIdx: number) => (
        <div key={q.id} className="space-y-3">
          <div className="font-medium">
            {qIdx + 1}. {q.text}
          </div>
          <div className="grid gap-2">
            {(Array.isArray(q.options) ? q.options : []).map((opt: QuizOption, optIndex: number) => (
              <label
                key={`${q.id}-${optIndex}`}
                className={cn(
                  "flex items-center gap-3 p-3 border rounded-lg cursor-pointer hover:border-primary/60",
                  feedback[q.id] && feedback[q.id].selected === optIndex && feedback[q.id].correct && "border-green-500 bg-green-500/10",
                  feedback[q.id] && feedback[q.id].selected === optIndex && !feedback[q.id].correct && "border-red-500 bg-red-500/10",
                )}
              >
                <input
                  type="radio"
                  name={`question-${q.id}`}
                  checked={answers[q.id] === optIndex}
                  onChange={() => handleSelect(q.id, optIndex)}
                  className="form-radio h-4 w-4 text-primary focus:ring-primary"
                  disabled={!!feedback[q.id]}
                />
                <span>{opt.text}</span>
                {feedback[q.id] && feedback[q.id].selected === optIndex && feedback[q.id].correct && <span className="ml-auto text-green-500">✓ Correct</span>}
                {feedback[q.id] && feedback[q.id].selected === optIndex && !feedback[q.id].correct && <span className="ml-auto text-red-500">✗ Incorrect</span>}
              </label>
            ))}
          </div>
        </div>
      ))}
      <button onClick={handleSubmit} className="px-4 py-2 bg-primary text-primary-foreground rounded-lg">
        Submit
      </button>
    </div>
  );
}

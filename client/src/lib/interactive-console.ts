/**
 * Utilities for interactive console execution
 * Detects input() calls and manages step-by-step input collection
 */

export interface InputCall {
  index: number;
  prompt: string;
  line: number;
}

/**
 * Parse Python code and extract all input() calls with their prompts
 */
export function parseInputCalls(code: string): InputCall[] {
  const lines = code.split('\n');
  const calls: InputCall[] = [];
  let callIndex = 0;

  lines.forEach((line, lineNum) => {
    // Match input(...) with string or without
    const inputMatches = line.matchAll(/input\s*\(\s*(['"`])(.*?)\1\s*\)/g);
    
    for (const match of inputMatches) {
      const prompt = match[2];
      calls.push({
        index: callIndex++,
        prompt,
        line: lineNum + 1,
      });
    }
  });

  return calls;
}

/**
 * Get the prompt text from an input call
 */
export function getInputPrompt(inputCall: InputCall): string {
  return inputCall.prompt || 'Input';
}

/**
 * Check if code has any input() calls
 */
export function hasInputCalls(code: string): boolean {
  return /input\s*\(/.test(code);
}

/**
 * Get total count of input() calls
 */
export function getInputCount(code: string): number {
  const matches = code.match(/input\s*\(/g);
  return matches ? matches.length : 0;
}

/**
 * Format the console output to show interactive-style input/output
 */
export function formatInteractiveOutput(
  prompts: string[],
  userInputs: string[],
  finalOutput: string
): string {
  const lines: string[] = [];

  // Add prompts and inputs in order
  for (let i = 0; i < Math.max(prompts.length, userInputs.length); i++) {
    if (i < prompts.length) {
      lines.push(prompts[i]);
    }
    if (i < userInputs.length) {
      lines.push(userInputs[i]);
    }
  }

  // Add final output
  if (finalOutput.trim()) {
    lines.push(finalOutput);
  }

  return lines.join('\n');
}

/**
 * Remove echoed input prompts from backend stdout to avoid duplicate prompt text
 */
export function stripInputPromptsFromOutput(serverOutput: string, prompts: string[]): string {
  let cleaned = (serverOutput || "").trim();
  for (const prompt of prompts) {
    if (!prompt) continue;
    const idx = cleaned.indexOf(prompt);
    if (idx !== -1) {
      cleaned = cleaned.slice(0, idx) + cleaned.slice(idx + prompt.length);
    }
  }

  // Normalize whitespace
  cleaned = cleaned.replace(/^\s+|\s+$/g, "");
  return cleaned;
}

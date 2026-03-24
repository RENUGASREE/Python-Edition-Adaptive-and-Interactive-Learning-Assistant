/**
 * Enhanced console output formatter
 * Makes Python console output look more like a real terminal
 */

export interface FormattedOutput {
  lines: Array<{
    text: string;
    type: 'prompt' | 'output' | 'input' | 'error';
    className: string;
  }>;
}

/**
 * Format Python code execution output to show in terminal style
 * Detects prompts and separates them from outputs
 */
export function formatConsoleOutput(output: string): FormattedOutput {
  const lines: FormattedOutput['lines'] = [];
  const outputLines = output.split('\n');
  
  for (const line of outputLines) {
    if (!line.trim()) {
      lines.push({
        text: '',
        type: 'output',
        className: 'text-gray-600',
      });
      continue;
    }

    // Detect prompt patterns (lines ending with : or ?)
    const isPrompt = /^.+:\s*$/.test(line) || /^.+\?\s*$/.test(line);
    const isError = line.toLowerCase().includes('error') || line.toLowerCase().includes('traceback');

    if (isError) {
      lines.push({
        text: line,
        type: 'error',
        className: 'text-red-400 font-semibold',
      });
    } else if (isPrompt) {
      lines.push({
        text: line,
        type: 'prompt',
        className: 'text-yellow-300 font-semibold',
      });
    } else {
      lines.push({
        text: line,
        type: 'output',
        className: 'text-green-400',
      });
    }
  }

  return { lines };
}

/**
 * Create a visual representation of the code execution flow
 * showing where input was provided
 */
export function formatWithInputHighlight(
  output: string,
  inputs: string[]
): string {
  if (!inputs.length) {
    return output;
  }

  // Simple approach: track which inputs were used by looking at the output
  const lines = output.split('\n');
  const result: string[] = [];
  
  let inputIndex = 0;
  for (const line of lines) {
    result.push(line);
    
    // If this line looks like a prompt and we have inputs, show the input after it
    if (/^.+:\s*$/.test(line) && inputIndex < inputs.length) {
      result.push(inputs[inputIndex]);
      inputIndex++;
    }
  }

  return result.join('\n');
}

/**
 * Get visual formatting instructions based on code
 */
export function getConsoleHelpText(code: string): string {
  const inputCount = (code.match(/input\s*\(/g) || []).length;
  
  if (inputCount === 0) {
    return '✓ This code does not require user input';
  }
  
  return `⚠️  This code expects ${inputCount} input${inputCount > 1 ? 's' : ''}. Provide one value per line in the Input field.`;
}

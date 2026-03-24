/**
 * Utility to parse Python code and detect input() calls
 * to provide better interactive console experience
 */

export interface InputCallInfo {
  line: number;
  prompt: string;
  fullStatement: string;
}

/**
 * Extract all input() calls from Python code
 */
export function detectInputCalls(code: string): InputCallInfo[] {
  const lines = code.split('\n');
  const inputCalls: InputCallInfo[] = [];
  
  // Regex to match input() calls with potential prompt strings
  const inputRegex = /input\s*\(\s*(['"`])(.*?)\1\s*\)/g;
  
  lines.forEach((line, idx) => {
    let match;
    const lineInputRegex = new RegExp(inputRegex);
    
    while ((match = lineInputRegex.exec(line)) !== null) {
      const prompt = match[2];
      inputCalls.push({
        line: idx + 1,
        prompt,
        fullStatement: line.trim(),
      });
    }
  });
  
  return inputCalls;
}

/**
 * Format console output to show as terminal would
 * Separates prompts from user input visually
 */
export function formatTerminalOutput(
  output: string,
  inputLines: string[],
  prompts: string[]
): string {
  const lines = output.split('\n');
  let inputIdx = 0;
  let result = '';
  
  for (const line of lines) {
    // Check if this line looks like a prompt
    const isPrompt = prompts.some(p => line.includes(p));
    
    if (isPrompt && inputIdx < inputLines.length) {
      result += `${line}\n`;
      result += `${inputLines[inputIdx]}\n`;
      inputIdx++;
    } else {
      result += `${line}\n`;
    }
  }
  
  return result.trim();
}

/**
 * Generate helpful message about expected inputs
 */
export function getInputInstructions(inputCount: number): string {
  if (inputCount === 0) {
    return '';
  }
  return `Code expects ${inputCount} input(s). Provide one value per line.`;
}

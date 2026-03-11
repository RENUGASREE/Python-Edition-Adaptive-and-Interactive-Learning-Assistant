import React, { useState } from 'react';
import SimpleCodeEditor from 'react-simple-code-editor';
import { highlight, languages } from 'prismjs';
import 'prismjs/components/prism-python';
import 'prismjs/themes/prism-dark.css'; // Or any other theme

interface EditorProps {
  code: string;
  onChange: (code: string) => void;
  disabled?: boolean;
}

export function Editor({ code, onChange, disabled }: EditorProps) {
  return (
    <div className="relative font-mono text-sm bg-[#1e1e1e] rounded-xl overflow-hidden border border-border shadow-inner min-h-[300px]">
      <div className="absolute top-0 left-0 right-0 bg-[#252526] px-4 py-2 text-xs text-muted-foreground border-b border-border flex items-center justify-between">
        <span>main.py</span>
        <span className="text-[10px] uppercase tracking-wider opacity-60">Python 3.10</span>
      </div>
      <div className="pt-10 h-full overflow-auto">
        <SimpleCodeEditor
          value={code}
          onValueChange={onChange}
          highlight={code => highlight(code, languages.python, 'python')}
          padding={16}
          disabled={disabled}
          className="font-code min-h-[300px]"
          style={{
            fontFamily: '"JetBrains Mono", monospace',
            fontSize: 14,
            backgroundColor: 'transparent',
            color: '#d4d4d4'
          }}
          textareaClassName="focus:outline-none"
        />
      </div>
    </div>
  );
}

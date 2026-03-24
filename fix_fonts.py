#!/usr/bin/env python3
"""Fix external resource loading errors in index.html"""

html_file = "client/index.html"

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Add error handler and fallback styles to Google Fonts link
if 'onerror' not in html:
    # Add the onerror handler
    html = html.replace(
        'display=swap" rel="stylesheet">',
        'display=swap" rel="stylesheet" onerror="console.warn(\'Fonts unavailable\')">'
    )
    
    # Add fallback fonts as a style tag before the Google Fonts link
    fallback_styles = '''    <style>
      /* Fallback fonts if external fonts fail to load */
      :root {
        --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        --font-mono: 'Courier New', Courier, monospace;
      }
      body { font-family: var(--font-sans); }
      code, pre { font-family: var(--font-mono); }
    </style>
    '''
    
    html = html.replace(
        '<link href="https://fonts.googleapis.com',
        fallback_styles + '<link href="https://fonts.googleapis.com'
    )

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("✓ Fixed index.html - added fallback fonts and error handler")

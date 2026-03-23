"""Auto-format plain text into styled HTML based on category."""
import re
import html


def is_plain_text(text):
    """Check if text is plain (not already HTML)."""
    return not bool(re.search(r'<(p|h[1-6]|div|blockquote|ul|ol|section|pre)\b', text))


def format_plain_text(text, category_slug=None):
    """Convert plain text to beautifully formatted HTML.

    Rules:
    - ```language ... ``` → syntax-highlighted code blocks
    - Lines starting with # → h2 headings
    - Lines starting with ## → h3 subheadings
    - Lines starting with > → blockquote
    - Lines starting with - or * → list items
    - Lines starting with Sanskrit:/English:/Meaning: → styled definition blocks
    - Lines with emoji prefixes → styled section headers
    - Empty lines → paragraph breaks
    - **text** → bold
    - *text* → italic
    - `text` → inline code
    """
    if not is_plain_text(text):
        return text

    # Step 1: Extract code blocks FIRST (protect them from other formatting)
    code_blocks = []
    code_placeholder = '\x00CODE_BLOCK_{}\x00'

    def replace_code_block(match):
        lang = match.group(1) or 'text'
        code = match.group(2).strip()
        idx = len(code_blocks)
        code_blocks.append((lang.strip(), code))
        return code_placeholder.format(idx)

    # Match ```language\n...\n```
    text = re.sub(r'```(\w*)\n(.*?)```', replace_code_block, text, flags=re.DOTALL)

    lines = text.strip().split('\n')
    html_parts = []
    in_list = False
    in_blockquote = False
    current_paragraph = []

    def flush_paragraph():
        if current_paragraph:
            content = ' '.join(current_paragraph)
            content = apply_inline_formatting(content)
            html_parts.append(f'<p>{content}</p>')
            current_paragraph.clear()

    def close_list():
        nonlocal in_list
        if in_list:
            html_parts.append('</ul>')
            in_list = False

    def close_blockquote():
        nonlocal in_blockquote
        if in_blockquote:
            html_parts.append('</blockquote>')
            in_blockquote = False

    for line in lines:
        stripped = line.strip()

        # Check if this line is a code block placeholder
        code_match = re.match(r'\x00CODE_BLOCK_(\d+)\x00', stripped)
        if code_match:
            flush_paragraph()
            close_list()
            close_blockquote()
            idx = int(code_match.group(1))
            lang, code = code_blocks[idx]
            escaped_code = html.escape(code)
            highlighted = syntax_highlight(escaped_code, lang)
            html_parts.append(
                f'<div class="code-block">'
                f'<div class="code-header">'
                f'<span class="code-lang">{lang}</span>'
                f'<button class="code-copy-btn" onclick="copyCode(this)">Copy</button>'
                f'</div>'
                f'<pre><code class="language-{lang}">{highlighted}</code></pre>'
                f'</div>'
            )
            continue

        # Empty line
        if not stripped:
            flush_paragraph()
            close_list()
            close_blockquote()
            continue

        # Horizontal divider
        if stripped == '---':
            flush_paragraph()
            close_list()
            close_blockquote()
            html_parts.append('<hr class="cosmic-divider">')
            continue

        # Emoji section headers
        emoji_header = re.match(r'^([\U0001F4DC\U0001F9E0\U0001F4FF\U0001F30D\u26A1\U0001F525\U0001F4A1\u2757\U0001F531\u2638\u2728\U0001F310\u26AB\u26AA\U0001F7E2\U0001F535]+)\s*(.+)', stripped)
        if emoji_header:
            flush_paragraph()
            close_list()
            close_blockquote()
            emoji, title = emoji_header.groups()
            title = title.strip()
            if title.startswith(('# ', '## ')):
                title = title.lstrip('#').strip()
            html_parts.append(f'<h2 class="section-header"><span class="header-emoji">{emoji}</span> {apply_inline_formatting(title)}</h2>')
            continue

        # Headings
        if stripped.startswith('### '):
            flush_paragraph()
            close_list()
            close_blockquote()
            content = apply_inline_formatting(stripped[4:])
            html_parts.append(f'<h4>{content}</h4>')
            continue
        if stripped.startswith('## '):
            flush_paragraph()
            close_list()
            close_blockquote()
            content = apply_inline_formatting(stripped[3:])
            html_parts.append(f'<h3>{content}</h3>')
            continue
        if stripped.startswith('# '):
            flush_paragraph()
            close_list()
            close_blockquote()
            content = apply_inline_formatting(stripped[2:])
            html_parts.append(f'<h2>{content}</h2>')
            continue

        # Sanskrit / English / Meaning blocks
        label_match = re.match(r'^(Sanskrit|English\s*(?:Meaning)?|Meaning|Hindi|Translation)\s*:\s*(.*)$', stripped, re.IGNORECASE)
        if label_match:
            flush_paragraph()
            close_list()
            close_blockquote()
            label, content = label_match.groups()
            label = label.strip()
            content = apply_inline_formatting(content.strip())
            if label.lower() == 'sanskrit':
                html_parts.append(f'<div class="sanskrit-block"><span class="block-label">{label}:</span> <span class="sanskrit-text">{content}</span></div>')
            else:
                html_parts.append(f'<div class="meaning-block"><span class="block-label">{label}:</span> {content}</div>')
            continue

        # Blockquote
        if stripped.startswith('> ') or stripped.startswith('\U0001F449 '):
            flush_paragraph()
            close_list()
            prefix_len = 2 if stripped.startswith('> ') else 3
            content = apply_inline_formatting(stripped[prefix_len:])
            if not in_blockquote:
                html_parts.append('<blockquote class="insight-quote">')
                in_blockquote = True
            html_parts.append(f'<p>{content}</p>')
            continue
        elif in_blockquote:
            close_blockquote()

        # List items
        list_match = re.match(r'^[\-\*\u2022]\s+(.+)', stripped)
        numbered_match = re.match(r'^\d+[\.\)]\s+(.+)', stripped)
        if list_match or numbered_match:
            flush_paragraph()
            close_blockquote()
            content = (list_match or numbered_match).group(1)
            content = apply_inline_formatting(content)
            if not in_list:
                html_parts.append('<ul class="styled-list">')
                in_list = True
            html_parts.append(f'<li>{content}</li>')
            continue
        elif in_list:
            close_list()

        # Regular paragraph line
        current_paragraph.append(stripped)

    # Flush remaining
    flush_paragraph()
    close_list()
    close_blockquote()

    return '\n'.join(html_parts)


def apply_inline_formatting(text):
    """Apply inline markdown-like formatting."""
    # Bold: **text** or __text__
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
    # Italic: *text* or _text_
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    # Inline code: `text`
    text = re.sub(r'`(.+?)`', r'<code class="inline-code">\1</code>', text)
    # Highlight: ==text==
    text = re.sub(r'==(.+?)==', r'<mark>\1</mark>', text)
    return text


def syntax_highlight(escaped_code, lang):
    """Apply basic syntax highlighting with CSS classes."""
    if lang not in ('python', 'py', 'javascript', 'js', 'sql', 'bash', 'shell', 'java', 'scala', 'yaml'):
        return escaped_code

    # Python keywords
    if lang in ('python', 'py'):
        keywords = r'\b(from|import|def|class|return|if|elif|else|for|while|try|except|finally|with|as|in|not|and|or|is|True|False|None|yield|lambda|pass|break|continue|raise|global|nonlocal|assert|del|async|await)\b'
        decorators = r'(@\w+)'
        strings = r'((&quot;{3}|&#x27;{3}).*?(\2)|(f?&quot;.*?&quot;|f?&#x27;.*?&#x27;))'
        comments = r'(#.*?)$'

        # Comments first (highest priority)
        escaped_code = re.sub(comments, r'<span class="hl-comment">\1</span>', escaped_code, flags=re.MULTILINE)
        # Strings
        escaped_code = re.sub(strings, r'<span class="hl-string">\1</span>', escaped_code)
        # Decorators
        escaped_code = re.sub(decorators, r'<span class="hl-decorator">\1</span>', escaped_code)
        # Keywords
        escaped_code = re.sub(keywords, r'<span class="hl-keyword">\1</span>', escaped_code)
        # Functions after def/class
        escaped_code = re.sub(r'(def\s+)(\w+)', r'\1<span class="hl-function">\2</span>', escaped_code)
        escaped_code = re.sub(r'(class\s+)(\w+)', r'\1<span class="hl-function">\2</span>', escaped_code)

    elif lang in ('sql',):
        keywords = r'\b(SELECT|FROM|WHERE|INSERT|INTO|UPDATE|SET|DELETE|CREATE|DROP|ALTER|TABLE|INDEX|JOIN|LEFT|RIGHT|INNER|OUTER|ON|AND|OR|NOT|IN|LIKE|BETWEEN|ORDER|BY|GROUP|HAVING|LIMIT|OFFSET|AS|DISTINCT|COUNT|SUM|AVG|MAX|MIN|UNION|ALL|EXISTS|CASE|WHEN|THEN|ELSE|END|NULL|IS|VALUES|PRIMARY|KEY|FOREIGN|REFERENCES|CASCADE)\b'
        escaped_code = re.sub(keywords, r'<span class="hl-keyword">\1</span>', escaped_code, flags=re.IGNORECASE)

    elif lang in ('bash', 'shell'):
        keywords = r'\b(sudo|apt|pip|npm|cd|ls|mkdir|rm|cp|mv|echo|cat|grep|awk|sed|chmod|chown|export|source|curl|wget|git|docker|python|node)\b'
        escaped_code = re.sub(keywords, r'<span class="hl-keyword">\1</span>', escaped_code)
        comments = r'(#.*?)$'
        escaped_code = re.sub(comments, r'<span class="hl-comment">\1</span>', escaped_code, flags=re.MULTILINE)

    return escaped_code

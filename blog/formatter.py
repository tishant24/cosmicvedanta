"""Auto-format plain text into styled HTML based on category."""
import re


def is_plain_text(text):
    """Check if text is plain (not already HTML)."""
    return not bool(re.search(r'<(p|h[1-6]|div|blockquote|ul|ol|section)\b', text))


def format_plain_text(text, category_slug=None):
    """Convert plain text to beautifully formatted HTML.

    Rules:
    - Lines starting with # → h2 headings
    - Lines starting with ## → h3 subheadings
    - Lines starting with > → blockquote
    - Lines starting with - or * → list items
    - Lines starting with Sanskrit:/English:/Meaning: → styled definition blocks
    - Lines with emoji prefixes (📜🧠📿🌍⚡🔥💡❗) → styled section headers
    - Empty lines → paragraph breaks
    - **text** → bold
    - *text* → italic
    - Text between --- → horizontal divider
    """
    if not is_plain_text(text):
        return text

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

        # Empty line — flush paragraph
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
        emoji_header = re.match(r'^([📜🧠📿🌍⚡🔥💡❗🔱☸✨🌐⚫⚪🟢🔵]+)\s*(.+)', stripped)
        if emoji_header:
            flush_paragraph()
            close_list()
            close_blockquote()
            emoji, title = emoji_header.groups()
            # Clean up special markers
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
        if stripped.startswith('> ') or stripped.startswith('👉 '):
            flush_paragraph()
            close_list()
            prefix = '> ' if stripped.startswith('> ') else '👉 '
            content = apply_inline_formatting(stripped[len(prefix):])
            if not in_blockquote:
                html_parts.append('<blockquote class="insight-quote">')
                in_blockquote = True
            html_parts.append(f'<p>{content}</p>')
            continue
        elif in_blockquote:
            close_blockquote()

        # List items
        list_match = re.match(r'^[\-\*•]\s+(.+)', stripped)
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
    # Italic: *text* or _text_ (but not inside bold)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    # Inline code: `text`
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    # Highlight: ==text==
    text = re.sub(r'==(.+?)==', r'<mark>\1</mark>', text)
    return text

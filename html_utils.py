import re
import html

def clean_html(raw_html):
    """Removes HTML tags and decodes HTML entities for clean text output."""
    if not raw_html:
        return ""

    # Unescape HTML entities (e.g., &#39; to ')
    text = html.unescape(raw_html)

    # Replace <br> and <p> with newlines for readability
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</p>\s*<p>', '\n\n', text, flags=re.IGNORECASE)

    # Remove all remaining HTML tags
    cleanr = re.compile('<.*?>', re.DOTALL)
    cleantext = re.sub(cleanr, '', text)

    return cleantext.strip()

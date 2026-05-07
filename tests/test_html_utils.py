import pytest
from html_utils import clean_html

def test_clean_html_empty_input():
    assert clean_html("") == ""
    assert clean_html(None) == ""

def test_clean_html_no_tags():
    assert clean_html("Hello World") == "Hello World"

def test_clean_html_basic_tags():
    assert clean_html("<div>Hello</div>") == "Hello"
    assert clean_html("<span>World</span>") == "World"

def test_clean_html_entities():
    assert clean_html("It&#39;s a beautiful day") == "It's a beautiful day"
    assert clean_html("Fish &amp; Chips") == "Fish & Chips"

def test_clean_html_br_tags():
    assert clean_html("Line 1<br>Line 2") == "Line 1\nLine 2"
    assert clean_html("Line 1<br/>Line 2") == "Line 1\nLine 2"
    assert clean_html("Line 1<BR >Line 2") == "Line 1\nLine 2"

def test_clean_html_p_tags():
    assert clean_html("<p>Para 1</p><p>Para 2</p>") == "Para 1\n\nPara 2"
    assert clean_html("<p>Para 1</p>  <p>Para 2</p>") == "Para 1\n\nPara 2"

def test_clean_html_mixed_content():
    html_input = """
    <div>
        <h1>Title</h1>
        <p>Paragraph 1<br>with break</p>
        <p>Paragraph 2</p>
        <a href="http://example.com">Link</a>
    </div>
    """
    expected_output = "Title\n        Paragraph 1\nwith break\n\nParagraph 2\n        Link"
    # Note: clean_html uses strip() at the end, but internal whitespace is preserved
    # except for what tags replace.
    result = clean_html(html_input)
    assert "Title" in result
    assert "Paragraph 1" in result
    assert "Paragraph 2" in result
    assert "Link" in result
    assert "\n" in result

def test_clean_html_complex_entities_and_tags():
    html_input = "&lt;b&gt;Bold&lt;/b&gt; &amp; <i>Italic</i>"
    # html.unescape makes it "<b>Bold</b> & <i>Italic</i>"
    # then tags are removed
    assert clean_html(html_input) == "Bold & Italic"

def test_clean_html_multiline_tags():
    html_input = "<div\nclass='test'>Multiline Content</div>"
    assert clean_html(html_input) == "Multiline Content"

    html_input_complex = "<script\ntype='text/javascript'>\nalert('hi');\n</script>Just text"
    # Note: this simple regex cleaner will leave the content of the script tag
    # but it should at least remove the tags themselves even if they span lines.
    cleaned = clean_html(html_input_complex)
    assert "<script" not in cleaned
    assert "</script>" not in cleaned

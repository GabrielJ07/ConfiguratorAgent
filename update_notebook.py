import json

filepath = 'Convert_MyActivity_to_Markdown.ipynb'
with open(filepath, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        new_source = []
        skip = False
        for i, line in enumerate(source):
            if 'def extract_response(item):' in line:
                new_source.append(line)
                new_source.append(source[i+1]) # docstring
                new_source.append("    safe_html_items = item.get('safeHtmlItem', [])\n")
                new_source.append("    response_parts = [html_item['html'] for html_item in safe_html_items if 'html' in html_item]\n")
                new_source.append("    response_html = \"\\n\".join(response_parts)\n")
                new_source.append("    if response_parts:\n")
                new_source.append("        response_html += \"\\n\"\n")
                skip = True
                continue
            if skip:
                if 'return clean_html(response_html)' in line:
                    new_source.append("\n")
                    new_source.append(line)
                    skip = False
                continue
            new_source.append(line)
        cell['source'] = new_source

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)
    f.write('\n')

import re
src = open('app.py', encoding='utf-8').read()

def replacer(match):
    html_str = match.group('html')
    # Replace any ${...} (where not preceded by {) with ${{...}}
    new_html = re.sub(r'(?<!\{)\$\{([^}]+)\}', r'${{\1}}', html_str)
    return f'f"""{new_html}"""'

new_src = re.sub(r'f"""(?P<html>.*?)"""', replacer, src, flags=re.DOTALL)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_src)

print("Fixed ${ escapes in app.py")

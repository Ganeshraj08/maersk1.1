import re
src = open('app.py', encoding='utf-8').read()
html_matches = re.finditer(r'f"""(?P<html>.*?)"""', src, re.DOTALL)
for m in html_matches:
    html_str = m.group('html')
    # search for bare ${ that are not ${{
    bare_dollar = re.findall(r'(?<!\{)\$\{', html_str)
    if bare_dollar:
        print("FOUND BARE DOLLAR PARENS: ", bare_dollar)
    else:
        print("All ${ references are correctly escaped with double braces in this HTML block.")

src = open('app.py', encoding='utf-8').read()
src = src.replace('${{{', '${{').replace('}}}', '}}')
open('app.py', 'w', encoding='utf-8').write(src)
print('Fixed triple braces')

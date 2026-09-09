from parsers import hebrew
heb, _ = hebrew.load('data/morphhb/wlc')
jud = [k for k in heb.keys() if k[0] == 'JUD']
print(f'Chaves JUD em hebraico parser: {len(jud)}')
if jud:
    print('Primeiro:', jud[0])

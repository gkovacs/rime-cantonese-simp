import opencc

converter = opencc.OpenCC('t2s.json')

entry_list = []
entry_to_freq = {}
outfile_essay = open('essay-cantonese-simp.txt', 'wt')
for line in open('essay-cantonese.txt', 'rt'):
  entry,freq = line.split('\t')
  entry = converter.convert(entry)
  for c in entry:
    if c in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,./:;':
      continue
  if entry not in entry_to_freq:
    entry_list.append(entry)
    entry_to_freq[entry] = 0
  entry_to_freq[entry] += int(freq)
for entry in entry_list:
  freq = entry_to_freq[entry]
  print(entry + '\t' + str(freq), file=outfile_essay)

outfile = open('jyut6ping3_nospaces.dict.yaml', 'wt')
outfile_simp = open('jyut6ping3_simp_nospaces.dict.yaml', 'wt')
outfile_withspaces_simp = open('jyut6ping3_simp.dict.yaml', 'wt')

print('''
---
name: jyut6ping3_nospaces
version: "2022.03.17"
sort: by_weight
vocabulary: essay-cantonese
...
''', file=outfile)

print('''
---
name: jyut6ping3_simp_nospaces
version: "2022.03.17"
sort: by_weight
vocabulary: essay-cantonese-simp
...
''', file=outfile_simp)

print('''
---
name: jyut6ping3_simp
version: "2022.03.17"
sort: by_weight
vocabulary: essay-cantonese-simp
...
''', file=outfile_withspaces_simp)

for filebase in ['jyut6ping3.chars', 'jyut6ping3.chars', 'jyut6ping3.words', 'jyut6ping3.phrase', 'jyut6ping3.maps']:
  in_header = True
  for line in open(f'{filebase}.dict.yaml'):
    line = line.strip()
    if line == '...':
      in_header = False
      continue
    if in_header:
      continue
    if line == '':
      continue
    if '\t' not in line:
      continue
    line_parts = line.split('\t')
    for c in line_parts[1]:
      if c in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,./:;':
        continue
    line_simp = converter.convert(line)
    print(line_simp, file=outfile_withspaces_simp)
    line_parts[1] = line_parts[1].replace(' ', '')
    print('\t'.join(line_parts), file=outfile)
    line_parts[0] = converter.convert(line_parts[0])
    print('\t'.join(line_parts), file=outfile_simp)

import opencc

converter = opencc.OpenCC('t2s.json')

entry_list = []
entry_to_freq = {}
tradsimp_entry_list = []
tradsimp_entry_to_freq = {}
outfile_essay_tradsimp = open('essay-cantonese-tradsimp.txt', 'wt')
outfile_essay = open('essay-cantonese-simp.txt', 'wt')
for line in open('essay-cantonese.txt', 'rt'):
  entry,freq = line.split('\t')
  entry_orig = entry
  entry = converter.convert(entry)
  for c in entry:
    if c in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,./:;':
      continue
  if entry not in entry_to_freq:
    entry_list.append(entry)
    entry_to_freq[entry] = 0
  entry_to_freq[entry] += int(freq)
  if entry_orig not in tradsimp_entry_to_freq:
    tradsimp_entry_list.append(entry_orig)
    tradsimp_entry_to_freq[entry_orig] = 0
  tradsimp_entry_to_freq[entry_orig] += int(freq)
  if entry != entry_orig:
    if entry not in tradsimp_entry_to_freq:
      tradsimp_entry_list.append(entry)
      tradsimp_entry_to_freq[entry] = 0
    tradsimp_entry_to_freq[entry] += int(freq)
for entry in entry_list:
  freq = entry_to_freq[entry]
  print(entry + '\t' + str(freq), file=outfile_essay)
for entry in tradsimp_entry_list:
  freq = tradsimp_entry_to_freq[entry]
  print(entry + '\t' + str(freq), file=outfile_essay_tradsimp)


outfile = open('jyut6ping3_nospaces.dict.yaml', 'wt')
outfile_simp = open('jyut6ping3_simp_nospaces.dict.yaml', 'wt')
outfile_tradsimp = open('jyut6ping3_tradsimp_nospaces.dict.yaml', 'wt')
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
name: jyut6ping3_tradsimp_nospaces
version: "2022.03.17"
sort: by_weight
vocabulary: essay-cantonese-tradsimp
...
''', file=outfile_tradsimp)

print('''
---
name: jyut6ping3_simp
version: "2022.03.17"
sort: by_weight
vocabulary: essay-cantonese-simp
...
''', file=outfile_withspaces_simp)

trad_to_pinyin_to_percent = {}
simp_to_pinyin_to_percent = {}

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
    if len(line_parts) >= 3:
      trad,pinyin,freq = line_parts
      freq = float(freq.replace('%', ''))
    elif len(line_parts) == 2:
      trad,pinyin = line_parts
      freq = 100
    else:
      continue
    simp = converter.convert(trad)
    if trad not in trad_to_pinyin_to_percent:
      trad_to_pinyin_to_percent[trad] = {}
    if pinyin not in trad_to_pinyin_to_percent[trad]:
      trad_to_pinyin_to_percent[trad][pinyin] = 0
    trad_to_pinyin_to_percent[trad][pinyin] = max(trad_to_pinyin_to_percent[trad][pinyin], freq)
    if simp not in simp_to_pinyin_to_percent:
      simp_to_pinyin_to_percent[simp] = {}
    if pinyin not in simp_to_pinyin_to_percent[simp]:
      simp_to_pinyin_to_percent[simp][pinyin] = 0
    simp_to_pinyin_to_percent[simp][pinyin] = max(simp_to_pinyin_to_percent[simp][pinyin], freq)

for trad,pinyin_to_percent in trad_to_pinyin_to_percent.items():
  for pinyin,percent in pinyin_to_percent.items():
    pinyin_nospaces = pinyin.replace(' ', '')
    print(f'{trad}\t{pinyin_nospaces}\t{percent}%', file=outfile)

for simp,pinyin_to_percent in simp_to_pinyin_to_percent.items():
  for pinyin,percent in pinyin_to_percent.items():
    pinyin_nospaces = pinyin.replace(' ', '')
    print(f'{simp}\t{pinyin}\t{percent}%', file=outfile_withspaces_simp)
    print(f'{simp}\t{pinyin_nospaces}\t{percent}%', file=outfile_simp)

for trad in (set(trad_to_pinyin_to_percent.keys()) | set(simp_to_pinyin_to_percent.keys())):
  pinyin_to_percent = {}
  for pinyin,percent in trad_to_pinyin_to_percent.get(trad, {}).items():
    if pinyin not in pinyin_to_percent:
      pinyin_to_percent[pinyin] = 0
    pinyin_to_percent[pinyin] = max(pinyin_to_percent[pinyin], percent)
  for pinyin,percent in simp_to_pinyin_to_percent.get(trad, {}).items():
    if pinyin not in pinyin_to_percent:
      pinyin_to_percent[pinyin] = 0
    pinyin_to_percent[pinyin] = max(pinyin_to_percent[pinyin], percent)
  for pinyin,percent in pinyin_to_percent.items():
    print(f'{trad}\t{pinyin}\t{percent}%', file=outfile_tradsimp)

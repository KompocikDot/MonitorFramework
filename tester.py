listastara = [{'t': 1}, {'t': 2}, {'t': 3}]
listanowa = [{'t': 1}, {'t': 2}]

added = [x for x in listanowa if x not in listastara]
removed = [x for x in listastara if x not in listanowa]
# for x in listanowa:
#      if x in listastara:
#           print(x, 'jest')
if added:
     print("Ma nowe elementy", added)

if removed:
     print("Ma usuniete elementy", removed)
# else:
#      print("Nie ma", dif)
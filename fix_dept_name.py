with open('d:/downloaf/the-supply-room/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

target = 'g.fillText("The " + flickerr.department + " Fund", tx, 470);'
replacement = '''let deptName = (flickerr.department || 'The Mutual Fun').trim();
      if (!deptName.toUpperCase().includes('FUND') && !deptName.toUpperCase().includes('MUTUAL')) {
        deptName = deptName + ' Fund';
      }
      g.fillText(deptName.toUpperCase(), tx, 470);'''

if target in c:
    c = c.replace(target, replacement)
    with open('d:/downloaf/the-supply-room/index.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("SUCCESS")
else:
    print("TARGET NOT FOUND")

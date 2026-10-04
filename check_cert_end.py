with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('function renderEngravedCertificate()')
end = text.find('window.addEventListener(', start)

print('Start:', start, 'End:', end)
if start != -1 and end != -1:
    print('Tail of function:\n', text[end-300:end])

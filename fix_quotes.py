with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the join string that has conflicting single quotes
bad_token = "font-family:'Cinzel',serif;"
good_token = "font-family:Cinzel,serif;"

if bad_token in text:
    text = text.replace(bad_token, good_token)
    print("Replaced single quotes inside Cinzel font-family successfully")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open(r'C:\Users\faizan\.gemini\antigravity\brain\ce014d9d-f09e-4a92-b7cf-58ca3be8d0d3\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Files saved cleanly")

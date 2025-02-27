import sys
import re

def unorderedList(text : str):
    lines = text.split('\n')
    started = False
    newLines = []

    for line in lines:
        if line == '' : continue
        match = re.match(r'^-\s+(.+)',line)
        if match:
            if not started:
                newLines.append('<ul>')
                started = True
            newLines.append(f'<li>{match.group(1)}</li>')
        else:
            if started:
                newLines.append('</ul>')
                started = False
            newLines.append(line)
    if started:
        newLines.append('</ul>')

    return '\n'.join(newLines)

def orderedList(text : str) -> str:
    lines = text.split('\n')
    started = False
    newLines = []
    for line in lines:
        if line == '': continue
        match = re.match(r'\s*(\d+)\.\s*(.+)', line)
        if match:
            if not started:
                newLines.append("<ol>")
                started = True
            newLines.append(f"<li>{match.group(2)}</li>")
        else:
            if started:
                newLines.append("</ol>")
                started = False
            newLines.append(line)
    if started:
        newLines.append("</ol>")
    return '\n'.join(newLines)

def enter(text:str) -> str:
    return re.sub(r'\\\n',r'\n<br>\n',text)

def bold(text:str) -> str:
    return re.sub(r'\*\*(.*?|\n*?)\*\*',r'<b>\1</b>',text)

def italic(text:str) -> str:
    return re.sub(r'\*(.*?|\n+)\*',r'<i>\1</i>',text)

def links(text:str) -> str:
    return re.sub(r'\[(.*?)\]\((.*?)\)',r'<a href="\2">\1</a>',text,flags=re.MULTILINE)

def images(text:str)->str:
    return re.sub(r'(!\[(.*?)\]\((.*?)\))',r'<img src="\3" alt="\2"/>',text,flags=re.MULTILINE)

def headers(text : str) -> str:
    html = re.sub(r'(#{1,6})\s*(.*)', 
                       lambda match: f'<h{len(match.group(1))}>{match.group(2)}</h{len(match.group(1))}>', 
                       text, 
                       flags=re.MULTILINE)
    return html

def main(filename:str):

    with open(filename,"r") as md:
        sys.stdin = md
        text = ""
        for a in sys.stdin:
            text += a
        with open(filename.split(".")[0] + ".html","w") as html:
            sys.stdout = html
            sys.stdout.write(headers(links(images(italic(bold(enter(orderedList(unorderedList(text)))))))))

    

if __name__ == '__main__':
    main(sys.argv[1])
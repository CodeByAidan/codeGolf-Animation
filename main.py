import itertools
import sys
from keyword import kwlist as python_keywords

from PIL import Image, ImageFont, ImageDraw, ImageChops, GifImagePlugin

versions = [version.strip() for version in (
    """
    def t(b):
     L=len;w,n=L(b[0])+3,-1;b=list("@"*w+"@@".join(b)+"@"*w);w+=n;I=b.index
     for i in range(L(b)):
      c=b[i];d={"^":-w,"<":n,">":1,"v":w}.get(c)
      if d:
       while c!='@':
        i+=d;c=b[i]
        if c=='*':b[i]='.'
        elif c in "123456789":i+=I(c)-i or I(c,i+1)-i
        elif c in '/\\\\':d={-w:n,w:1,1:w,n:-w}[d]*(-1 if c=='/' else 1)
     return "*" not in b
    """,
    """
    def t(b):
     L=len;w=L(b[0])+3;b=list("@"*w+"@@".join(b)+"@"*w);w-=1;I=b.index
     for i in range(L(b)):
      c=b[i];d={"^":-w,"<":-1,">":1,"v":w}.get(c)
      if d:
       while c!='@':
        i+=d;c=b[i]
        if c=='*':b[i]='.'
        elif c in "123456789":i+=I(c)-i or I(c,i+1)-i
        elif c in '/\\\\':d={-w:-1,w:1,1:w,-1:-w}[d]*(-1 if c=='/' else 1)
     return "*" not in b
    """,
    """
    def t(b):
     L=len;w=L(b[0])+3;b=list("@"*w+"@@".join(b)+"@"*w);w-=1;I=b.index
     for i in range(L(b)):
      c=b[i];d={"^":-w,"<":-1,">":1,"v":w}.get(c)
      if d:
       while c!='@':
        i+=d;c=b[i]
        if c=='*':b[i]='.'
        elif c in '/\\\\':d={-w:-1,w:1,1:w,-1:-w}[d]*(-1 if c=='/' else 1)
        elif c>'0':i+=I(c)-i or I(c,i+1)-i
     return "*" not in b
    """,
    """
    def t(b):
     w=len(b[0])+2;B=list('@'*w+'@@'.join(b)+'@'*w);l=len(B);C="<>v^";D=[-1,1,w,-w];i=0
     while i<l:
        d=C.find(B[i])
        if-1<d:
         j=i;n=l*4
         while('@'!=B[j])*n:
            c=B[j]
            if'+'>c:B[j]=''
            if'/'==c:d=(d+2)%4
            if'\\\\'==c:d=3-d
            if c.isdigit():j=(B*2).index(c,j+1)%l
            j+=D[d];n-=1
        i+=1
     return'*'not in B
    """,
    """
    def t(b):
     w=len(b[0])+2;B=list('@'*w+'@@'.join(b)+'@'*w);l=len(B);i=0
     while i<l:
        d="<>v^".find(B[i])
        if-1<d:
         j=i;n=l*4
         while(B[j]!='@')*n:
            c=B[j]
            if'+'>c:B[j]=''
            if'/'==c:d=(d+2)%4
            if'\\\\'==c:d=3-d
            if c.isdigit():j=(B*2).index(c,j+1)%l
            j+=[-1,1,w,-w][d];n-=1
        i+=1
     return'*'not in B
    """,
    """
    def t(b):
     w=len(b[0])+2;B=list('@'*w+'@@'.join(b)+'@'*w);l=len(B);i=0
     while i<l:
        d="<>v^".find(B[i])
        if-1<d:
         j=i;c='.'
         while c not in"@<>v^":
            if'+'>c:B[j]=''
            if'/'==c:d^=2
            if'\\\\'==c:d^=3
            elif'0'<c:j=(B*2).index(c,j+1)%l
            j+=[-1,1,w,-w][d];c=B[j]
        i+=1
     return'*'not in B
    """,
    """
    def t(b):
     w=len(b[0])+2;B=list('@'*w+'@@'.join(b)+'@'*w);l=len(B);i=0
     while i<l:
        d="<>v^".find(B[i]);j=i;c='.'
        while c not in"@<>v^":
         if'+'>c:B[j]=''
         if'/'==c:d^=2
         if'\\\\'==c:d^=3
         elif'0'<c:j=(B*2).index(c,j+1)%l
         j+=[-1,1,w,-w,-i][d];c=B[j]
        i+=1
     return'*'not in B
    """,
    """
    def t(b):
     w=len(b[0])+1;B=list('@'*w+'@'.join(b)+'@'*w);l=len(B);i=0
     while i<l:
        d="<>v^".find(B[i]);j=i;c='.'
        while c not in"@<>v^":
         if'+'>c:B[j]=''
         if'/'==c:d^=2
         if'\\\\'==c:d^=3
         elif'0'<c:j=(B*2).index(c,j+1)%l
         j+=[-1,1,w,-w,-j][d];c=B[j]
        i+=1
     return'*'not in B
    """,
    """
    def t(b):
     w=len(b[0])+1;B=list('@'*w+'@'.join(b));i=l=len(B);C="<>^v@"
     while i:
        j=l-i;i-=1;d=C.find(B[j]);c='.'
        while c not in C:
         if'+'>c:B[j]='.'
         if'0'<c<C:j=(B*2).index(c,j+1)%l
         elif'.'<c:d^=2+(c<C)
         j-=[1,-1,w,-w,j][d];c=B[j%l]
     return'*'not in B
    """,
    """
    def t(b):
     w=len(b[0])+1;B=list('@'*w+'@'.join(b));i=l=len(B);C="<>^v@"
     while i:
      i-=1;d,j,c=C.find(B[i]),i,'.'
      while(c in C)-1:
       if'+'>c:B[j]='.'
       if'0'<c<C:j=(B*2).index(c,j+1)%l
       elif'.'<c:d^=2+(c<C)
       j-=[1,-1,w,-w,j][d];c=B[j%l]
     return('*'in B)-1
    """)]


def ndiff(src, dest):
    src_len, dest_len = len(src), len(dest)
    d = {(-1, -1): -1}
    for i in range(src_len):
        d[i, -1] = i
    for j in range(dest_len):
        d[-1, j] = j
    for i, j in itertools.product(range(src_len), range(dest_len)):
        d[i, j] = min(
            d[i - 1, j] + 1,
            d[i, j - 1] + 1,
            d[i - 1, j - 1] + (src[i] != dest[j]))
    path = 'S'
    while i or j:
        i, j, s = min(
            (i - 1, j, 'D'),
            (i, j - 1, 'I'),
            (i - 1, j - 1, 'S'),
            key=lambda i_j_s: d.get((i_j_s[0], i_j_s[1]), sys.maxsize))
        path += s
    src_ofs = dest_ofs = 0
    for i, s in enumerate(path[::-1]):
        c, d = src[i + src_ofs], dest[i + dest_ofs]
        if s == 'D':
            dest_ofs -= 1
            yield '-', c
        elif s == 'S':
            if c == d:
                yield ' ', d
            else:
                yield '-', c
                yield '+', d
        else:
            src_ofs -= 1
            yield '+', d


width = max(len(line) for version in versions for line in version.split("\n"))
height = max(len(version.split("\n")) for version in versions)

font = ImageFont.truetype(r"C:\Users\aidan\Downloads\OsakaMono.ttf", 15)
em, lineheight = 9, 14
anim_frames = 1

theme = {
    "identifier": "blue",
    "keyword": "black",
    "string": "maroon",
    "number": "magenta",
    "punctuation": "gray",
    "whitespace": None,
}


def clike_highlighter(src, keywords, theme=theme):
    import string
    x = y = i = 0
    out = []

    def emit(stop, typ):
        color = theme.get(typ, "black")
        # print ("(%s \"%s\" %s)" % (typ, src[start:stop].replace("\n","¶"), color))
        for c in src[start:stop]:
            out.append((c, color))

    while i < len(src):
        start = i
        ch = src[i]
        if ch in "\'\"":
            while True:
                i += 1
                if src[i] == '\\':
                    i += 1
                elif src[i] == ch:
                    i += 1
                    emit(i, "string")
                    break
        elif ch in string.punctuation:
            i += 1
            emit(i, "punctuation")
        elif ch in string.whitespace:
            i += 1
            emit(i, "whitespace")
        elif ch in string.digits:
            while True:
                i += 1
                if i == len(src) or (src[i] not in string.digits and src[i] not in "e."):
                    emit(i, "number")
                    break
        else:
            while True:
                i += 1
                if i == len(src) or src[i] in "\'\"" or src[i] in string.punctuation or src[i] in string.whitespace:
                    emit(i, "keyword" if src[start:i] in keywords else "identifier")
                    break
    return out


versions = [clike_highlighter(version, python_keywords) for version in versions]


def render(text, ofs, diff, diff_ch, label):
    frames = []
    for frame in range(anim_frames if ofs is not None else 1):
        image = Image.new("RGB", (width * em + int(em * 1.5), height * lineheight + int(lineheight / 2)), "white")
        frames.append(image)
        draw = ImageDraw.Draw(image)
        x, y = 0, 0
        for i, (ch, color) in enumerate(text):
            if ch == '\n':
                x = 0
                y += lineheight
            else:
                if i == ofs:
                    draw.rectangle((x, y, x + em, y + lineheight),
                                   fill='red' if diff == '+' else 'blue')
                    scale = 1.0 / 3 * frame
                    if diff == '-':
                        scale = 1.0 - scale
                    draw.text((x, y), ch, font=font,
                              fill='yellow')
                    draw.rectangle((x + em, y, x + em + em, y + lineheight),
                                   fill='white')
                    x += int(round(float(em) * scale))
                if color:
                    draw.text((x, y), ch, font=font, fill=color)
                x += em
        if label:
            label = str(label)
            x = width * em - len(label) * em
            draw.rectangle((x, 0, width * em, lineheight), fill='yellow')
            draw.text((x, 0), label, font=font, fill='red')
        del draw
    return frames


def compute_frames(prev, curr):
    adjust = 0
    for ofs, diff in enumerate(ndiff(prev, curr)):
        diff, ch = diff[0], diff[-1]
        if diff in "+-":
            yield prev, ofs - adjust, diff, ch
            if diff == "+":
                prev = prev[:ofs - adjust] + [ch] + prev[ofs - adjust:]
            else:
                assert prev[ofs - adjust] == ch, (ofs, prev[:ofs + 1], ch)
                prev = prev[:ofs - adjust] + prev[ofs - adjust + 1:]
                adjust += 1
    assert prev == curr, ["%d= %s != %s" % (i, prev[i].replace('\n', '¶').replace(' ', '¢'),
                                            curr[i].replace('\n', '¶').replace(' ', '¢')) for i in
                          range(min(len(prev), len(curr))) if prev[i] != curr[i]]


frames = render(versions[0], None, None, None, len(versions[0]))

prev = versions[0]
for i in range(3, len(versions)):
    curr = versions[i]
    print("==== %d (%d %d) ====" % (i, len(curr), len(prev) - len(curr)))
    for frame in compute_frames(prev, curr):
        frames += render(*frame, label="%d -> %d" % (len(prev), len(curr)))
frames += render(versions[-1], None, None, None, len(versions[-1]))

frames = frames[:2000]

with open("anim.gif", "wb") as f:
    prev = None
    for frame in frames:
        frame = frame.convert('P', palette=Image.WEB)
        if not prev:
            for s in GifImagePlugin.getheader(frame)[0]:
                f.write(s)
            prev = frame.copy()
            frame = GifImagePlugin.getdata(frame)
        else:
            delta = ImageChops.subtract_modulo(frame, prev)
            prev = frame.copy()
            if bbox := delta.getbbox():
                frame = GifImagePlugin.getdata(frame.crop(bbox), offset=bbox[:2])
            else:
                continue
        for s in frame:
            f.write(s)
    f.write(b";")

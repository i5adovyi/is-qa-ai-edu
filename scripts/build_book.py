"""Optional PDF publisher. Requires reportlab; portal and labs do not."""
import json
import re
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted, KeepTogether
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/pdf/ai-engineering-fieldbook.pdf'
INK=colors.HexColor('#172820'); GREEN=colors.HexColor('#d5edb6'); MUTED=colors.HexColor('#61715f')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BookTitle',fontName='Times-Roman',fontSize=43,leading=47,textColor=INK,spaceAfter=25))
styles.add(ParagraphStyle(name='Chapter',fontName='Times-Roman',fontSize=27,leading=32,textColor=INK,spaceAfter=19,keepWithNext=True))
styles.add(ParagraphStyle(name='Section',fontName='Times-Roman',fontSize=17,leading=21,textColor=INK,spaceBefore=17,spaceAfter=9,keepWithNext=True))
styles.add(ParagraphStyle(name='Subsection',fontName='Helvetica-Bold',fontSize=11,leading=15,textColor=INK,spaceBefore=12,spaceAfter=7,keepWithNext=True))
styles.add(ParagraphStyle(name='Prose',fontName='Helvetica',fontSize=9.8,leading=15,textColor=INK,spaceAfter=9))
styles.add(ParagraphStyle(name='SmallText',parent=styles['Prose'],fontSize=8,leading=11))
styles.add(ParagraphStyle(name='BulletText',parent=styles['Prose'],leftIndent=12,firstLineIndent=-8,spaceAfter=6))
styles.add(ParagraphStyle(name='Mono',fontName='Courier',fontSize=7.2,leading=10,textColor=INK,backColor=colors.HexColor('#eef2e7'),borderPadding=9,spaceBefore=7,spaceAfter=12))

def clean(s):
    replacements={'→':'->','←':'<-','↗':'','✓':'yes','×':'x','—':' - ','–':'-','’':"'",'‘':"'",'“':'"','”':'"','…':'...','≥':'>=','≤':'<=','≈':'~','∈':'in','δ':'delta','μ':'mu','σ':'sigma','🎯':'','🤗':'','├':'|','└':'|','─':'-','│':'|','•':'-'}
    for a,b in replacements.items():s=s.replace(a,b)
    return s.encode('latin-1',errors='replace').decode('latin-1')

def fmt(s):
    s=escape(clean(s))
    s=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',lambda m:f'<link href="{m.group(2)}" color="#436b31">{m.group(1)}</link>',s)
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',s)
    s=re.sub(r'`([^`]+)`',r'<font name="Courier">\1</font>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
    return s

def markdown(text):
    lines=text.splitlines();flow=[];para=[];code=False;buf=[]
    def flush():
        if para:flow.append(Paragraph(fmt(' '.join(para)),styles['Prose']));para.clear()
    i=0
    while i<len(lines):
        l=lines[i];i+=1
        if l.startswith('```'):
            flush()
            if code:
                wrapped=[]
                for row in buf:wrapped.extend(textwrap.wrap(clean(row),width=100,replace_whitespace=False,drop_whitespace=False) or [''])
                flow.append(Preformatted('\n'.join(wrapped),styles['Mono']));buf=[]
            code=not code;continue
        if code:buf.append(l);continue
        if l.lstrip().startswith('|') and i<len(lines) and re.match(r'\s*\|?\s*:?-{3}',lines[i]):
            flush();rows=[l];i+=1
            while i<len(lines) and lines[i].lstrip().startswith('|'):rows.append(lines[i]);i+=1
            cells=[[Paragraph(fmt(c.strip()),styles['SmallText']) for c in row.strip().strip('|').split('|')] for row in rows]
            width=(A4[0]-100)/len(cells[0]);t=Table(cells,colWidths=[width]*len(cells[0]),repeatRows=1,hAlign='LEFT')
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),GREEN),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.3,colors.HexColor('#ccd6c4')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]));flow.extend([t,Spacer(1,12)]);continue
        h=re.match(r'^(#{1,6})\s+(.+)',l)
        if h:flush();flow.append(Paragraph(fmt(h[2]),styles['Chapter' if len(h[1])==1 else 'Section' if len(h[1])==2 else 'Subsection']));continue
        if not l.strip():flush();continue
        if l.strip()=='---':flush();continue
        m=re.match(r'^\s*(?:[-*]|\d+\.)\s+(.+)',l)
        if m:flush();flow.append(Paragraph('- '+fmt(m[1]),styles['BulletText']));continue
        para.append(l.lstrip('> '))
    flush();return flow

class Book(BaseDocTemplate):
    def __init__(self,path):
        super().__init__(str(path),pagesize=A4,leftMargin=50,rightMargin=50,topMargin=56,bottomMargin=51,title='AI Engineering Fieldbook',author='AI Engineering Academy')
        self.addPageTemplates(PageTemplate(id='normal',frames=Frame(50,51,A4[0]-100,A4[1]-107,id='body',leftPadding=0,bottomPadding=0,rightPadding=0,topPadding=0),onPage=self.decorate))
    def decorate(self,c,doc):
        c.setStrokeColor(colors.HexColor('#dce3d5'));c.line(50,34,A4[0]-50,34)
        c.setFillColor(MUTED);c.setFont('Helvetica',8);c.drawString(50,22,'AI ENGINEERING ACADEMY  /  FIELD EDITION 2026');c.drawRightString(A4[0]-50,22,str(doc.page))
        if doc.page>1:c.setFont('Helvetica',7);c.drawString(50,A4[1]-30,'LEARN THE CONCEPTS. BUILD THE SYSTEM. SHOW THE EVIDENCE.')
    def afterFlowable(self,f):
        if isinstance(f,Paragraph) and f.style.name=='Chapter':
            text=f.getPlainText();key='chapter-'+str(self.seq.nextf('chapter'));self.canv.bookmarkPage(key);self.canv.addOutlineEntry(text,key,0,False);self.notify('TOCEntry',(0,text,self.page,key))

def build():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    story=[Spacer(1,85),Paragraph('FIELD PROGRAM / OCTOBER 2026',styles['Subsection']),Spacer(1,25),Paragraph('AI Engineering<br/>Fieldbook',styles['BookTitle']),Paragraph('From deliberate prompting to reliable agent systems',styles['Section']),Spacer(1,28),Paragraph('24 lessons. 72 lesson exercises. 11 labs. Eight stages of deliberate practice.',styles['Prose']),Paragraph('Context engineering - tools and skills - agentic development - harnesses - evaluation - delegation - production',styles['Prose']),Spacer(1,50),Paragraph('An original companion to the Signal Desk practice project. Read with a terminal, an experiment log, and a willingness to test your assumptions.',styles['Prose']),Paragraph('External courses, books, and videos are linked for independent study. Their content is not reproduced here. Completion is a personal learning record, not an accredited qualification.',styles['SmallText']),PageBreak(),Paragraph('Contents',styles['Chapter'])]
    toc=TableOfContents();toc.levelStyles=[ParagraphStyle(name='TOC',fontName='Helvetica',fontSize=9,leading=13,spaceBefore=5,leftIndent=0,firstLineIndent=0)];story.extend([toc,PageBreak()])
    curriculum=json.loads((ROOT/'content/curriculum.json').read_text())
    paths=[ROOT/'docs/START-HERE.md',ROOT/'docs/ASSESSMENT.md',ROOT/'docs/GLOSSARY.md',ROOT/'docs/STUDY-PLAN.md',ROOT/'docs/OPERATING-PLAYBOOK.md',ROOT/'docs/PRACTICE-MAP.md',ROOT/'docs/INTEGRATION-LABS.md',ROOT/'lab/model-bridge.md',ROOT/'content/dev-sandbox/README.md',ROOT/'content/research/README.md',ROOT/'content/research/worked-example.md']+[ROOT/l['file'] for l in curriculum['lessons']]+sorted((ROOT/'content/labs').glob('[0-9]*.md'))+[ROOT/'lab/mcp_lab/README.md',ROOT/'lab/mcp_lab/solutions.md',ROOT/'content/skill-practice/HOST-EVIDENCE.md']+sorted((ROOT/'content/articles').glob('*.md'))+sorted((ROOT/'capstones').glob('*.md'))+sorted((ROOT/'templates').glob('*.md'))+[ROOT/'content/library/README.md',ROOT/'content/library/catalog.md',ROOT/'docs/REUSE.md']
    for p in paths:story.extend(markdown(p.read_text()));story.append(PageBreak())
    Book(OUT).multiBuild(story);print(OUT)
if __name__=='__main__':build()

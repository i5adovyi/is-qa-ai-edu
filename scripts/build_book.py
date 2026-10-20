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
styles.add(ParagraphStyle(name='Prose',fontName='Helvetica',fontSize=9.8,leading=15,textColor=INK,spaceAfter=9,allowWidows=0,allowOrphans=0))
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
    lab_count=len(list((ROOT/'content/labs').glob('[0-9]*.md')))
    story=[Spacer(1,85),Paragraph('FIELD PROGRAM / OCTOBER 2026',styles['Subsection']),Spacer(1,25),Paragraph('AI Engineering<br/>Fieldbook',styles['BookTitle']),Paragraph('From deliberate prompting to reliable agent systems',styles['Section']),Spacer(1,28),Paragraph(f'24 lessons. 72 lesson exercises. {lab_count} labs. Six incidents and a capstone investigation. Eight stages of deliberate practice.',styles['Prose']),Paragraph('Preparation - context - tools and skills - agentic development - harnesses - evaluation - delegation - production',styles['Prose']),Spacer(1,50),Paragraph('An original companion to the Signal Desk practice project. Read with a terminal, an experiment log, and a willingness to test your assumptions.',styles['Prose']),Paragraph('External courses, books, and videos are linked for independent study. Their content is not reproduced here. Completion is a personal learning record, not an accredited qualification.',styles['SmallText']),PageBreak(),Paragraph('Contents',styles['Chapter'])]
    toc=TableOfContents();toc.levelStyles=[ParagraphStyle(name='TOC',fontName='Helvetica',fontSize=9,leading=13,spaceBefore=5,leftIndent=0,firstLineIndent=0)];story.extend([toc,PageBreak()])
    curriculum=json.loads((ROOT/'content/curriculum.json').read_text())
    paths=[ROOT/'docs/SETUP.md',ROOT/'docs/START-HERE.md',ROOT/'docs/ASSESSMENT.md',ROOT/'docs/GLOSSARY.md',ROOT/'docs/STUDY-PLAN.md',ROOT/'docs/OPERATING-PLAYBOOK.md',ROOT/'docs/PRACTICE-MAP.md',ROOT/'docs/INTEGRATION-LABS.md',ROOT/'lab/model-bridge.md',ROOT/'content/dev-sandbox/README.md',ROOT/'content/research/README.md',ROOT/'content/research/worked-example.md']+[ROOT/l['file'] for l in curriculum['lessons']]+sorted((ROOT/'content/labs').glob('[0-9]*.md'))+[ROOT/'lab/mcp_lab/README.md',ROOT/'lab/mcp_lab/solutions.md',ROOT/'content/skill-practice/HOST-EVIDENCE.md']+sorted((ROOT/'content/articles').glob('*.md'))+sorted((ROOT/'capstones').glob('*.md'))+sorted((ROOT/'templates').glob('*.md'))+[ROOT/'content/library/README.md',ROOT/'content/library/catalog.md',ROOT/'docs/REUSE.md']
    additions=[]
    for folder in ['content/onboarding','content/assessment','content/walkthroughs']:
        additions.extend(sorted((ROOT/folder).glob('*.md')))
    additions.extend([ROOT/'docs/FUTURE-PROJECT-READINESS.md',ROOT/'docs/ACCOUNT-MIGRATION.md',ROOT/'docs/CONTINUE-LEARNING.md',ROOT/'lab/planner_lab/README.md'])
    incident_position=paths.index(ROOT/'lab/mcp_lab/README.md')
    incident_paths=[ROOT/'content/incidents/README.md']+sorted((ROOT/'content/incidents').glob('[0-9]*.md'))+[ROOT/'content/incidents/ASSESSMENT.md',ROOT/'lab/incidents/README.md']
    paths[incident_position:incident_position]=incident_paths
    paths=additions+paths
    answer_sections=[]
    for p in paths:
        if not p.exists():continue
        text=p.read_text()
        if p.name == 'solutions.md':
            answer_sections.append(text)
            continue
        # Paper readers get answer guidance in a deliberate appendix, not beside the attempt.
        if p.parent.name=='lessons':
            match=re.search(r'(?ms)^## Hints and solution outline\n(.*?)(?=^## |\Z)',text)
            if match:
                answer_sections.append('# '+text.splitlines()[0].lstrip('# ')+' — guidance\n'+match[1])
                text=text[:match.start()]+'## Hint access\n\nAttempt the exercise first. Guidance is in the final appendix and behind disclosures in the portal.\n\n'+text[match.end():]
        story.extend(markdown(text));story.append(PageBreak())
    learning=json.loads((ROOT/'content/learning.json').read_text())
    story.extend(markdown('# Applied checks\n\nPredict, explain, or inspect a new case. Preserve your attempt before consulting a tutor. These checks supplement the lesson quizzes.\n'))
    for check in learning['checks']:
        story.extend(markdown('## '+check['id']+'\n\n'+check['prompt']+'\n\nReview criteria: '+'; '.join(check['criteria'])))
    story.append(PageBreak())
    # Incident guidance stays out of this static student book altogether. Unlike
    # the portal/CLI, a PDF cannot condition disclosure on a saved attempt.
    story.extend(markdown('# Incident guidance access\n\nThe six incident briefs and capstone incident are included above. Incident hints, debriefs, and reference implementations are deliberately omitted from this student fieldbook. Save your hypothesis, evidence, and next check in the portal or terminal exercise, then explicitly request a hint or debrief there. These two attempt records are separate. The editable repository includes guidance for maintenance; this is a learning workflow, not a secure examination.\n'))
    story.append(PageBreak())
    story.extend(markdown('# Guidance appendix — open after your attempt\n\nThese are hints and solution outlines. Return to the exercises if you want to try independently first.\n'))
    story.append(PageBreak())
    for section in answer_sections:
        story.extend(markdown(section));story.append(PageBreak())
    Book(OUT).multiBuild(story);print(OUT)
if __name__=='__main__':build()

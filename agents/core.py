"""Transparent, offline research assistant agents (no API key required)."""
import math
import re
from collections import Counter
from pathlib import Path

STOP = set('a an the is are was were to of in on for and or with from by as at that this it be can how what which do does into their its using use we our about'.split())

def sentences(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n+', text) if len(s.strip()) >= 25]

def tokens(text):
    return [w for w in re.findall(r'[a-z0-9]+', text.lower()) if w not in STOP and len(w)>2]

class SearchAgent:
    def run(self, question, documents, top_k=6):
        q=set(tokens(question))
        candidates=[]
        for name, content in documents.items():
            for i, sentence in enumerate(sentences(content)):
                st=set(tokens(sentence))
                overlap=len(q & st)
                if overlap:
                    score=overlap / math.sqrt(max(1,len(q))*max(1,len(st)))
                    candidates.append({'source':name,'sentence':sentence,'score':round(score,4),'index':i})
        return sorted(candidates,key=lambda x:x['score'],reverse=True)[:top_k]

class SummaryAgent:
    def run(self, evidence):
        if not evidence:
            return 'No relevant evidence found in the uploaded documents.'
        return ' '.join(f"{item['sentence']} [{item['source']}]" for item in evidence[:3])

class VerificationAgent:
    def run(self, evidence):
        if not evidence:
            return {'status':'Insufficient evidence','note':'No matching passages were found. Do not treat this as a factual answer.'}
        sources=len(set(x['source'] for x in evidence))
        return {'status':'Evidence found','note':f'{len(evidence)} matching passages from {sources} document(s). Matches indicate relevance, not independent fact-checking.'}

class ReportAgent:
    def run(self, question, evidence, summary, verification):
        lines=[f'# Research report\n',f'**Question:** {question}\n',f'## Evidence-based summary\n{summary}\n',f"## Verification\n**{verification['status']}** — {verification['note']}\n",'## Source passages\n']
        lines.extend(f"- **{e['source']}** (relevance {e['score']:.2f}): {e['sentence']}" for e in evidence)
        lines.append('\n## Limitations\nThis tool searches only the provided files, uses lexical similarity, and cannot independently verify scientific truth or discover live papers. Review original publications before citing.')
        return '\n'.join(lines)

def run_pipeline(question,documents):
    evidence=SearchAgent().run(question,documents)
    summary=SummaryAgent().run(evidence)
    verification=VerificationAgent().run(evidence)
    report=ReportAgent().run(question,evidence,summary,verification)
    return {'evidence':evidence,'summary':summary,'verification':verification,'report':report}

def load_demo():
    folder=Path(__file__).resolve().parents[1]/'data'
    return {p.name:p.read_text(encoding='utf-8') for p in folder.glob('*.txt')}

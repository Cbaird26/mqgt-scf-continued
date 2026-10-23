"""Regenerate the editorial guide. Uses Arial on macOS, Helvetica otherwise.
The delivered guide PDF is the canonical input for exact corpus page preservation.
"""
from pathlib import Path
import json,re,html
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
P=Path(__file__).resolve().parents[1]
font='Helvetica';bold='Helvetica-Bold'
fp=Path('/System/Library/Fonts/Supplemental')
if (fp/'Arial.ttf').exists():
 pdfmetrics.registerFont(TTFont('Arial',str(fp/'Arial.ttf')));pdfmetrics.registerFont(TTFont('ArialB',str(fp/'Arial Bold.ttf')));font='Arial';bold='ArialB'
ink=colors.HexColor('#193342');accent=colors.HexColor('#167987');muted=colors.HexColor('#526470');pale=colors.HexColor('#EAF2F3')
s=getSampleStyleSheet()
styles={
'body':ParagraphStyle('body',fontName=font,fontSize=10,leading=14,textColor=ink,spaceAfter=8),
'small':ParagraphStyle('small',fontName=font,fontSize=8.2,leading=11,textColor=ink,spaceAfter=4),
'head':ParagraphStyle('head',fontName=bold,fontSize=20,leading=24,textColor=ink,spaceAfter=15),
'sub':ParagraphStyle('sub',fontName=bold,fontSize=11.5,leading=15,textColor=accent,spaceBefore=12,spaceAfter=6),
'cover':ParagraphStyle('cover',fontName=bold,fontSize=32,leading=36,textColor=ink,spaceAfter=16),
'kicker':ParagraphStyle('kicker',fontName=bold,fontSize=9,leading=13,textColor=accent,spaceAfter=14),
'cell':ParagraphStyle('cell',fontName=font,fontSize=8.4,leading=11,textColor=ink),
'cellb':ParagraphStyle('cellb',fontName=bold,fontSize=8.4,leading=11,textColor=ink),
}
def para(t,style='body'):return Paragraph(t,styles[style])
def table(headers,rows,widths):
 data=[[para(html.escape(str(x)),'cellb') for x in headers]]+[[para(html.escape(str(x)),'cell') for x in row] for row in rows]
 t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),pale),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.8,accent),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#D3DFE3')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]));return t
cat=json.loads((P/'CATALOG_NEW_WORK.json').read_text());story=[]
def add(t,style='body'):story.append(para(t,style))
def newpage(title):story.append(PageBreak());add(title,'head')
add('BAIRD / ZORAASI  ·  RESEARCH ARCHIVE  ·  EDITION 2026.10.22','kicker')
add('A Theory of Everything<br/>Updated research corpus','cover')
add('Exact mode sums, coupled vacuum, radion mixing<br/>and finite-momentum stability','sub')
add('Prepared for Christopher Michael Baird<br/>AI-assisted curation and editorial assembly','body')
story.append(Spacer(1,14))
story.append(table(['Reading edition','New material','Preserved baseline'],[['9,447 pages','51 source PDFs / 189 pages','9,252 pages from the published 2026.10.20 edition']],[160,160,179]))
story.append(Spacer(1,18))
add('Current result to read first','sub')
add('The minimal retained spectral action has tachyonic poles with negative residues and additional non-real poles under the specified direct Lorentzian continuation. Earlier positive static curvatures and two-derivative kinetic tests do not establish a stable vacuum. The new corpus makes that qualification visible before the historical material.')
add('How to navigate','sub')
add('Pages 1-6: update guide and catalogue.<br/>Pages 7-96: nine theory and continuation notes.<br/>Pages 97-9348: complete prior public corpus.<br/>Pages 9349-9447: recent computational mathematics and status records.')
add('The package retains original research files, all seven GitHub prerelease bundles, complete caveats, source hashes and portable assembly tools. The prior public ZIP remains intact as an archival component.')
add('Local preparation only. No new Zenodo DOI or publication is created by this package.','small')
newpage('What the latest work establishes')
add('Read the sequence as a record of conditional results and corrections. The source PDFs retain their historical wording; this guide identifies their present scope.')
rows=[('Common stationary profiles','Finite local spectral data do not select a unique exact gauge response for every allowed profile family. This is an existence result, not ambiguity for every prescribed dataset.'),('Weak, neutral and scalar completion','Geometric weak response and neutral matching are followed by a declared microscopic scalar/anomaly sector. Its local scalar estimates are subsequently replaced by exact internal mode-sum calculations within the retained model.'),('Exact coupled vacuum','The untuned action is unstable. Selected mass and flatness terms yield restricted tuned branches with positive static curvatures. Those inputs are not predictions or a solution of the cosmological constant problem.'),('Radion and finite momentum','The two-derivative metric is positive in the tested fixtures. The later full-momentum quadratic operator exposes tachyonic and complex poles. The representative radion-connected squared parameter shifts from about 0.8296 to 0.6565 in cutoff units; it is not a certified particle of a completed theory.')]
story.append(table(['Stage','Current interpretation'],rows,[120,379]))
add('Limits that remain active','sub')
add('The finite-momentum calculation uses the declared warped family, a closed neutral scalar/metric sector and the transverse-traceless graviton. Charged/phase constraints, higher compactification modes and tadpoles, additional allowed operators and a causal quantum prescription remain unresolved. Bounded floating-point pole searches are not global or interval certificates.')
add('No measured coupling is fitted. The measured fine-structure constant remains unexplained. Neither the archived calculations nor this packaging establish a completed or experimentally validated Theory of Everything.')
add('The full release notes and extracted assumptions/review records are included in the archive. See CLAIM_STATUS.md for a more detailed supersession map.','small')
newpage('Theory and continuation catalogue')
add('Physical page numbers below refer to this 9,447-page reading edition. IDs map to original filenames, hashes and sources in CATALOG_NEW_WORK.json and CATALOG_NEW_WORK.csv.','small')
short=['Six-route research continuation','Common-vacuum spectral-profile theorem','Geometric weak-gauge response','Neutral gauge and Higgs matching','Microscopic scalar and anomaly sector','Exact scalar mode sums and Higgs kinetics','Exact coupled scalar/radius vacuum','Radion kinetics and scalar mixing','Finite-momentum metric/radion/scalar poles']
story.append(table(['ID','Work','Pages'],[[x['id'],name,f"{x['corpus_start']}-{x['corpus_end']}"] for x,name in zip(cat[:9],short)],[45,380,74]))
add('Source status','sub')
add('N001, N002 and N005-N009 are published GitHub research prereleases. Their 26 original assets, metadata and release descriptions are retained. N003 and N004 are recovered local PDF notes; standalone code bundles for those two notes were not located.')
add('The 21 October checkpoint includes shared-action, thermal, public-count, electromagnetic, ultraviolet and synthetic-memory routes. Its public experimental data reanalysis is distinct from the original authors\' work; the synthetic-memory exercise is not an experience measurement.')
add('The chronology is scientific, not a claim that every note has the same publication date. The finite-momentum release was published on 23 October UTC / 22 October America/New_York. Its preparation date remains 22 October.','small')
for half in range(2):
 newpage('Mathematics and status catalogue'+(' / 2' if half else ' / 1'))
 add('Forty-two distinct PDFs cover fourteen finite Hadamard orders. Reports and status boards are retained as archive records; no matrices are independently recalculated in this edition.','small')
 rows=[]
 for x in cat[9+21*half:9+21*(half+1)]:
  n=x['source_filename'];order=re.search(r'(?:Hadamard_|hadamard_)(\d+)',n)[1];kind='Status board' if n.startswith('STATUS') else 'Scoreboard' if n.startswith('SCORE') else 'Construction report'
  date=re.search(r'2026-10-(\d+)',n)[1]
  rows.append([x['id'],f'Oct {date} / {order}',kind,f"{x['corpus_start']}-{x['corpus_end']}"])
 story.append(table(['ID','Date / order','Record','Pages'],rows,[43,119,252,85]))
 add('Byte-identical PDF copies are removed; distinct historical status snapshots remain. Available JSON, text and Markdown sidecars are included with their provenance. Full-conjecture, new-order and physical-validation claims are not inferred from these reports.','small')
newpage('Package, provenance and reuse')
add('Reproducibility','sub')
add('The public ZIP contains the updated reading corpus, this guide, catalogues and page maps; the original 2026.10.20 package; all seven later release distributions; the two intervening PDFs; recent mathematics records; complete caveats; prepared Zenodo metadata; and assembly/verification tools.')
add('Run <font name="Courier">python3 08_Rebuild/verify_package.py</font> from the extracted root, or use the SHA256SUMS.txt manifest. Rebuild the reading PDF with <font name="Courier">08_Rebuild/rebuild_corpus.py</font> and an output path outside the package. Each research bundle retains its own scientific reproduction instructions.')
add('Verification boundary','sub')
add('Source checksums, ZIP integrity, PDF syntax, page content/geometry, navigation and a fresh portable rebuild are checked during packaging. The final VERIFICATION.json records the executed checks and the visual sample. Scientific suites are not rerun, and their recorded checks are not summed as independent physical evidence.')
add('Lineage and attribution','sub')
add('Previous public edition: <link href="https://doi.org/10.5281/zenodo.23524358" color="#167987">10.5281/zenodo.23524358</link>.<br/>Existing concept: 10.5281/zenodo.14019809.<br/>Latest included GitHub tag: v2026.10.22-finite-momentum-poles.<br/>Pinned source: c0e36ad13a8da384c2b8c25463dae01022c12e46.','small')
add('The historical corpus retains Jennifer Lorraine Nielsen\'s separately authored 116-page CC BY 4.0 preprint (10.20944/preprints202604.0315.v5). The private 240-page manuscript and personal study guide remain excluded. The public-count input is separately attributed to Pedalino et al. (10.5281/zenodo.17502163); the optional EOS ancillary table is not redistributed.')
add('Component licenses and printed authorship remain authoritative. Inclusion does not imply collaborators\' endorsement or joint authorship of every work. See RIGHTS_AND_ATTRIBUTION.txt and each preserved bundle. AI-assisted assembly does not constitute external peer review.')
add('Coverage','sub')
add('This edition covers the verified public baseline, the seven identified prereleases and the documented recent local sources. It does not claim to contain every cloud-only draft or repository. Full research limitations are preserved in the source notes, release descriptions, CLAIM_STATUS.md and 07_Caveats/.','small')
def decorate(c,doc):
 c.saveState();c.setStrokeColor(accent);c.setLineWidth(.7);c.line(48,754,547,754)
 c.setFont(font,8);c.setFillColor(muted);c.drawString(48,766,'A THEORY OF EVERYTHING  /  CORPUS UPDATE 2026.10.22')
 c.drawString(48,27,'Research archive - conditional results and preserved historical sources');c.drawRightString(547,27,f'{doc.page} / 6');c.restoreState()
out=P/'02_Update_Guide_and_Catalogue_2026-10-22.pdf'
SimpleDocTemplate(str(out),pagesize=(595.28,841.89),rightMargin=48,leftMargin=48,topMargin=103,bottomMargin=49,title='A Theory of Everything - Corpus Update Guide 2026-10-22',author='Christopher Michael Baird; AI-assisted editorial assembly').build(story,onFirstPage=decorate,onLaterPages=decorate)
print(out)

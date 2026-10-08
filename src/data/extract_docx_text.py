"""
Deep inspection of IEEE_PAPER updated.docx and crop recommendation IEEE code full.docx
"""

import zipfile
import xml.etree.ElementTree as ET

def get_text_from_docx(docx_path):
    with zipfile.ZipFile(docx_path) as z:
        xml_content = z.read('word/document.xml')
        tree = ET.fromstring(xml_content)
        paragraphs = []
        for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            texts = [node.text for node in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
            if texts:
                paragraphs.append(''.join(texts))
        return '\n'.join(paragraphs)

with open('reports/scratch_doc_text.txt', 'w', encoding='utf-8') as out:
    for doc in ['docs/IEEE_PAPER updated.docx', 'legacy/crop recommendation IEEE code full.docx']:
        out.write(f"\n{'='*80}\nFILE: {doc}\n{'='*80}\n")
        out.write(get_text_from_docx(doc))
        out.write("\n\n")

print("Saved text to reports/scratch_doc_text.txt")

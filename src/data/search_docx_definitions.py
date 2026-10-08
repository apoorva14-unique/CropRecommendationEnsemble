"""
Extract text and search for feature definitions in docx files.
"""

import os
import zipfile
import xml.etree.ElementTree as ET

def get_text_from_docx(docx_path):
    with zipfile.ZipFile(docx_path) as z:
        xml_content = z.read('word/document.xml')
        tree = ET.fromstring(xml_content)
        # Find all w:t elements
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        paragraphs = []
        for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            texts = [node.text for node in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
            if texts:
                paragraphs.append(''.join(texts))
        return '\n'.join(paragraphs)

for doc in ['docs/IEEE_PAPER updated.docx', 'legacy/crop recommendation IEEE code full.docx']:
    if os.path.exists(doc):
        print(f"\n{'='*80}\nINSPECTING: {doc}\n{'='*80}")
        text = get_text_from_docx(doc)
        print(f"Total lines: {len(text.splitlines())}")
        
        # Search lines containing keywords
        keywords = ['FC', 'BA', 'Field Capacity', 'Iron', 'Boron', 'Barium', 'CU', 'MN', 'ZN', 'EC', 'OC', 'Soil Type', 'Dataset', 'complete soil data', 'Kadapa', 'Andhra']
        for line in text.splitlines():
            line_upper = line.upper()
            if any(k.upper() in line_upper for k in ['FC', 'BA', 'FIELD CAPACITY', 'IRON', 'BORON', 'BARIUM', 'MICRONUTRIENT']):
                print(f"  [MATCH] {line.strip()}")

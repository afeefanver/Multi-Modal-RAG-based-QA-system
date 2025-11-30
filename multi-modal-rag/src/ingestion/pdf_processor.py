import pymupdf
from pathlib import Path
from typing import List, Dict
import re

class MultiModalPDFProcessor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.doc = pymupdf.open(pdf_path)
        
    def extract_text_chunks(self) -> List[Dict]:
        """Extract text with page metadata"""
        chunks = []
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            text = page.get_text()
            
            # Split into paragraphs
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip() and len(p.strip()) > 50]
            
            for para in paragraphs:
                chunks.append({
                    'content': para,
                    'type': 'text',
                    'page': page_num + 1,
                    'metadata': {'source': 'text_extraction'}
                })
        
        print(f"✓ Extracted {len(chunks)} text chunks")
        return chunks
    
    def extract_tables_simple(self) -> List[Dict]:
        """Extract tables using simple text analysis"""
        tables = []
        
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            text = page.get_text()
            
            # Look for table-like structures (multiple lines with tabs or spaces)
            lines = text.split('\n')
            table_lines = []
            in_table = False
            
            for line in lines:
                # Simple heuristic: if line has multiple spaces/tabs, might be table
                if '\t' in line or '  ' in line:
                    table_lines.append(line)
                    in_table = True
                elif in_table and len(table_lines) > 3:
                    # Found end of table
                    table_text = '\n'.join(table_lines)
                    tables.append({
                        'content': table_text,
                        'type': 'table',
                        'page': page_num + 1,
                        'metadata': {
                            'table_id': len(tables),
                            'extraction_method': 'simple'
                        }
                    })
                    table_lines = []
                    in_table = False
                else:
                    if in_table and table_lines:
                        table_text = '\n'.join(table_lines)
                        if len(table_lines) > 3:  # Minimum table size
                            tables.append({
                                'content': table_text,
                                'type': 'table',
                                'page': page_num + 1,
                                'metadata': {
                                    'table_id': len(tables),
                                    'extraction_method': 'simple'
                                }
                            })
                    table_lines = []
                    in_table = False
        
        print(f"✓ Extracted {len(tables)} tables")
        return tables
    
    def process_all(self) -> List[Dict]:
        """Process all modalities"""
        all_chunks = []
        
        print("\n" + "="*50)
        print("Processing PDF Document")
        print("="*50)
        
        print("\n[1/2] Extracting text...")
        all_chunks.extend(self.extract_text_chunks())
        
        print("\n[2/2] Extracting tables...")
        all_chunks.extend(self.extract_tables_simple())
        
        print(f"\n{'='*50}")
        print(f"✓ Total chunks extracted: {len(all_chunks)}")
        print(f"  - Text chunks: {sum(1 for c in all_chunks if c['type'] == 'text')}")
        print(f"  - Table chunks: {sum(1 for c in all_chunks if c['type'] == 'table')}")
        print("="*50 + "\n")
        
        return all_chunks
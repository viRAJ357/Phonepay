import docx
from docx.opc.constants import RELATIONSHIP_TYPE as RT

def get_detailed_info(file_path, output_path):
    doc = docx.Document(file_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("--- PARAGRAPHS ---\n")
        for i, para in enumerate(doc.paragraphs):
            f.write(f"P{i}: {para.text}\n")
            
        f.write("\n--- HYPERLINKS ---\n")
        rels = doc.part.rels
        for rel in rels.values():
            if rel.reltype == RT.HYPERLINK:
                f.write(f"ID: {rel.rId}, Target: {rel._target}\n")

if __name__ == "__main__":
    get_detailed_info(r'C:\Users\nikhi\Downloads\Phone Pe.docx', 'docx_dump.txt')

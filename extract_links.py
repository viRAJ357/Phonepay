import docx
from docx.opc.constants import RELATIONSHIP_TYPE as RT

def get_hyperlinks(file_path):
    doc = docx.Document(file_path)
    links = []
    # Check document relationships
    rels = doc.part.rels
    for rel in rels.values():
        if rel.reltype == RT.HYPERLINK:
            links.append(rel._target)
    
    # Check for hyperlinks in paragraphs (sometimes they are there)
    for para in doc.paragraphs:
        for run in para.runs:
            # docx doesn't directly support getting hyperlinks in runs easily
            pass
            
    return links

if __name__ == "__main__":
    links = get_hyperlinks(r'C:\Users\nikhi\Downloads\Phone Pe.docx')
    print("EXTRACTED_LINKS_START")
    for link in links:
        print(link)
    print("EXTRACTED_LINKS_END")

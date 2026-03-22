import docx
import os

def extract_text(file_path, output_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return
    
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(full_text))
    print(f"Text extracted to {output_path}")

if __name__ == "__main__":
    extract_text(r'C:\Users\nikhi\Downloads\Phone Pe.docx', 'phone_pe_info.txt')

from pypdf2 import PdfReader
import os

def parse_cv(cv_path: str):
    """
    Parses a PDF or TXT resume and returns the text.
    Modified to use PyPDF2 correctly.
    """
    if not os.path.exists(cv_path):
        print(f"[!] Archivo CV no encontrado: {cv_path}")
        return ""
        
    print(f"[*] Parsing CV: {cv_path}")
    
    if cv_path.endswith('.pdf'):
        try:
            reader = PdfReader(cv_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"[!] Error Parsing PDF: {e}")
            return ""
            
    elif cv_path.endswith('.txt'):
        try:
            with open(cv_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"[!] Error Parsing TXT: {e}")
            return ""
    
    return ""

if __name__ == "__main__":
    # Test (requires a dummy file)
    import sys
    if len(sys.argv) > 1:
        print(parse_cv(sys.argv[1])[:500])

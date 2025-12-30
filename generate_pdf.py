from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_pdf(text_file, pdf_file):
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter
    y = height - 40
    
    with open(text_file, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        c.drawString(40, y, line.strip())
        y -= 20
        if y < 40:
            c.showPage()
            y = height - 40
            
    c.save()

if __name__ == "__main__":
    create_pdf('data/dummy_knowledge.txt', 'data/knowledge_base.pdf')

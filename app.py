from flask import Flask, request, jsonify, render_template
import pdfplumber
import spacy
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO, StringIO
import base64

app = Flask(__name__)

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

# List of inappropriate clauses
inappropriate_clauses = [
    "exclusive jurisdiction", "non-compete", "automatic renewal", "one-sided indemnity", "unilateral amendment", 
    "unlimited liability", "non-disparagement", "binding arbitration", "limitation of liability", "non-solicitation", 
    "liquidated damages", "confidentiality without exceptions", "no termination for convenience", "venue selection", 
    "no assignment", "non-transferable", "force majeure without exclusions", "entire agreement clause", "waiver of rights", 
    "severability clause", "waiver of jury trial", "no oral modification", "intellectual property ownership", 
    "termination without cause", "lack of dispute resolution", "no refunds", "mandatory mediation", 
    "no third-party beneficiaries", "survival clause", "right to audit", "governing law clause", "payment upon demand", 
    "unilateral termination", "unilateral renewal", "unilateral change in terms", "liquidated damages clause", 
    "excessive late fees", "unfair penalty clauses", "hidden fees", "unilateral control of IP", "inconsistent terms", 
    "no right to withhold payment", "no warranties", "no guarantees", "restrictive covenants", "one-sided confidentiality", 
    "no liability for data breaches", "no liability for delays", "no liability for loss of profits", 
    "no liability for consequential damages", "no remedy for breach",
    "limitation on indirect damages", "waiver of notice", "exclusivity clause", "non-disclosure agreement", 
    "indemnification clause", "conflict of interest", "dispute resolution clause", "non-payment clause", 
    "conflicting terms", "confidential information", "breach of contract", "force majeure event", 
    "time is of the essence", "assignment clause", "severability provision", "venue and jurisdiction", 
    "survivability provision", "merger clause", "suspension of services", "termination clause", 
    "effective date", "amendment and modification", "entire agreement provision", "no third-party rights", 
    "representations and warranties", "choice of law provision", "good faith clause", "no written amendment", 
    "compliance with laws", "survival provision", "notice provision", "governing law and jurisdiction", 
    "arbitration provision", "non-reliance provision", "notices and communications", "governing jurisdiction", 
    "applicable law", "dispute resolution mechanism", "confidentiality provision", "limitations of liability", 
    "confidentiality obligations", "severability provision", "limitation on liability", "force majeure provision", 
    "no damages for delay", "sole remedy provision", "indemnity provision", "force majeure clause", "remedy provision", 
    "non-disclosure provision", "governing law provision", "arbitration clause", "no oral agreements", 
    "representation and warranty", "choice of venue", "no implied warranties", "exclusivity provision", 
    "binding effect provision", "no modification unless in writing"
]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and file.filename.endswith('.pdf'):
        text = extract_text(file)
        entities = perform_ner(text)
        highlighted_pdf = highlight_clauses(file, text, entities)
        
        # Encode PDF to base64 to send it as a JSON response
        pdf_base64 = base64.b64encode(highlighted_pdf.getvalue()).decode('utf-8')
        
        response = {
            'text': text,
            'entities': entities,
            'highlighted_pdf': pdf_base64
        }
        
        return jsonify(response)

    return jsonify({"error": "Invalid file format"}), 400

def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def perform_ner(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def highlight_clauses(file, text, entities):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)  # Use letter size (8.5 x 11 inches)
    width, height = letter

    c.setFont("Helvetica", 12)

    lines = text.split('\n')
    y = height - 50  # Start from the top of the page

    # Highlight inappropriate clauses and entities
    for line in lines:
        x_start = 50
        x_end = width - 50
        line_width = c.stringWidth(line)
        highlighted = False

        # Check for inappropriate clauses
        for clause in inappropriate_clauses:
            index = line.lower().find(clause.lower())
            if index != -1:
                clause_length = len(clause)
                # Draw non-highlighted part before the clause
                c.drawString(x_start, y, line[:index])
                
                # Draw highlighted clause
                c.setFillColorRGB(1, 0, 0)  # Red color for highlighting
                c.drawString(x_start + c.stringWidth(line[:index]), y, line[index:index + clause_length])
                c.setFillColorRGB(0, 0, 0)  # Reset color
                
                # Draw non-highlighted part after the clause
                c.drawString(x_start + c.stringWidth(line[:index + clause_length]), y, line[index + clause_length:])
                highlighted = True
                break
        
        if not highlighted:
            c.drawString(x_start, y, line)

        y -= 15  # Move to the next line

    # Adding entities at the end of the PDF for better visibility
    y -= 20
    c.drawString(50, y, "Entities found:")
    y -= 15

    for entity in entities:
        c.setFillColorRGB(0, 0, 1)  # Blue color for highlighting entities
        c.drawString(70, y, f"{entity[0]} ({entity[1]})")
        y -= 15

    c.save()
    buffer.seek(0)
    return buffer

if __name__ == '__main__':
    app.run(debug=True)

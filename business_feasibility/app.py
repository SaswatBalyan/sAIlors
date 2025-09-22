from flask import Flask, render_template, request, send_file, make_response
from analysis import analyze_location, generate_detailed_analysis
from data_fetcher import get_nearby_businesses
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
from datetime import datetime

app = Flask(__name__)

# Business type mapping for Google Places API
BUSINESS_TYPE_MAPPING = {
    "restaurant": "restaurant",
    "cafe": "cafe",
    "gym": "gym",
    "pharmacy": "pharmacy",
    "grocery_or_supermarket": "supermarket",
    "bar": "bar",
    "shopping_mall": "shopping_mall",
    "lodging": "lodging",
    "retail_store": "store",
    "beauty_salon": "beauty_salon",
    "clinic": "hospital",
    "bank": "bank"
}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            location = request.form["location"]
            business_type = request.form["business"]
            budget_lakhs = float(request.form["budget"])
            budget_usd = budget_lakhs * 100000 / 83  # Convert INR lakhs to USD (approximate rate)
            extra_notes = request.form.get("extra_notes", "").strip()

            # Get real business data from Google Places API
            google_places_type = BUSINESS_TYPE_MAPPING.get(business_type, business_type)
            nearby_businesses = get_nearby_businesses(location, google_places_type, radius=2000)
            
            # Filter businesses that match the selected type
            filtered_businesses = [
                b for b in nearby_businesses if business_type in b.get("types", []) or google_places_type in b.get("types", [])
            ]

            result = analyze_location(filtered_businesses, business_type, budget_usd, extra_notes, budget_lakhs)
            result["user_location"] = location.split(",")  # [lat, lng]
        except (KeyError, ValueError) as e:
            # Handle missing form fields or invalid data
            result = {
                "error": f"Please fill in all required fields correctly. Error: {str(e)}",
                "feasibility": 0,
                "competition": "Unknown",
                "pros": [],
                "cons": [],
                "market_insights": [],
                "budget_analysis": [],
                "recommendations": [],
                "businesses": [],
                "user_location": ["0", "0"]  # Default location for error cases
            }
    return render_template("index.html", result=result)

@app.route("/download_pdf", methods=["POST"])
def download_pdf():
    """Generate and download detailed PDF analysis"""
    try:
        # Get form data
        location = request.form["location"]
        business_type = request.form["business"]
        budget_lakhs = float(request.form["budget"])
        budget_usd = budget_lakhs * 100000 / 83
        extra_notes = request.form.get("extra_notes", "").strip()
        
        # Get real business data
        google_places_type = BUSINESS_TYPE_MAPPING.get(business_type, business_type)
        nearby_businesses = get_nearby_businesses(location, google_places_type, radius=2000)
        filtered_businesses = [
            b for b in nearby_businesses if business_type in b.get("types", []) or google_places_type in b.get("types", [])
        ]
        
        # Generate detailed analysis for PDF
        detailed_analysis = generate_detailed_analysis(
            filtered_businesses, business_type, budget_usd, extra_notes, budget_lakhs, location
        )
        
        # Create PDF
        pdf_buffer = io.BytesIO()
        create_pdf_report(pdf_buffer, detailed_analysis, location, business_type, budget_lakhs)
        pdf_buffer.seek(0)
        
        # Return PDF as download
        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=business_analysis_{business_type}_{location.replace(",", "_")}.pdf'
        
        return response
        
    except Exception as e:
        return f"Error generating PDF: {str(e)}", 500

def create_pdf_report(buffer, analysis, location, business_type, budget_lakhs):
    """Create a detailed PDF report"""
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,
        textColor=colors.darkblue
    )
    story.append(Paragraph("Business Feasibility Analysis Report", title_style))
    story.append(Spacer(1, 12))
    
    # Report metadata
    meta_style = ParagraphStyle(
        'Meta',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey
    )
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", meta_style))
    story.append(Paragraph(f"Location: {location}", meta_style))
    story.append(Paragraph(f"Business Type: {business_type.title()}", meta_style))
    story.append(Paragraph(f"Budget: ₹{budget_lakhs:.1f} lakhs", meta_style))
    story.append(Spacer(1, 20))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", styles['Heading2']))
    story.append(Paragraph(f"Feasibility Score: {analysis.get('feasibility', 0)}%", styles['Normal']))
    story.append(Paragraph(f"Competition Level: {analysis.get('competition', 'Unknown')}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Advantages
    story.append(Paragraph("Key Advantages", styles['Heading2']))
    for advantage in analysis.get('pros', []):
        story.append(Paragraph(f"• {advantage}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Challenges
    story.append(Paragraph("Key Challenges", styles['Heading2']))
    for challenge in analysis.get('cons', []):
        story.append(Paragraph(f"• {challenge}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Market Analysis
    story.append(Paragraph("Market Analysis", styles['Heading2']))
    for insight in analysis.get('market_insights', []):
        story.append(Paragraph(f"• {insight}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Financial Assessment
    story.append(Paragraph("Financial Assessment", styles['Heading2']))
    for assessment in analysis.get('budget_analysis', []):
        story.append(Paragraph(f"• {assessment}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Strategic Recommendations
    story.append(Paragraph("Strategic Recommendations", styles['Heading2']))
    for recommendation in analysis.get('recommendations', []):
        story.append(Paragraph(f"• {recommendation}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Recommended Business Types
    story.append(Paragraph("Recommended Business Types", styles['Heading2']))
    for business_type in analysis.get('recommended_businesses', []):
        story.append(Paragraph(f"• {business_type}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Competitor Analysis
    if analysis.get('businesses'):
        story.append(Paragraph("Nearby Competitors", styles['Heading2']))
        competitor_data = [['Business Name', 'Location', 'Rating']]
        for business in analysis.get('businesses', [])[:10]:
            parts = business.split(' at ')
            if len(parts) == 2:
                name = parts[0]
                location_info = parts[1]
                competitor_data.append([name, location_info, 'N/A'])
        
        competitor_table = Table(competitor_data)
        competitor_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(competitor_table)
    
    # Detailed Analysis
    if analysis.get('detailed_analysis'):
        story.append(PageBreak())
        story.append(Paragraph("Detailed Analysis", styles['Heading1']))
        story.append(Paragraph(analysis.get('detailed_analysis', ''), styles['Normal']))
    
    doc.build(story)

if __name__ == "__main__":
    app.run(debug=True, port=5001)

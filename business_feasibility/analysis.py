# analysis.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is required. Please set it in your .env file.")

# Configure the API
genai.configure(api_key=api_key)

def analyze_location(business_data, business_type, budget_usd, extra_notes="", budget_lakhs=0):
    """
    Returns detailed feasibility analysis with comprehensive research.
    """
    # Determine competition level
    num_competitors = len(business_data)
    if num_competitors >= 8:
        competition = "High"
        base_feasibility = 25
    elif num_competitors >= 4:
        competition = "Medium"
        base_feasibility = 45
    else:
        competition = "Low"
        base_feasibility = 65

    # Budget-based feasibility adjustment (using INR lakhs)
    budget_multiplier = min(1.2, max(0.7, budget_lakhs / 5))  # Normalize around 5 lakhs
    feasibility = int(base_feasibility * budget_multiplier)
    feasibility = min(95, max(10, feasibility))  # Keep within reasonable bounds

    businesses_list = [
        {
            'name': biz['name'],
            'location': f"{biz['lat']},{biz['lng']}",
            'lat': biz['lat'],
            'lng': biz['lng'],
            'types': ', '.join(biz.get('types', [])),
            'rating': biz.get('rating', 0),
            'price_level': biz.get('price_level', 0),
            'vicinity': biz.get('vicinity', ''),
            'display': f"{biz['name']} ({', '.join(biz.get('types', []))}) at {biz['lat']},{biz['lng']}"
        }
        for biz in business_data
    ]

    # Create comprehensive research prompt
    research_prompt = f"""
You are a business analyst with expertise in market research and feasibility studies. Analyze the following business opportunity with detailed research:

BUSINESS DETAILS:
- Business Type: {business_type}
- Budget: ₹{budget_lakhs:.1f} lakhs (approximately ${budget_usd:,.0f})
- Competition Level: {competition} ({num_competitors} competitors nearby)
- Extra Notes: {extra_notes if extra_notes else "No additional notes provided"}

NEARBY COMPETITORS:
{chr(10).join([biz['display'] for biz in businesses_list]) if businesses_list else "No direct competitors found in the area"}

Please provide a comprehensive analysis including:

1. ADVANTAGES (5-7 points):
   - Market opportunity analysis
   - Location advantages
   - Budget feasibility
   - Target demographic insights
   - Growth potential
   - Operational advantages
   - Any specific advantages based on the extra notes

2. CHALLENGES (5-7 points):
   - Market challenges
   - Competition analysis
   - Budget constraints
   - Location disadvantages
   - Operational challenges
   - Risk factors
   - Any specific concerns based on the extra notes

3. MARKET ANALYSIS:
   - Target demographic analysis
   - Peak hours and seasonal trends
   - Pricing strategy recommendations
   - Marketing approach suggestions

4. FINANCIAL ASSESSMENT:
   - Budget adequacy assessment
   - Key expense categories
   - Revenue projections
   - Break-even timeline

5. STRATEGIC RECOMMENDATIONS:
   - Specific action items
   - Risk mitigation strategies
   - Success factors to focus on
   - Any specific recommendations based on the extra notes

6. RECOMMENDED BUSINESS TYPES:
   - Alternative business types suitable for this location
   - Business types with higher success potential
   - Emerging opportunities in the area
   - Complementary business ideas

IMPORTANT: Format your response with clear headers and use simple bullet points without asterisks, emojis, or special formatting. Be professional and specific in your analysis.
"""

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(research_prompt)
        output_text = response.text.strip()

        # Parse the detailed response
        pros, cons, market_insights, budget_analysis, recommendations, recommended_businesses = parse_detailed_response(output_text)

    except Exception as e:
        print(f"Error generating content: {e}")
        # Fallback to basic analysis
        pros = [
            f"Low competition in the area ({num_competitors} competitors)",
            f"Budget of ₹{budget_lakhs:.1f} lakhs provides good starting capital",
            "Location appears to have good foot traffic potential",
            "Growing market demand for {business_type} services"
        ]
        cons = [
            "Need to conduct more detailed market research",
            "Competition analysis required",
            "Location-specific challenges need assessment",
            "Budget may need adjustment based on actual costs"
        ]
        market_insights = ["Conduct detailed market research to validate assumptions"]
        budget_analysis = [f"Budget of ₹{budget_lakhs:.1f} lakhs should cover initial setup costs"]
        recommendations = ["Start with a pilot program to test the market"]
        recommended_businesses = [
            "Food & Beverage: Coffee shops, juice bars, or healthy food options",
            "Retail: Specialty stores, convenience stores, or local product shops", 
            "Services: Laundry, dry cleaning, or repair services",
            "Healthcare: Pharmacy, medical supplies, or wellness centers",
            "Education: Tutoring centers, skill development, or language classes"
        ]

    return {
        "feasibility": feasibility,
        "competition": competition,
        "pros": pros,
        "cons": cons,
        "market_insights": market_insights,
        "budget_analysis": budget_analysis,
        "recommendations": recommendations,
        "recommended_businesses": recommended_businesses,
        "businesses": businesses_list
    }


def parse_detailed_response(text):
    """Parse the detailed AI response into structured sections"""
    pros = []
    cons = []
    market_insights = []
    budget_analysis = []
    recommendations = []
    recommended_businesses = []
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    current_section = None
    
    for line in lines:
        line_lower = line.lower()
        
        if 'pros' in line_lower or 'advantages' in line_lower:
            current_section = 'pros'
        elif 'cons' in line_lower or 'challenges' in line_lower or 'disadvantages' in line_lower:
            current_section = 'cons'
        elif 'market insights' in line_lower or 'demographic' in line_lower:
            current_section = 'market_insights'
        elif 'budget' in line_lower or 'financial' in line_lower:
            current_section = 'budget_analysis'
        elif 'recommendations' in line_lower or 'action' in line_lower:
            current_section = 'recommendations'
        elif 'recommended business' in line_lower or 'business types' in line_lower:
            current_section = 'recommended_businesses'
        elif line.startswith('-') or line.startswith('•') or line.startswith('*'):
            # Extract bullet point content and clean it
            content = line[1:].strip()
            # Remove any remaining asterisks, emojis, or special formatting
            content = clean_text(content)
            if current_section == 'pros':
                pros.append(content)
            elif current_section == 'cons':
                cons.append(content)
            elif current_section == 'market_insights':
                market_insights.append(content)
            elif current_section == 'budget_analysis':
                budget_analysis.append(content)
            elif current_section == 'recommendations':
                recommendations.append(content)
            elif current_section == 'recommended_businesses':
                recommended_businesses.append(content)
        elif current_section and not any(keyword in line_lower for keyword in ['pros', 'cons', 'market', 'budget', 'recommendations', 'insights', 'analysis', 'business']):
            # Add as content to current section and clean it
            content = clean_text(line)
            if current_section == 'pros':
                pros.append(content)
            elif current_section == 'cons':
                cons.append(content)
            elif current_section == 'market_insights':
                market_insights.append(content)
            elif current_section == 'budget_analysis':
                budget_analysis.append(content)
            elif current_section == 'recommendations':
                recommendations.append(content)
            elif current_section == 'recommended_businesses':
                recommended_businesses.append(content)
    
    # Ensure we have at least some content in each section
    if not pros:
        pros = ["Market research indicates positive potential for this business type"]
    if not cons:
        cons = ["Competition analysis and risk assessment needed"]
    if not market_insights:
        market_insights = ["Conduct detailed demographic and market research"]
    if not budget_analysis:
        budget_analysis = ["Budget appears adequate for initial operations"]
    if not recommendations:
        recommendations = ["Develop a comprehensive business plan"]
    if not recommended_businesses:
        recommended_businesses = [
            "Food & Beverage: Coffee shops, juice bars, or healthy food options",
            "Retail: Specialty stores, convenience stores, or local product shops", 
            "Services: Laundry, dry cleaning, or repair services",
            "Healthcare: Pharmacy, medical supplies, or wellness centers",
            "Education: Tutoring centers, skill development, or language classes"
        ]
    
    return pros, cons, market_insights, budget_analysis, recommendations, recommended_businesses


def clean_text(text):
    """Clean text by removing emojis, asterisks, and special formatting"""
    import re
    
    # Remove emojis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub('', text)
    
    # Remove asterisks and other special characters
    text = re.sub(r'[*•▪▫]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def generate_detailed_analysis(business_data, business_type, budget_usd, extra_notes="", budget_lakhs=0, location=""):
    """
    Generate a comprehensive detailed analysis for PDF reports
    """
    # Get basic analysis first
    basic_analysis = analyze_location(business_data, business_type, budget_usd, extra_notes, budget_lakhs)
    
    # Create comprehensive detailed prompt for PDF
    detailed_prompt = f"""
You are a senior business analyst preparing a comprehensive feasibility report for a potential business investment. Provide an in-depth analysis covering all aspects of this business opportunity.

BUSINESS OPPORTUNITY DETAILS:
- Business Type: {business_type}
- Location: {location}
- Budget: ₹{budget_lakhs:.1f} lakhs (approximately ${budget_usd:,.0f})
- Competition Level: {basic_analysis.get('competition', 'Unknown')} ({len(business_data)} competitors nearby)
- Additional Notes: {extra_notes if extra_notes else "No additional notes provided"}

NEARBY COMPETITORS:
{chr(10).join([f"{biz['name']} (Rating: {biz.get('rating', 'N/A')}, Price Level: {biz.get('price_level', 'N/A')}) at {biz['lat']},{biz['lng']}" for biz in business_data]) if business_data else "No direct competitors found in the area"}

Please provide a comprehensive 2000+ word detailed analysis covering:

1. EXECUTIVE SUMMARY
   - Overall feasibility assessment
   - Key success factors
   - Primary risks and opportunities
   - Investment recommendation

2. MARKET ANALYSIS
   - Target market demographics and size
   - Market trends and growth potential
   - Seasonal variations and peak periods
   - Customer behavior patterns
   - Market saturation analysis

3. COMPETITIVE LANDSCAPE
   - Detailed competitor analysis
   - Market positioning opportunities
   - Competitive advantages and disadvantages
   - Pricing strategy recommendations
   - Differentiation strategies

4. FINANCIAL PROJECTIONS
   - Revenue projections (monthly and yearly)
   - Cost structure analysis
   - Break-even analysis
   - Cash flow projections
   - ROI expectations
   - Budget adequacy assessment

5. OPERATIONAL CONSIDERATIONS
   - Location advantages and disadvantages
   - Infrastructure requirements
   - Staffing needs and costs
   - Supply chain considerations
   - Technology requirements

6. RISK ASSESSMENT
   - Market risks
   - Operational risks
   - Financial risks
   - Regulatory risks
   - Mitigation strategies

7. STRATEGIC RECOMMENDATIONS
   - Go/No-go recommendation with rationale
   - Implementation timeline
   - Success metrics and KPIs
   - Long-term growth strategies
   - Exit strategies

8. CONCLUSION
   - Final assessment
   - Next steps
   - Key success factors to monitor

Format this as a professional business report with clear sections and detailed analysis. Be specific, data-driven, and actionable in your recommendations.
"""

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(detailed_prompt)
        detailed_analysis_text = response.text.strip()
        
        # Clean the detailed analysis
        detailed_analysis_text = clean_text(detailed_analysis_text)
        
        # Add detailed analysis to basic analysis
        basic_analysis['detailed_analysis'] = detailed_analysis_text
        
        return basic_analysis
        
    except Exception as e:
        print(f"Error generating detailed analysis: {e}")
        # Return basic analysis with error message
        basic_analysis['detailed_analysis'] = "Detailed analysis could not be generated due to technical issues. Please refer to the basic analysis above."
        return basic_analysis

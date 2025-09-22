# analysis.py
from google import genai

# Option 1: Use environment variable (recommended)
client = genai.Client(api_key="AIzaSyC9ByL_0yDWb3GuNcwND-Te3RMJEColZ40")

# Option 2: Hardcode API key (for testing only)
# client = genai.Client(api_key="YOUR_KEY_HERE")

def analyze_location(business_data, business_type):
    """
    Returns feasibility %, competition, pros, cons, and nearby businesses.
    """
    if not business_data:
        return {
            "feasibility": 80,
            "competition": "Low",
            "pros": ["No competitors nearby, good opportunity"],
            "cons": [],
            "businesses": []
        }

    # Determine competition and feasibility
    num_competitors = len(business_data)
    if num_competitors >= 8:
        competition = "High"
        feasibility = 30
    elif num_competitors >= 4:
        competition = "Medium"
        feasibility = 50
    else:
        competition = "Low"
        feasibility = 70

    businesses_list = [
        f"{biz['name']} ({', '.join(biz['types'])}) at {biz['lat']},{biz['lng']}"
        for biz in business_data
    ]

    # Prompt for Gemini AI
    prompt = f"Analyze opening a {business_type} in this area.\n" \
             f"List 3 pros and 3 cons based on location and competitors.\n" \
             f"Nearby businesses:\n" + "\n".join(businesses_list)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        output_text = response.text.strip()

        pros, cons = [], []
        lines = [line.strip() for line in output_text.split("\n") if line.strip()]
        for line in lines:
            if line.lower().startswith("pro") or line.startswith("-"):
                pros.append(line.replace("Pro:", "").replace("-", "").strip())
            elif line.lower().startswith("con"):
                cons.append(line.replace("Con:", "").replace("-", "").strip())

        if not pros:
            pros = ["Location seems favorable for customer footfall."]
        if not cons:
            cons = ["Competition may be strong nearby."]

    except Exception as e:
        print(f"Error generating content: {e}")
        pros = ["Location seems favorable for customer footfall."]
        cons = ["Competition may be strong nearby."]

    return {
        "feasibility": feasibility,
        "competition": competition,
        "pros": pros,
        "cons": cons,
        "businesses": businesses_list
    }

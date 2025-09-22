# Business Feasibility Analyzer

A comprehensive web-based application that helps entrepreneurs and business owners analyze the feasibility of starting a business at a specific location. The application uses **Google Maps API** and **Google Gemini AI** to provide detailed insights on market competition, financial feasibility, strategic recommendations, and nearby competitors.

---

## Features

- **Location-Based Analysis:** Input latitude and longitude to get an analysis of the business potential in that area.
- **Business Type Selection:** Supports multiple business types including restaurants, cafes, gyms, pharmacies, retail stores, banks, and more.
- **Budget Evaluation:** Input your budget in INR lakhs to get a feasibility score.
- **AI-Powered Analysis:** Uses Google Gemini 1.5 Flash model to generate detailed market research and recommendations.
- **PDF Report Generation:** Download a detailed business feasibility report in PDF format.
- **Interactive Map:** Visualize your location and nearby competitors on an interactive map using Leaflet.js.
- **Competitor Analysis:** Displays nearby competitors with name, location, rating, and price level.
- **User-Friendly Interface:** Simple and responsive design for easy navigation on any device.

---

## Table of Contents

- [Installation](#installation)  
- [Usage](#usage)  
- [File Structure](#file-structure)  
- [Tech Stack](#tech-stack)  
- [How It Works](#how-it-works)  
- [Example Use Case](#example-use-case)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Installation

# 1. Clone the repository
git clone https://github.com/<your-username>/business-feasibility-analyzer.git
cd business-feasibility-analyzer

# 2. Create a virtual environment
python -m venv venv
# Activate the virtual environment:
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file in the root directory and add your Google API key:
echo "GOOGLE_API_KEY=your_google_api_key_here" > .env

---

## Usage

# 1. Activate your virtual environment (if not already active)
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

# 2. Run the Flask application
python main.py

# 3. Open your browser and navigate to:
http://127.0.0.1:5001/

# 4. Fill in the form:
#    - Location: Enter latitude and longitude (e.g., 28.6139,77.2090)
#    - Business Type: Select from dropdown (Restaurant, Cafe, Gym, etc.)
#    - Budget: Enter your investment budget in INR Lakhs
#    - Additional Notes: Optional extra information about your business idea

# 5. Click "Analyze" to view the business feasibility report.
# 6. Optionally, download the detailed PDF report using the "Download Detailed PDF Report" button.

---

## Tech Stack

The Business Feasibility Analyzer is built using the following technologies:

- **Backend:**
  - [Python 3.10+](https://www.python.org/)
  - [Flask](https://flask.palletsprojects.com/) – Web framework
  - [googlemaps](https://pypi.org/project/googlemaps/) – For fetching nearby businesses
  - [Google Generative AI API (Gemini 1.5)](https://developers.generativeai.google/) – AI-based business analysis
  - [dotenv](https://pypi.org/project/python-dotenv/) – Environment variable management

- **Frontend:**
  - HTML5 & CSS3
  - [Leaflet.js](https://leafletjs.com/) – Interactive maps

- **Reporting:**
  - [ReportLab](https://www.reportlab.com/) – PDF generation

- **Deployment & Environment:**
  - Virtual environment (venv)
  - Git & GitHub for version control

- **Other Tools:**
  - Browser (for running the web app locally)
  - Optional: Text editor or IDE like VS Code, PyCharm

---

## Working

The Business Feasibility Analyzer helps users evaluate whether starting a particular business at a given location is practical.  
Here’s how it works step by step:

1. **User Input**
   - Enter location coordinates (latitude, longitude).
   - Select a business type (e.g., restaurant, gym, cafe, pharmacy).
   - Provide a budget (in INR Lakhs).
   - (Optional) Add extra notes or specific requirements.

2. **Data Collection**
   - The app uses the **Google Maps API** to fetch details of nearby businesses.
   - Collects competitor data: name, rating, price level, and location.

3. **AI-Powered Analysis**
   - The **Gemini API** processes the input data.
   - Generates:
     - Feasibility percentage
     - Competition level (High/Medium/Low)
     - Advantages and Challenges
     - Market insights
     - Budget analysis
     - Strategic recommendations
     - Alternative business suggestions

4. **Visualization**
   - Displays feasibility as a **progress bar**.
   - Shows competitor businesses in a **table**.
   - Renders an **interactive map** using Leaflet.js, marking both user location and nearby competitors.

5. **Report Generation**
   - Users can **download a detailed PDF report** containing all analysis and recommendations.

6. **Output**
   - Clear feasibility percentage.
   - Competitor overview.
   - Practical recommendations for decision-making.

---

##License

For educational and hackathon use.

---

# sAIlors Business Feasibility Analyzer

A modern web application that helps entrepreneurs analyze the feasibility of starting a business in a specific location. The app uses AI-powered analysis combined with real-time Google Places data to provide comprehensive business insights.

## Features

- **Hero Section**: Modern, responsive landing page with call-to-action
- **AI-Powered Analysis**: Uses Google's Generative AI for detailed business feasibility analysis
- **Real-time Data**: Integrates with Google Places API for competitor analysis
- **Interactive Map**: Visual representation of nearby businesses
- **PDF Reports**: Generate detailed PDF reports for business planning
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Quick Start

1. **Clone and Navigate**:
   ```bash
   cd /home/saswat-balyan/devStuff/sAIlors/webapp_update
   ```

2. **Run the Webapp**:
   ```bash
   ./run_webapp.sh
   ```

3. **Access the Application**:
   Open your browser and go to `http://localhost:5001`

## Setup Requirements

### Prerequisites
- Python 3.8 or higher
- pip3
- Google API Key (free)

### Google API Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the following APIs:
   - Google Places API
   - Google Generative AI API
4. Create credentials (API Key)
5. Add the API key to `business_feasibility/.env` file

### Environment Configuration
The script will create a `.env` file template if it doesn't exist. Edit `business_feasibility/.env`:

```env
GOOGLE_API_KEY=your_actual_api_key_here
```

## Project Structure

```
webapp_update/
├── business_feasibility/          # Backend Flask application
│   ├── app.py                     # Main Flask application
│   ├── analysis.py                # AI analysis logic
│   ├── data_fetcher.py            # Google Places API integration
│   ├── requirements.txt           # Python dependencies
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css          # Modern dark theme CSS
│   │   └── images/                # Static images
│   └── templates/
│       └── index.html             # Main HTML template
├── frontend/                      # Frontend assets (JSX design reference)
│   ├── react.jsx                  # Original React component
│   ├── text.jsx                   # Text styles reference
│   └── assets/                    # Design assets
├── run_webapp.sh                  # Launch script
└── README.md                      # This file
```

## How It Works

1. **User Input**: Enter location coordinates, business type, budget, and optional notes
2. **Data Collection**: App fetches nearby businesses using Google Places API
3. **AI Analysis**: Google Generative AI analyzes the data and provides insights
4. **Results Display**: Comprehensive analysis including:
   - Feasibility score
   - Competition level
   - Advantages and challenges
   - Market analysis
   - Financial assessment
   - Strategic recommendations
   - Interactive map of competitors

## Business Types Supported

- Restaurant
- Cafe
- Gym/Fitness Center
- Pharmacy
- Grocery Store
- Bar
- Shopping Mall
- Hotel/Inn
- Retail Store
- Beauty Salon
- Medical Clinic
- Bank/Financial Services

## Technology Stack

- **Backend**: Python Flask
- **AI**: Google Generative AI (Gemini)
- **Maps**: Google Places API, Leaflet.js
- **Frontend**: HTML5, CSS3, JavaScript
- **PDF Generation**: ReportLab
- **Styling**: Custom CSS with modern dark theme

## API Usage

The application makes requests to:
- Google Places API for business data
- Google Generative AI API for analysis
- OpenStreetMap for map tiles

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your Google API key is correctly set in `.env`
2. **Port Already in Use**: Change the port in `app.py` if 5001 is occupied
3. **Missing Dependencies**: Run `pip3 install -r business_feasibility/requirements.txt`
4. **Permission Denied**: Make sure `run_webapp.sh` is executable: `chmod +x run_webapp.sh`

### Getting Help

If you encounter issues:
1. Check the terminal output for error messages
2. Verify your Google API key and enabled APIs
3. Ensure all dependencies are installed
4. Check that Python 3.8+ is installed

## License

This project is for educational and business analysis purposes.

## Contributing

Feel free to submit issues and enhancement requests!

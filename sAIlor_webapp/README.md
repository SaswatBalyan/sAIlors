# sAIlor - AI-Powered Location Intelligence Platform

A comprehensive Next.js + FastAPI application that provides intelligent location analysis for businesses using advanced **AI/ML** and **geospatial** data. Enter a candidate site (latitude/longitude), a radius, and your business type to get detailed feasibility analysis with demand, competition, and risk metrics.

## 🚀 Features

- **Intelligent Location Analysis**: AI-powered feasibility scoring for business locations
- **Demand Analysis**: Population density analysis using geospatial rasters
- **Competition Analysis**: Real-time POI data from OpenStreetMap
- **Risk Assessment**: Comprehensive risk scoring based on business parameters
- **Interactive Maps**: Visual location analysis with Leaflet maps
- **Business Recommendations**: AI-driven business type recommendations
- **Trend Forecasting**: 12-month demand trend predictions
- **Modern UI**: Clean, responsive interface with dark theme

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Data Sources  │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│                 │
│                 │    │                 │    │ • Population    │
│ • React 19      │    │ • Python 3.11   │    │   Rasters       │
│ • TypeScript    │    │ • FastAPI       │    │ • OSM Overpass  │
│ • Tailwind CSS  │    │ • scikit-learn  │    │ • Geospatial    │
│ • Leaflet Maps  │    │ • Rasterio      │    │   Libraries     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Tech Stack

### Frontend
- **Next.js 15** with App Router
- **React 19** with TypeScript
- **Tailwind CSS** for styling
- **shadcn/ui** component library
- **Leaflet** for interactive maps
- **Recharts** for data visualization
- **React Hook Form** with Zod validation

### Backend
- **FastAPI** with Python 3.11
- **scikit-learn** for ML predictions
- **Rasterio** for geospatial data processing
- **Shapely** for geometric operations
- **PyProj** for coordinate transformations
- **Pandas** for data manipulation
- **Requests** for API calls

## 📋 Prerequisites

- **Node.js** 18+ (recommended: 20.x)
- **Python** 3.11+
- **Conda** or **Miniconda**
- **Git**

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd sAIlor_webapp
```

### 2. Backend Setup

```bash
# Create and activate conda environment
conda env create -f backend/environment.yml
conda activate sAIlor-backend

# Copy environment configuration
cp backend/.env.example backend/.env

# (Optional) Download population raster data
# Place population_density.tif in data/ directory
# Update POP_TIF_PATH in backend/.env

# Install dependencies and train model
cd backend
python app/build_dataset.py
python app/train.py

# Start the backend server
uvicorn app.main:app --app-dir backend --reload --port 8000
```

The backend will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd geoai-ui

# Install dependencies
npm install

# Copy environment configuration
cp .env.local.example .env.local

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📁 Project Structure

```
sAIlor_webapp/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # Main API application
│   │   ├── features.py        # ML feature processing
│   │   ├── train.py           # Model training script
│   │   └── build_dataset.py   # Dataset generation
│   ├── cache/                 # Model and POI cache
│   ├── environment.yml        # Conda environment
│   └── .env.example          # Environment variables
├── geoai-ui/                  # Next.js frontend
│   ├── src/
│   │   ├── app/              # Next.js app router pages
│   │   ├── components/       # React components
│   │   └── lib/              # Utility functions
│   ├── public/               # Static assets
│   └── package.json          # Frontend dependencies
├── data/                     # Data directory
│   └── population_density.tif # Population raster (optional)
└── README.md                 # This file
```

## 🔧 Configuration

### Backend Environment Variables

Create `backend/.env` with the following variables:

```env
# Population density raster file path (optional)
POP_TIF_PATH=data/population_density.tif

# Maximum population density for scaling
POP_MAX_DENSITY=5000

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# CORS Origins
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Frontend Environment Variables

Create `geoai-ui/.env.local` with the following variables:

```env
# Backend API Base URL
NEXT_PUBLIC_API_BASE=http://localhost:8000

# Map Configuration
NEXT_PUBLIC_MAP_DEFAULT_LAT=12.9698
NEXT_PUBLIC_MAP_DEFAULT_LON=79.1559
```

## 📊 API Endpoints

### POST /analyze
Analyze location feasibility for a business.

**Request Body:**
```json
{
  "business_type": "cafe",
  "city": "Vellore",
  "lat": 12.9698,
  "lon": 79.1559,
  "radius_m": 500,
  "budget_lakh": 10.0,
  "seating_capacity": 30,
  "use_population_density": true,
  "consider_competition": true
}
```

**Response:**
```json
{
  "summary": "Feasibility analysis for a cafe in Vellore...",
  "pros": ["Strong local demand", "Low competition"],
  "cons": ["High operational risk"],
  "scores": {
    "demand": 75,
    "risk": 42,
    "competition": 60
  },
  "debug": {
    "poi_count": 5,
    "mean_density": 3400.2,
    "raster_used": true
  },
  "pois": [...]
}
```

### POST /predict
Get ML model prediction for business viability.

**Request Body:**
```json
{
  "business_type": "cafe",
  "city": "Vellore",
  "budget_lakh": 10.0,
  "seating_capacity": 30,
  "radius_m": 500,
  "demand_score": 75
}
```

**Response:**
```json
{
  "prediction": "Promising",
  "confidence": 0.89,
  "probabilities": {
    "not_viable": 0.11,
    "promising": 0.89
  }
}
```

## 🎯 Business Types Supported

- **Cafe / Coffee Shop**: Perfect for high-footfall areas
- **Gym / Fitness Center**: Requires stable demand and manageable risk
- **Restaurant**: Needs strong demand and careful competition analysis
- **Stationery / Print Shop**: Good for office/campus areas
- **Hostel Mess / Canteen**: Ideal for student-dense areas
- **Retail Store**: Suitable for areas with good foot traffic
- **Pharmacy**: Essential service with stable demand
- **Beauty Salon / Spa**: Requires moderate demand and low competition

## 📈 Analysis Features

### Business Feasibility Score (BFS)
Composite metric combining:
- **Demand Score** (50%): Population density analysis
- **Safety Score** (30%): 100 - Risk Score
- **Open Space Score** (20%): 100 - Competition Score

### Risk Assessment
- Budget vs typical business parameters
- Seating capacity appropriateness
- Operating hours impact
- Market condition effects

### Competition Analysis
- Real-time POI data from OpenStreetMap
- Density-based competition scoring
- Cached results for performance

## 🔄 Development Workflow

### Running Tests
```bash
# Frontend
cd geoai-ui
npm run lint
npm run type-check

# Backend
cd backend
python -m pytest tests/
```

### Building for Production
```bash
# Frontend
cd geoai-ui
npm run build

# Backend
cd backend
uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000
```

## 🐛 Troubleshooting

### Common Issues

1. **Backend not starting**
   - Check if conda environment is activated
   - Verify all dependencies are installed
   - Check port 8000 is not in use

2. **Frontend build errors**
   - Clear Next.js cache: `npm run clean`
   - Delete node_modules and reinstall
   - Check TypeScript errors: `npm run type-check`

3. **Map not loading**
   - Ensure Leaflet CSS is imported
   - Check browser console for errors
   - Verify coordinates are valid

4. **Analysis returning mock data**
   - Check if backend is running on port 8000
   - Verify API_BASE_URL in frontend .env
   - Check backend logs for errors

### Performance Optimization

- **POI Caching**: POI data is cached for 1 hour
- **Raster Optimization**: Use compressed GeoTIFF files
- **Model Caching**: ML model is loaded once at startup
- **Frontend Optimization**: Code splitting and lazy loading

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenStreetMap** contributors for POI data
- **WorldPop/GHSL** for population density data
- **scikit-learn** community for ML tools
- **FastAPI** and **Next.js** communities
- **shadcn/ui** for beautiful components

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation at `/docs`

---

**Made with ❤️ for intelligent location analysis**
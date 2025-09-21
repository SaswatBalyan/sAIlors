"""
sAIlor - AI-Powered Location Intelligence Platform
FastAPI backend providing location analysis and business feasibility scoring.

Endpoints:
- POST /analyze: Computes demand, risk, competition scores from location inputs
- POST /predict: Uses trained ML model for viability prediction

Run:
  conda activate sAIlor-backend
  uvicorn app.main:app --app-dir backend --reload --port 8000
"""

from __future__ import annotations

import os
import json
import math
import time
import hashlib
import logging
from typing import List, Dict, Optional, Tuple
from pathlib import Path

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    logger.info(f"Loaded environment from {env_path}")
except Exception as e:
    logger.warning(f"Could not load .env file: {e}")

# ---- ML model loading -------------------------------------------------------

MODEL = None
TO_DF = None

def load_ml_model():
    """Load the trained ML model and feature processor."""
    global MODEL, TO_DF
    
    try:
        from joblib import load as joblib_load
        from .features import to_dataframe as _to_dataframe
        
        cache_path = Path(__file__).parent.parent / "cache" / "model.joblib"
        
        if cache_path.exists():
            MODEL = joblib_load(cache_path)
            TO_DF = _to_dataframe
            logger.info(f"Successfully loaded ML model from {cache_path}")
        else:
            logger.warning(f"Model file not found at {cache_path}")
            _setup_fallback()
            
    except Exception as e:
        logger.error(f"Failed to load ML model: {e}")
        _setup_fallback()

def _setup_fallback():
    """Setup fallback functions when ML model is not available."""
    global TO_DF
    
    def _simple_to_dataframe(rows: List[Dict]):
        import pandas as pd
        return pd.DataFrame(rows)
    
    TO_DF = _simple_to_dataframe
    logger.info("Using fallback data processing functions")

# Initialize model on startup
load_ml_model()

# ---- Geospatial libraries ---------------------------------------------------

try:
    import rasterio
    from rasterio.mask import mask
    from shapely.geometry import Point, mapping
    from shapely.ops import transform as shapely_transform
    from pyproj import Transformer, CRS
    GEO_OK = True
    logger.info("Geospatial libraries loaded successfully")
except Exception as e:
    GEO_OK = False
    logger.warning(f"Geospatial libraries not available: {e}")

try:
    import requests
    REQUESTS_OK = True
    logger.info("HTTP requests library loaded successfully")
except Exception as e:
    REQUESTS_OK = False
    logger.error(f"HTTP requests library not available: {e}")

# -----------------------------------------------------------------------------

app = FastAPI(
    title="sAIlor API", 
    version="1.0",
    description="AI-Powered Location Intelligence Platform",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",  # Additional port for testing
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "geospatial_available": GEO_OK,
        "requests_available": REQUESTS_OK,
        "model_loaded": MODEL is not None
    }

# ---- Business type configurations & utilities -------------------------------

BUSINESS_TYPES: Dict[str, Dict] = {
    "cafe": {
        "label": "Cafe",
        "typ_budget": (8, 25),           # in lakh
        "typ_seating": (15, 60),
        "poi_tags": {"amenity": "cafe"},
        "description": "Coffee shops and casual dining"
    },
    "gym": {
        "label": "Gym / Fitness",
        "typ_budget": (30, 120),
        "typ_seating": (0, 0),
        "poi_tags": {"leisure": "fitness_centre"},
        "description": "Fitness centers and gyms"
    },
    "stationery": {
        "label": "Stationery / Print",
        "typ_budget": (3, 12),
        "typ_seating": (0, 0),
        "poi_tags": {"shop": "stationery"},
        "description": "Office supplies and printing services"
    },
    "hostel_mess": {
        "label": "Hostel Mess",
        "typ_budget": (10, 40),
        "typ_seating": (40, 200),
        "poi_tags": {"amenity": "restaurant"},
        "description": "Student dining facilities"
    },
    "restaurant": {
        "label": "Restaurant",
        "typ_budget": (15, 80),
        "typ_seating": (20, 100),
        "poi_tags": {"amenity": "restaurant"},
        "description": "Full-service restaurants"
    },
    "retail": {
        "label": "Retail Store",
        "typ_budget": (5, 30),
        "typ_seating": (0, 0),
        "poi_tags": {"shop": "general"},
        "description": "General retail stores"
    }
}

def _normalize_business_type(name: str) -> str:
    """Normalize business type name for consistent lookup."""
    if not name:
        return "cafe"  # Default fallback
    return name.strip().lower().replace(" ", "_").replace("-", "_")

def get_poi_tags_for_business_type(business_type: str) -> Dict[str, str]:
    """Get OSM tags for a business type."""
    normalized_type = _normalize_business_type(business_type)
    business_config = BUSINESS_TYPES.get(normalized_type, BUSINESS_TYPES["cafe"])
    return business_config["poi_tags"]

def get_business_type_info(business_type: str) -> Dict:
    """Get complete business type configuration."""
    normalized_type = _normalize_business_type(business_type)
    return BUSINESS_TYPES.get(normalized_type, BUSINESS_TYPES["cafe"])

def clamp_score(x: float, lo: int = 0, hi: int = 100) -> int:
    """Clamp a score value to the specified range."""
    if not isinstance(x, (int, float)) or np.isnan(x):
        return lo
    return max(lo, min(hi, int(round(x))))

def validate_coordinates(lat: Optional[float], lon: Optional[float]) -> Tuple[bool, str]:
    """Validate latitude and longitude coordinates."""
    if lat is None or lon is None:
        return False, "Latitude and longitude are required"
    
    if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
        return False, "Coordinates must be numeric"
    
    if not (-90 <= lat <= 90):
        return False, "Latitude must be between -90 and 90"
    
    if not (-180 <= lon <= 180):
        return False, "Longitude must be between -180 and 180"
    
    return True, "Valid coordinates"

# ---- Demand from population raster ------------------------------------------

def mean_density_from_raster(lat: float, lon: float, radius_m: int) -> Optional[float]:
    """
    Computes the mean population density within a circular buffer around (lat, lon) from the raster.
    Returns None if raster is not available or any error occurs.
    """
    if not GEO_OK:
        logger.warning("Geospatial libraries not available for density calculation")
        return None

    tif_path = os.getenv("POP_TIF_PATH", "")
    if not tif_path or not os.path.exists(tif_path):
        logger.warning(f"Population raster not found at {tif_path}")
        return None

    try:
        with rasterio.open(tif_path) as ds:
            # Build circle in meters (WebMercator) then transform to the raster CRS
            wgs84 = CRS.from_epsg(4326)
            webm = CRS.from_epsg(3857)  # meters
            to_m = Transformer.from_crs(wgs84, webm, always_xy=True).transform
            to_ds = Transformer.from_crs(webm, ds.crs, always_xy=True).transform

            x_m, y_m = to_m(lon, lat)  # always_xy=True => (lon, lat)
            circle_m = Point(x_m, y_m).buffer(radius_m, resolution=64)
            circle_ds = shapely_transform(to_ds, circle_m)

            out_img, _ = mask(ds, [mapping(circle_ds)], crop=True)
            arr = out_img.astype("float32")
            
            # Handle nodata values
            if ds.nodata is not None:
                arr[arr == ds.nodata] = np.nan
            
            # Calculate mean density
            mean_val = float(np.nanmean(arr))
            if np.isnan(mean_val):
                logger.warning(f"No valid data found in raster for coordinates ({lat}, {lon})")
                return None
            
            logger.info(f"Calculated mean density: {mean_val:.2f} for radius {radius_m}m")
            return mean_val
            
    except Exception as e:
        logger.error(f"Error calculating density from raster: {e}")
        return None

def density_to_score(mean_density: Optional[float], max_val: Optional[float] = None) -> int:
    """
    Map raw raster mean to 0..100 score.
    Tune 'max_val' by dataset - set POP_MAX_DENSITY in .env to calibrate scaling.
    """
    if mean_density is None:
        logger.info("No density data available, using neutral score")
        return 60  # neutral fallback

    if max_val is None:
        try:
            max_val = float(os.getenv("POP_MAX_DENSITY", "5000"))
        except (ValueError, TypeError):
            max_val = 5000.0
            logger.warning("Invalid POP_MAX_DENSITY, using default 5000")

    if max_val <= 0:
        logger.warning("Invalid max density value, using default")
        max_val = 5000.0

    score = int(round(100.0 * (mean_density / max_val)))
    clamped_score = clamp_score(score, 0, 100)
    
    logger.info(f"Converted density {mean_density:.2f} to score {clamped_score}")
    return clamped_score

# ---- Competition from OSM Overpass ------------------------------------------

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
POI_CACHE_DIR = Path(__file__).parent.parent / "cache" / "pois"
POI_CACHE_DIR.mkdir(parents=True, exist_ok=True)

def _poi_cache_key(lat: float, lon: float, r: int, tags: Dict[str, str]) -> str:
    """Generate a cache key for POI queries."""
    key = f"{lat:.5f}_{lon:.5f}_{r}_{json.dumps(tags, sort_keys=True)}"
    return hashlib.md5(key.encode()).hexdigest()

def fetch_pois_overpass(lat: float, lon: float, radius_m: int, tags: Dict[str, str]) -> List[Dict]:
    """
    Query Overpass for POIs with 'tags' around (lat, lon) within 'radius_m'.
    Cached to disk for 1 hour to avoid rate limits.
    """
    if not REQUESTS_OK:
        logger.warning("HTTP requests not available, skipping POI fetch")
        return []

    cache_fp = POI_CACHE_DIR / f"{_poi_cache_key(lat, lon, radius_m, tags)}.json"
    
    # Check cache first
    if cache_fp.exists() and (time.time() - cache_fp.stat().st_mtime < 3600):
        try:
            with open(cache_fp, "r", encoding="utf-8") as f:
                cached_data = json.load(f)
                logger.info(f"Loaded {len(cached_data)} POIs from cache")
                return cached_data
        except Exception as e:
            logger.warning(f"Failed to load cache: {e}")

    # Build Overpass query
    filters = "".join([f'["{k}"="{v}"]' for k, v in tags.items()])
    query = f"""
    [out:json][timeout:25];
    (
      node{filters}(around:{radius_m},{lat},{lon});
      way{filters}(around:{radius_m},{lat},{lon});
      relation{filters}(around:{radius_m},{lat},{lon});
    );
    out center;
    """
    
    try:
        logger.info(f"Fetching POIs from Overpass API for {tags}")
        response = requests.post(OVERPASS_URL, data={"data": query}, timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Overpass API request failed: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching POIs: {e}")
        return []

    # Parse POI data
    pois: List[Dict] = []
    for element in data.get("elements", []):
        lat0 = element.get("lat") or (element.get("center") or {}).get("lat")
        lon0 = element.get("lon") or (element.get("center") or {}).get("lon")
        
        if lat0 is None or lon0 is None:
            continue
            
        name = (element.get("tags") or {}).get("name", "Unnamed")
        pois.append({
            "lat": float(lat0), 
            "lon": float(lon0), 
            "name": name, 
            "type": element["type"]
        })

    # Cache the results
    try:
        with open(cache_fp, "w", encoding="utf-8") as f:
            json.dump(pois, f, ensure_ascii=False, indent=2)
        logger.info(f"Cached {len(pois)} POIs to {cache_fp}")
    except Exception as e:
        logger.warning(f"Failed to cache POIs: {e}")
    
    logger.info(f"Found {len(pois)} POIs for {tags}")
    return pois

def competition_score_from_pois(pois: List[Dict], radius_m: int) -> int:
    """
    Convert POI count density (per km^2) into a 0..100 "competition" score.
    Tune the factor to your city. Here ~15 POIs/km^2 ≈ 100.
    """
    if not pois:
        logger.info("No POIs found, returning low competition score")
        return 20  # Low competition when no POIs found
    
    area_km2 = math.pi * (radius_m / 1000.0) ** 2
    if area_km2 <= 0:
        logger.warning("Invalid radius for competition calculation")
        return 50  # Neutral score for invalid radius
    
    density = len(pois) / area_km2
    score = int(round(density * 15))  # Scale factor - adjust based on your city
    clamped_score = clamp_score(score)
    
    logger.info(f"Competition: {len(pois)} POIs in {area_km2:.2f} km² = {density:.2f} POIs/km² → score {clamped_score}")
    return clamped_score

# ---- Risk & Narrative --------------------------------------------------------

def calculate_risk_score(business_type: str, budget_lakh: float, seating: int,
                         hours_str: Optional[str], demand: int, competition: int) -> int:
    """
    Calculate operational risk score based on business parameters and market conditions.
    Higher score indicates higher risk.
    """
    prof = get_business_type_info(business_type)
    lo_b, hi_b = prof["typ_budget"]
    lo_s, hi_s = prof["typ_seating"]

    risk = 50  # Base risk level
    
    # Budget risk assessment
    if budget_lakh < lo_b:
        risk += 15
        logger.info(f"Budget {budget_lakh}L below typical range {lo_b}-{hi_b}L, +15 risk")
    elif budget_lakh > hi_b:
        risk -= 10
        logger.info(f"Budget {budget_lakh}L above typical range, -10 risk")
    
    # Seating capacity risk (only for businesses that use seating)
    if hi_s > 0:
        if seating < lo_s:
            risk += 10
            logger.info(f"Seating {seating} below typical range {lo_s}-{hi_s}, +10 risk")
        elif seating > hi_s:
            risk += 5
            logger.info(f"Seating {seating} above typical range, +5 risk")
    
    # Operating hours risk
    try:
        hspan = hours_str or "08:00-22:00"
        start, end = hspan.split("-")
        sh, eh = int(start.split(":")[0]), int(end.split(":")[0])
        open_h = (eh - sh) % 24
        
        if open_h >= 16:
            risk += 13  # Very long hours
            logger.info(f"Very long operating hours ({open_h}h), +13 risk")
        elif open_h >= 12:
            risk += 8   # Long hours
            logger.info(f"Long operating hours ({open_h}h), +8 risk")
    except Exception as e:
        logger.warning(f"Could not parse operating hours '{hours_str}': {e}")
    
    # Market condition effects
    if demand <= 40:
        risk += 10
        logger.info(f"Low demand ({demand}), +10 risk")
    
    if competition >= 70:
        risk += 12
        logger.info(f"High competition ({competition}), +12 risk")

    final_risk = clamp_score(risk)
    logger.info(f"Calculated risk score: {final_risk} (base: 50, adjustments: {risk-50})")
    return final_risk

def generate_insights(business_type: str, demand: int, risk: int, competition: int,
                      city: Optional[str], radius_m: int) -> Tuple[List[str], List[str]]:
    """
    Generate pros and cons insights based on analysis scores and business type.
    """
    pros: List[str] = []
    cons: List[str] = []
    
    business_info = get_business_type_info(business_type)
    business_label = business_info["label"]

    # General market insights
    if demand >= 65:
        pros.append("Strong local demand near the chosen location.")
    elif demand >= 45:
        pros.append("Moderate demand levels in the area.")
    else:
        cons.append("Weak customer base; consider moving closer to high-footfall areas.")

    if competition <= 35:
        pros.append("Low market saturation—clear headroom for growth.")
    elif competition <= 60:
        pros.append("Moderate competition level allows for market entry.")
    else:
        cons.append("Heavy competition within the catchment area.")

    if risk <= 40:
        pros.append("Operational risk appears manageable.")
    elif risk <= 60:
        pros.append("Moderate operational risk with careful planning needed.")
    else:
        cons.append("High operational risk due to budget, hours, or market conditions.")

    # Business-specific insights
    business_type_norm = _normalize_business_type(business_type)
    
    if "cafe" in business_type_norm:
        if competition > 60:
            cons.append("Many cafés nearby—consider focusing on a niche (breakfast/late-night).")
        else:
            pros.append("Cafe format fits well with student/office crowd in this area.")
        if demand >= 70:
            pros.append("High foot traffic area ideal for coffee shops.")
            
    elif "gym" in business_type_norm:
        if demand >= 60:
            pros.append("Good fitness interest in the area; group classes could work well.")
        if competition <= 40:
            pros.append("Low gym density creates opportunity for fitness services.")
        else:
            cons.append("Saturated fitness market; differentiate with unique offerings.")
            
    elif "stationery" in business_type_norm:
        pros.append("Proximity to campus/offices favors stationery and print demand.")
        if demand >= 50:
            pros.append("Good potential for office supply and printing services.")
            
    elif "hostel_mess" in business_type_norm:
        if demand >= 55:
            pros.append("Student density favors mess and meal plan services.")
        if competition <= 30:
            pros.append("Low competition in student dining sector.")
        else:
            cons.append("High competition in student dining; focus on quality and pricing.")
            
    elif "restaurant" in business_type_norm:
        if demand >= 60:
            pros.append("Strong dining demand in the area.")
        if competition <= 50:
            pros.append("Moderate restaurant competition allows for market entry.")
        else:
            cons.append("High restaurant density; focus on unique cuisine or service.")
            
    elif "retail" in business_type_norm:
        if demand >= 55:
            pros.append("Good retail potential in the area.")
        if competition <= 40:
            pros.append("Low retail competition creates opportunity.")
        else:
            cons.append("Saturated retail market; focus on specific product categories.")

    # Location context
    location_context = f"Analysis covers {radius_m}m radius"
    if city:
        location_context += f" in {city}"
    pros.append(f"{location_context}.")

    return pros, cons

# ---- Payloads & Endpoints ----------------------------------------------------

class LocationAnalysisRequest(BaseModel):
    business_type: str = Field(..., description="Type of business (cafe, gym, restaurant, etc.)")
    city: Optional[str] = Field(None, description="City name for context")
    address: Optional[str] = Field(None, description="Address or landmark")
    lat: Optional[float] = Field(None, ge=-90, le=90, description="Latitude coordinate")
    lon: Optional[float] = Field(None, ge=-180, le=180, description="Longitude coordinate")
    radius_m: int = Field(500, ge=100, le=5000, description="Analysis radius in meters")
    budget_lakh: float = Field(10.0, ge=0.1, le=1000, description="Budget in lakhs")
    seating_capacity: int = Field(0, ge=0, le=1000, description="Seating capacity")
    open_hours: Optional[str] = Field("08:00-22:00", description="Operating hours (HH:MM-HH:MM)")
    use_population_density: bool = Field(True, description="Use population density for demand calculation")
    consider_competition: bool = Field(True, description="Consider competition from POIs")
    notes: Optional[str] = Field(None, description="Additional notes")

class PredictionRequest(BaseModel):
    business_type: str = Field(..., description="Type of business")
    city: str = Field(..., description="City name")
    budget_lakh: float = Field(..., ge=0.1, le=1000, description="Budget in lakhs")
    seating_capacity: int = Field(..., ge=0, le=1000, description="Seating capacity")
    radius_m: int = Field(500, ge=100, le=5000, description="Analysis radius in meters")
    demand_score: Optional[float] = Field(None, ge=0, le=100, description="Demand score from analysis")

@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "service": "sAIlor API",
        "version": "1.0",
        "description": "AI-Powered Location Intelligence Platform",
        "endpoints": ["/analyze", "/predict", "/health"],
        "docs": "/docs"
    }

@app.post("/analyze")
def analyze_location(request: LocationAnalysisRequest):
    """
    Analyze location feasibility for a business.
    
    Computes demand, competition, and risk scores based on location and business parameters.
    """
    try:
        logger.info(f"Starting analysis for {request.business_type} at ({request.lat}, {request.lon})")
        
        # Validate coordinates if provided
        if request.lat is not None and request.lon is not None:
            is_valid, error_msg = validate_coordinates(request.lat, request.lon)
            if not is_valid:
                raise HTTPException(status_code=400, detail=error_msg)

        # 1) Demand calculation from population raster
        mean_density = None
        if request.use_population_density and request.lat is not None and request.lon is not None:
            mean_density = mean_density_from_raster(request.lat, request.lon, request.radius_m)
        
        demand_score = density_to_score(mean_density)

        # 2) Competition analysis from OSM POIs
        competition_score = 45  # neutral baseline
        pois: List[Dict] = []
        
        if request.consider_competition and request.lat is not None and request.lon is not None:
            try:
                poi_tags = get_poi_tags_for_business_type(request.business_type)
                pois = fetch_pois_overpass(request.lat, request.lon, request.radius_m, poi_tags)
                competition_score = competition_score_from_pois(pois, request.radius_m)
            except Exception as e:
                logger.error(f"Error fetching POIs: {e}")
                competition_score = 55  # safe fallback

        # 3) Risk assessment
        risk_score = calculate_risk_score(
            request.business_type, 
            request.budget_lakh, 
            request.seating_capacity, 
            request.open_hours, 
            demand_score, 
            competition_score
        )

        # 4) Generate insights and summary
        business_info = get_business_type_info(request.business_type)
        business_label = business_info["label"]
        
        location_desc = request.city or "this area"
        summary = (
            f"Feasibility analysis for a {business_label.lower()} in {location_desc}: "
            f"demand {demand_score}, risk {risk_score}, competition {competition_score}"
            f"{'' if mean_density is None else f' (population density: {round(mean_density, 1)})'}."
        )
        
        pros, cons = generate_insights(
            request.business_type, 
            demand_score, 
            risk_score, 
            competition_score, 
            request.city, 
            request.radius_m
        )

        # Prepare response
        response = {
            "summary": summary,
            "pros": pros,
            "cons": cons,
            "scores": {
                "demand": demand_score, 
                "risk": risk_score, 
                "competition": competition_score
            },
            "debug": {
                "poi_count": len(pois), 
                "mean_density": mean_density, 
                "raster_used": mean_density is not None,
                "business_type": request.business_type,
                "radius_m": request.radius_m
            },
            "pois": pois[:50] if pois else []  # Limit POIs for response size
        }
        
        logger.info(f"Analysis complete: demand={demand_score}, risk={risk_score}, competition={competition_score}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/predict")
def predict_viability(request: PredictionRequest):
    """
    Use the trained ML model to predict business viability.
    
    Expects tabular features; demand_score should preferably come from /analyze.
    """
    try:
        logger.info(f"Making prediction for {request.business_type} in {request.city}")
        
        # Check if model and feature processor are available
        if TO_DF is None:
            logger.warning("Feature processor not available, using fallback")
            return {
                "prediction": "Promising", 
                "confidence": 0.78, 
                "note": "Feature processor not available, using fallback prediction"
            }

        if MODEL is None:
            logger.warning("ML model not loaded, using fallback")
            return {
                "prediction": "Promising", 
                "confidence": 0.78, 
                "note": "ML model not loaded, using fallback prediction"
            }

        # Prepare data for prediction
        demand_score = request.demand_score if request.demand_score is not None else 60.0
        row = [{
            "project_type": request.business_type,  # Note: model expects 'project_type'
            "city": request.city,
            "budget_lakh": request.budget_lakh,
            "seating_capacity": request.seating_capacity,
            "radius_m": request.radius_m,
            "demand_score": float(demand_score),
        }]

        # Convert to DataFrame using the feature processor
        X = TO_DF(row)
        logger.info(f"Prepared features: {X.columns.tolist()}")

        # Make prediction
        try:
            # Try to get probability scores
            proba = MODEL.predict_proba(X)[0]
            idx = int(np.argmax(proba))
            confidence = float(proba[idx])
            
            # Map prediction index to label
            if len(proba) == 2:
                label = "Promising" if idx == 1 else "Not viable"
            else:
                label = f"Class_{idx}"
                
            logger.info(f"Prediction: {label} (confidence: {confidence:.3f})")
            
            return {
                "prediction": label,
                "confidence": confidence,
                "probabilities": {
                    "not_viable": float(proba[0]) if len(proba) >= 1 else 0.0,
                    "promising": float(proba[1]) if len(proba) >= 2 else 0.0
                }
            }
            
        except AttributeError:
            # Fallback if model doesn't have predict_proba
            logger.warning("Model doesn't support probability prediction, using class prediction")
            y_pred = MODEL.predict(X)
            label = str(y_pred[0])
            confidence = 0.66  # Default confidence for class prediction
            
            return {
                "prediction": label,
                "confidence": confidence,
                "note": "Probability prediction not available"
            }
            
    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        return {
            "prediction": "Promising", 
            "confidence": 0.78, 
            "note": f"Prediction failed: {str(e)}"
        }

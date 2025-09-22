from flask import Flask, render_template, request
from analysis import analyze_location

app = Flask(__name__)

# Example nearby businesses
example_businesses = [
    {"name": "City Pharmacy", "lat": 28.6139, "lng": 77.2095, "types": ["pharmacy"]},
    {"name": "HealthPlus Pharmacy", "lat": 28.6142, "lng": 77.2100, "types": ["pharmacy"]},
    {"name": "Local Cafe", "lat": 28.6140, "lng": 77.2085, "types": ["cafe"]},
    {"name": "Fitness Gym", "lat": 28.6135, "lng": 77.2090, "types": ["gym"]},
    {"name": "Mini Grocery", "lat": 28.6137, "lng": 77.2103, "types": ["grocery_or_supermarket"]},
]

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        location = request.form["location"]
        business_type = request.form["business"]

        # Filter nearby businesses to selected type only
        filtered_businesses = [
            b for b in example_businesses if business_type in b.get("types", [])
        ]

        result = analyze_location(filtered_businesses, business_type)
        result["user_location"] = location.split(",")  # [lat, lng]
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)

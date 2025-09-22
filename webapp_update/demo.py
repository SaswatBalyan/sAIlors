#!/usr/bin/env python3
"""
Demo script for sAIlors Business Feasibility Analyzer
Shows the webapp features and capabilities
"""

import webbrowser
import time
import subprocess
import sys
import os

def print_banner():
    """Print the application banner"""
    print("=" * 60)
    print("🚀 sAIlors Business Feasibility Analyzer - Demo")
    print("=" * 60)
    print()

def check_webapp_running():
    """Check if the webapp is already running"""
    try:
        import requests
        response = requests.get("http://localhost:5001", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_webapp():
    """Start the webapp if not running"""
    print("🔧 Starting the webapp...")
    
    # Check if already running
    if check_webapp_running():
        print("✅ Webapp is already running!")
        return True
    
    # Start the webapp
    try:
        script_path = os.path.join(os.path.dirname(__file__), "run_webapp.sh")
        subprocess.Popen([script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait for webapp to start
        print("⏳ Waiting for webapp to start...")
        for i in range(30):  # Wait up to 30 seconds
            if check_webapp_running():
                print("✅ Webapp started successfully!")
                return True
            time.sleep(1)
            print(".", end="", flush=True)
        
        print("\n❌ Failed to start webapp")
        return False
        
    except Exception as e:
        print(f"\n❌ Error starting webapp: {e}")
        return False

def open_browser():
    """Open the webapp in the default browser"""
    print("🌐 Opening webapp in your browser...")
    try:
        webbrowser.open("http://localhost:5001")
        print("✅ Browser opened!")
    except Exception as e:
        print(f"❌ Could not open browser: {e}")
        print("   Please manually open: http://localhost:5001")

def show_features():
    """Display the webapp features"""
    print("\n📋 Webapp Features:")
    print("   • Modern hero section with call-to-action")
    print("   • AI-powered business feasibility analysis")
    print("   • Real-time competitor data from Google Places")
    print("   • Interactive map showing nearby businesses")
    print("   • Comprehensive analysis including:")
    print("     - Feasibility score and competition level")
    print("     - Advantages and challenges")
    print("     - Market analysis and financial assessment")
    print("     - Strategic recommendations")
    print("     - Alternative business type suggestions")
    print("   • PDF report generation")
    print("   • Responsive design for all devices")

def show_usage_instructions():
    """Show how to use the webapp"""
    print("\n📖 How to Use:")
    print("   1. Enter location coordinates (e.g., 28.6139,77.2090 for Delhi)")
    print("   2. Select your business type from the dropdown")
    print("   3. Enter your budget in INR Lakhs")
    print("   4. Add any additional notes (optional)")
    print("   5. Click 'Analyze' to get your feasibility report")
    print("   6. Download PDF report for detailed analysis")

def show_api_setup():
    """Show API setup instructions"""
    print("\n🔑 API Setup (for full functionality):")
    print("   1. Get a free Google API key from: https://console.cloud.google.com/")
    print("   2. Enable Google Places API and Google Generative AI API")
    print("   3. Add your API key to: business_feasibility/.env")
    print("   4. Restart the webapp")

def main():
    """Main demo function"""
    print_banner()
    
    # Start webapp
    if not start_webapp():
        print("❌ Could not start webapp. Please run './run_webapp.sh' manually.")
        return
    
    # Show features
    show_features()
    
    # Show usage instructions
    show_usage_instructions()
    
    # Show API setup
    show_api_setup()
    
    # Open browser
    open_browser()
    
    print("\n🎉 Demo complete! The webapp should now be open in your browser.")
    print("   Press Ctrl+C to stop the webapp when you're done.")
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for trying sAIlors Business Feasibility Analyzer!")
        print("   To stop the webapp, run: pkill -f 'python3 app.py'")

if __name__ == "__main__":
    main()

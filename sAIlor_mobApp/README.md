# Synthesys Mobile App

A mobile version of the Synthesys GeoAI feasibility analysis tool, converted from the web application. This Android app helps users evaluate business locations and concepts using AI-powered analysis.

## Features

### 🏠 Hero Screen
- Welcome screen with app branding
- Call-to-action buttons to start analysis
- Mobile-optimized design with gradient backgrounds

### 📊 Scenario Analysis
- **Project Type Selection**: Choose from Cafe, Gym, Hostel Mess, Bookstore, or Other
- **Location Input**: City, address, and precise coordinates
- **Business Details**: Budget, seating capacity, operating hours
- **Analysis Parameters**: Population density and competition consideration toggles
- **Location Services**: "Use my location" button for easy coordinate input

### 📈 Results Dashboard
- **Feasibility Score**: Overall business viability percentage
- **Detailed Analysis**: Pros, cons, and risk factors
- **Score Breakdown**: Demand, Risk, and Competition metrics
- **Map View**: Visual representation of the analysis area
- **Business Recommendations**: AI-suggested business types with probability scores
- **Demographics**: Target audience analysis
- **Spending Patterns**: Customer behavior insights
- **Predictions**: Future success probability

## Technical Stack

- **Framework**: Android with Jetpack Compose
- **Language**: Kotlin
- **UI**: Material Design 3 with custom dark theme
- **Navigation**: Navigation Compose
- **Networking**: Retrofit 2 with Gson
- **Charts**: Vico Compose (planned)
- **Maps**: Google Maps Compose (planned)
- **Architecture**: MVVM with Repository pattern

## Project Structure

```
app/src/main/java/com/example/sailor/
├── data/                    # Data models and entities
│   └── ScenarioData.kt
├── network/                 # API service definitions
│   └── ApiService.kt
├── repository/              # Data repository
│   └── AnalysisRepository.kt
├── ui/
│   ├── components/          # Reusable UI components
│   │   └── MapView.kt
│   ├── screens/             # Main app screens
│   │   ├── HeroScreen.kt
│   │   ├── ScenarioFormScreen.kt
│   │   └── ResultsScreen.kt
│   └── theme/               # App theming
│       ├── Color.kt
│       ├── Theme.kt
│       └── Type.kt
├── utils/                   # Utility functions
│   └── InsightsUtils.kt
├── viewmodel/               # ViewModels
│   └── MainViewModel.kt
└── MainActivity.kt          # Main activity with navigation
```

## Setup Instructions

### Prerequisites
- Android Studio Arctic Fox or later
- Android SDK 24+ (Android 7.0)
- Google Maps API key (for map functionality)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sAIlor
   ```

2. **Open in Android Studio**
   - Launch Android Studio
   - Open the project folder

3. **Configure Google Maps API**
   - Get a Google Maps API key from the [Google Cloud Console](https://console.cloud.google.com/)
   - Replace `YOUR_GOOGLE_MAPS_API_KEY` in `AndroidManifest.xml` with your actual API key

4. **Build and Run**
   - Sync project with Gradle files
   - Build the project
   - Run on an emulator or physical device

## API Integration

The app is designed to work with the same backend API as the web application:

- **Analysis Endpoint**: `POST /analyze` - Analyzes business feasibility
- **Prediction Endpoint**: `POST /predict` - Provides success predictions

Currently, the app uses mock data for demonstration purposes. To connect to a real backend:

1. Update the API base URL in the repository
2. Implement proper error handling
3. Add authentication if required

## Mobile-Specific Optimizations

### UI/UX Improvements
- **Touch-Friendly Controls**: Large buttons and input fields
- **Responsive Design**: Adapts to different screen sizes
- **Dark Theme**: Matches the web app's aesthetic
- **Smooth Navigation**: Intuitive flow between screens
- **Loading States**: Visual feedback during API calls

### Performance Optimizations
- **Lazy Loading**: Efficient list rendering
- **Image Optimization**: Compressed assets
- **Memory Management**: Proper state handling
- **Network Efficiency**: Optimized API calls

### Mobile Features
- **Location Services**: GPS integration for coordinates
- **Offline Support**: Cached data for better UX
- **Push Notifications**: (Future enhancement)
- **Biometric Authentication**: (Future enhancement)

## Development Notes

### Current Status
- ✅ Core UI screens implemented
- ✅ Navigation flow complete
- ✅ Mock data integration
- ✅ Mobile-optimized design
- ⏳ Google Maps integration (placeholder)
- ⏳ Real API integration
- ⏳ Advanced charting

### Future Enhancements
- Real-time map integration with POI data
- Advanced data visualization
- Offline mode support
- Push notifications
- User authentication
- Data export functionality
- Social sharing features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the InnovAct2025 TeamSynthesys initiative.

## Support

For questions or support, please contact the development team or create an issue in the repository.


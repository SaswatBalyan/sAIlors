package com.example.sailor.repository

import com.example.sailor.data.AnalysisResult
import com.example.sailor.data.PredictionResult
import com.example.sailor.data.ScenarioData
import com.example.sailor.network.ApiService
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AnalysisRepository @Inject constructor(
    private val apiService: ApiService
) {
    suspend fun analyzeScenario(scenario: ScenarioData): Result<AnalysisResult> {
        return try {
            val request = com.example.sailor.network.AnalysisRequest(
                project_type = scenario.projectType.name.lowercase().replace("_", "-"),
                city = scenario.city,
                address = scenario.address,
                lat = scenario.lat,
                lon = scenario.lon,
                radius_m = scenario.radiusM,
                budget_lakh = scenario.budgetInLakh,
                seating_capacity = scenario.seatingCapacity,
                open_hours = scenario.openHours,
                use_population_density = scenario.usePopulationDensity,
                consider_competition = scenario.considerCompetition,
                notes = scenario.notes
            )
            
            val response = apiService.analyze(request)
            if (response.isSuccessful) {
                Result.success(response.body() ?: getMockAnalysisResult())
            } else {
                Result.success(getMockAnalysisResult()) // Fallback to mock data
            }
        } catch (e: Exception) {
            Result.success(getMockAnalysisResult()) // Fallback to mock data
        }
    }
    
    suspend fun getPrediction(
        projectType: String,
        city: String,
        budgetLakh: Double,
        seatingCapacity: Int,
        radiusM: Int,
        demandScore: Int,
        lat: Double?,
        lon: Double?
    ): Result<PredictionResult> {
        return try {
            val request = com.example.sailor.network.PredictionRequest(
                project_type = projectType,
                city = city,
                budget_lakh = budgetLakh,
                seating_capacity = seatingCapacity,
                radius_m = radiusM,
                demand_score = demandScore,
                lat = lat,
                lon = lon
            )
            
            val response = apiService.predict(request)
            if (response.isSuccessful) {
                Result.success(response.body() ?: getMockPredictionResult())
            } else {
                Result.success(getMockPredictionResult())
            }
        } catch (e: Exception) {
            Result.success(getMockPredictionResult())
        }
    }
    
    private fun getMockAnalysisResult(): AnalysisResult {
        return AnalysisResult(
            summary = "Dummy feasibility (mock): good demand near campus; watch competition.",
            pros = listOf("High student footfall (mock)", "Lower rent (mock)"),
            cons = listOf("Nearby competition (mock)", "Seasonal demand (mock)"),
            scores = com.example.sailor.data.Scores(risk = 42, demand = 75, competition = 60)
        )
    }
    
    private fun getMockPredictionResult(): PredictionResult {
        return PredictionResult(
            prediction = "Moderate Success",
            confidence = 0.75
        )
    }
}


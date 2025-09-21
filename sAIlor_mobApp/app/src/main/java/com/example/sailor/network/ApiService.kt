package com.example.sailor.network

import com.example.sailor.data.AnalysisResult
import com.example.sailor.data.PredictionResult
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.POST

interface ApiService {
    @POST("analyze")
    suspend fun analyze(@Body request: AnalysisRequest): Response<AnalysisResult>
    
    @POST("predict")
    suspend fun predict(@Body request: PredictionRequest): Response<PredictionResult>
}

data class AnalysisRequest(
    val project_type: String,
    val city: String,
    val address: String?,
    val lat: Double,
    val lon: Double,
    val radius_m: Int,
    val budget_lakh: Double,
    val seating_capacity: Int,
    val open_hours: String?,
    val use_population_density: Boolean,
    val consider_competition: Boolean,
    val notes: String?
)

data class PredictionRequest(
    val project_type: String,
    val city: String,
    val budget_lakh: Double,
    val seating_capacity: Int,
    val radius_m: Int,
    val demand_score: Int,
    val lat: Double?,
    val lon: Double?
)


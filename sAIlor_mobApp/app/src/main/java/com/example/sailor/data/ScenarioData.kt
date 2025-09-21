package com.example.sailor.data

data class ScenarioData(
    val projectType: ProjectType,
    val city: String,
    val address: String? = null,
    val budgetInLakh: Double,
    val seatingCapacity: Int,
    val openHours: String? = null,
    val lat: Double,
    val lon: Double,
    val radiusM: Int = 500,
    val usePopulationDensity: Boolean = true,
    val considerCompetition: Boolean = true,
    val notes: String? = null
)

enum class ProjectType(val displayName: String) {
    CAFE("Cafe"),
    GYM("Gym"),
    HOSTEL_MESS("Hostel Mess"),
    BOOKSTORE("Bookstore"),
    OTHER("Other")
}

data class AnalysisResult(
    val summary: String,
    val pros: List<String>,
    val cons: List<String>,
    val scores: Scores
)

data class Scores(
    val risk: Int,
    val demand: Int,
    val competition: Int
)

data class PredictionResult(
    val prediction: String,
    val confidence: Double
)

data class FeasibilityResult(
    val score: Int,
    val feasible: Boolean,
    val cutoff: Int
)

data class BusinessRecommendation(
    val name: String,
    val probability: Int
)

data class GapData(
    val label: String,
    val demand: Int,
    val supply: Int
)

data class TrendData(
    val month: String,
    val demand: Int
)

data class DemographicData(
    val label: String,
    val value: String
)

data class SpendingData(
    val label: String,
    val value: String
)


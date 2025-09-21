package com.example.sailor

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.sailor.ui.screens.HeroScreen
import com.example.sailor.ui.screens.ResultsScreen
import com.example.sailor.ui.screens.ScenarioFormScreen
import com.example.sailor.ui.theme.SAIlorTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            SAIlorTheme {
                MainApp()
            }
        }
    }
}

@Composable
fun MainApp() {
    val navController = rememberNavController()
    var analysisResult by remember { mutableStateOf<com.example.sailor.data.AnalysisResult?>(null) }
    var predictionResult by remember { mutableStateOf<com.example.sailor.data.PredictionResult?>(null) }
    var currentScenario by remember { mutableStateOf<com.example.sailor.data.ScenarioData?>(null) }
    var isLoading by remember { mutableStateOf(false) }
    var isLoadingPrediction by remember { mutableStateOf(false) }

    Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = "hero",
            modifier = Modifier.padding(innerPadding)
        ) {
            composable("hero") {
                HeroScreen(
                    onAnalyzeClick = {
                        navController.navigate("form")
                    },
                    onCommunityClick = {
                        // TODO: Implement community action
                    }
                )
            }
            
            composable("form") {
                ScenarioFormScreen(
                    onBackClick = {
                        navController.popBackStack()
                    },
                    onSubmit = { scenario ->
                        currentScenario = scenario
                        isLoading = true
                        // Simulate API call
                        kotlinx.coroutines.GlobalScope.launch {
                            kotlinx.coroutines.delay(2000) // Simulate network delay
                            analysisResult = com.example.sailor.data.AnalysisResult(
                                summary = "Dummy feasibility (mock): good demand near campus; watch competition.",
                                pros = listOf("High student footfall (mock)", "Lower rent (mock)"),
                                cons = listOf("Nearby competition (mock)", "Seasonal demand (mock)"),
                                scores = com.example.sailor.data.Scores(risk = 42, demand = 75, competition = 60)
                            )
                            isLoading = false
                            navController.navigate("results")
                        }
                    },
                    isLoading = isLoading
                )
            }
            
            composable("results") {
                analysisResult?.let { result ->
                    ResultsScreen(
                        analysisResult = result,
                        predictionResult = predictionResult,
                        onBackClick = {
                            navController.popBackStack()
                        },
                        onGetPrediction = {
                            isLoadingPrediction = true
                            // Simulate API call
                            kotlinx.coroutines.GlobalScope.launch {
                                kotlinx.coroutines.delay(1500)
                                predictionResult = com.example.sailor.data.PredictionResult(
                                    prediction = "Moderate Success",
                                    confidence = 0.75
                                )
                                isLoadingPrediction = false
                            }
                        },
                        onExportJson = {
                            // TODO: Implement JSON export
                        },
                        isLoadingPrediction = isLoadingPrediction,
                        scenarioData = currentScenario
                    )
                } ?: run {
                    // Show error or redirect
                    navController.navigate("hero")
                }
            }
        }
    }
}
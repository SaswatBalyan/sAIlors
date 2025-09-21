package com.example.sailor.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.sailor.data.AnalysisResult
import com.example.sailor.data.PredictionResult
import com.example.sailor.data.ScenarioData
import com.example.sailor.repository.AnalysisRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class MainViewModel @Inject constructor(
    private val repository: AnalysisRepository
) : ViewModel() {
    
    private val _uiState = MutableStateFlow(MainUiState())
    val uiState: StateFlow<MainUiState> = _uiState.asStateFlow()
    
    fun analyzeScenario(scenario: ScenarioData) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)
            
            repository.analyzeScenario(scenario).fold(
                onSuccess = { result ->
                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        analysisResult = result,
                        currentScenario = scenario
                    )
                },
                onFailure = { error ->
                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        error = error.message ?: "Analysis failed"
                    )
                }
            )
        }
    }
    
    fun getPrediction() {
        val currentScenario = _uiState.value.currentScenario
        val analysisResult = _uiState.value.analysisResult
        
        if (currentScenario == null || analysisResult == null) return
        
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoadingPrediction = true)
            
            repository.getPrediction(
                projectType = currentScenario.projectType.name.lowercase().replace("_", "-"),
                city = currentScenario.city,
                budgetLakh = currentScenario.budgetInLakh,
                seatingCapacity = currentScenario.seatingCapacity,
                radiusM = currentScenario.radiusM,
                demandScore = analysisResult.scores.demand,
                lat = currentScenario.lat,
                lon = currentScenario.lon
            ).fold(
                onSuccess = { result ->
                    _uiState.value = _uiState.value.copy(
                        isLoadingPrediction = false,
                        predictionResult = result
                    )
                },
                onFailure = { error ->
                    _uiState.value = _uiState.value.copy(
                        isLoadingPrediction = false,
                        error = error.message ?: "Prediction failed"
                    )
                }
            )
        }
    }
    
    fun clearError() {
        _uiState.value = _uiState.value.copy(error = null)
    }
    
    fun clearResults() {
        _uiState.value = _uiState.value.copy(
            analysisResult = null,
            predictionResult = null,
            currentScenario = null
        )
    }
}

data class MainUiState(
    val isLoading: Boolean = false,
    val isLoadingPrediction: Boolean = false,
    val analysisResult: AnalysisResult? = null,
    val predictionResult: PredictionResult? = null,
    val currentScenario: ScenarioData? = null,
    val error: String? = null
)


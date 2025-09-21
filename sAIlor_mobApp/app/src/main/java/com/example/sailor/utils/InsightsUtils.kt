package com.example.sailor.utils

import com.example.sailor.data.*

object InsightsUtils {
    
    fun computeFeasibility(scores: Scores): FeasibilityResult {
        val score = ((scores.demand * 0.4) + ((100 - scores.risk) * 0.3) + ((100 - scores.competition) * 0.3)).toInt()
        val cutoff = 60
        return FeasibilityResult(
            score = score,
            feasible = score >= cutoff,
            cutoff = cutoff
        )
    }
    
    fun recommendBusinesses(scores: Scores): List<BusinessRecommendation> {
        val recommendations = mutableListOf<BusinessRecommendation>()
        
        when {
            scores.demand > 70 && scores.competition < 40 -> {
                recommendations.add(BusinessRecommendation("Premium Cafe", 85))
                recommendations.add(BusinessRecommendation("Co-working Space", 75))
                recommendations.add(BusinessRecommendation("Bookstore", 65))
            }
            scores.demand > 60 && scores.competition < 50 -> {
                recommendations.add(BusinessRecommendation("Quick Service Restaurant", 80))
                recommendations.add(BusinessRecommendation("Gym", 70))
                recommendations.add(BusinessRecommendation("Hostel Mess", 60))
            }
            else -> {
                recommendations.add(BusinessRecommendation("Food Truck", 70))
                recommendations.add(BusinessRecommendation("Pop-up Store", 60))
                recommendations.add(BusinessRecommendation("Online Service", 50))
            }
        }
        
        return recommendations
    }
    
    fun buildGapSeries(scores: Scores): List<GapData> {
        return listOf(
            GapData("Current", scores.demand, 100 - scores.competition),
            GapData("6 months", (scores.demand * 1.1).toInt(), (100 - scores.competition) + 10),
            GapData("12 months", (scores.demand * 1.2).toInt(), (100 - scores.competition) + 20)
        )
    }
    
    fun buildTrendSeries(scores: Scores): List<TrendData> {
        val baseDemand = scores.demand
        return listOf(
            TrendData("Jan", baseDemand),
            TrendData("Feb", (baseDemand * 0.95).toInt()),
            TrendData("Mar", (baseDemand * 1.05).toInt()),
            TrendData("Apr", (baseDemand * 1.1).toInt()),
            TrendData("May", (baseDemand * 1.15).toInt()),
            TrendData("Jun", (baseDemand * 1.2).toInt()),
            TrendData("Jul", (baseDemand * 1.1).toInt()),
            TrendData("Aug", (baseDemand * 1.05).toInt()),
            TrendData("Sep", (baseDemand * 1.0).toInt()),
            TrendData("Oct", (baseDemand * 1.1).toInt()),
            TrendData("Nov", (baseDemand * 1.15).toInt()),
            TrendData("Dec", (baseDemand * 1.2).toInt())
        )
    }
    
    fun inferRiskFactors(scores: Scores): List<String> {
        val risks = mutableListOf<String>()
        
        if (scores.risk > 60) {
            risks.add("High operational uncertainty")
        }
        if (scores.competition > 70) {
            risks.add("Saturated market with strong competition")
        }
        if (scores.demand < 50) {
            risks.add("Limited customer base in the area")
        }
        if (scores.risk > 50 && scores.competition > 50) {
            risks.add("Seasonal demand fluctuations")
        }
        
        if (risks.isEmpty()) {
            risks.add("Low risk profile - good market conditions")
        }
        
        return risks
    }
    
    fun mockDemographics(): List<DemographicData> {
        return listOf(
            DemographicData("Age 18-25", "45%"),
            DemographicData("Age 26-35", "35%"),
            DemographicData("Students", "60%"),
            DemographicData("Working Professionals", "40%"),
            DemographicData("Average Income", "₹25,000-50,000")
        )
    }
    
    fun mockSpending(): List<SpendingData> {
        return listOf(
            SpendingData("Food & Beverage", "₹800-1,200/month"),
            SpendingData("Entertainment", "₹500-800/month"),
            SpendingData("Study Materials", "₹300-500/month"),
            SpendingData("Transportation", "₹400-600/month")
        )
    }
}


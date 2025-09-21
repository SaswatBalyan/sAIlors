package com.example.sailor.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.LocationOn
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.sailor.R
import com.example.sailor.data.ProjectType
import com.example.sailor.data.ScenarioData

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ScenarioFormScreen(
    onBackClick: () -> Unit,
    onSubmit: (ScenarioData) -> Unit,
    isLoading: Boolean = false
) {
    var projectType by remember { mutableStateOf(ProjectType.CAFE) }
    var city by remember { mutableStateOf("Vellore") }
    var address by remember { mutableStateOf("") }
    var budgetInLakh by remember { mutableStateOf("10") }
    var seatingCapacity by remember { mutableStateOf("30") }
    var openHours by remember { mutableStateOf("08:00-22:00") }
    var lat by remember { mutableStateOf("12.9698") }
    var lon by remember { mutableStateOf("79.1559") }
    var radiusM by remember { mutableStateOf("500") }
    var usePopulationDensity by remember { mutableStateOf(true) }
    var considerCompetition by remember { mutableStateOf(true) }
    var notes by remember { mutableStateOf("Target students near PRP block; affordable breakfast menu.") }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                brush = Brush.radialGradient(
                    colors = listOf(
                        Color(0xFF9438F5).copy(alpha = 0.3f),
                        Color(0xFF6366F1).copy(alpha = 0.2f),
                        Color.Transparent
                    ),
                    radius = 800f
                )
            )
    ) {
        Column(
            modifier = Modifier.fillMaxSize()
        ) {
            // Top App Bar
            TopAppBar(
                title = {
                    Text(
                        text = stringResource(R.string.analyze_title),
                        color = Color.White,
                        fontWeight = FontWeight.Bold
                    )
                },
                navigationIcon = {
                    IconButton(onClick = onBackClick) {
                        Icon(
                            imageVector = Icons.Default.ArrowBack,
                            contentDescription = "Back",
                            tint = Color.White
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color.Transparent
                )
            )

            // Content
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
                    .padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                // Header
                Text(
                    text = stringResource(R.string.analyze_subtitle),
                    color = Color.White.copy(alpha = 0.7f),
                    fontSize = 16.sp,
                    modifier = Modifier.padding(bottom = 8.dp)
                )

                // Form Card
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(
                        containerColor = Color.White.copy(alpha = 0.05f)
                    ),
                    shape = RoundedCornerShape(16.dp)
                ) {
                    Column(
                        modifier = Modifier.padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        // Project Type
                        Column {
                            Text(
                                text = stringResource(R.string.project_type),
                                color = Color.White,
                                fontWeight = FontWeight.Medium
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            var expanded by remember { mutableStateOf(false) }
                            ExposedDropdownMenuBox(
                                expanded = expanded,
                                onExpandedChange = { expanded = !expanded }
                            ) {
                                OutlinedTextField(
                                    value = projectType.displayName,
                                    onValueChange = {},
                                    readOnly = true,
                                    trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .menuAnchor(),
                                    colors = OutlinedTextFieldDefaults.colors(
                                        focusedTextColor = Color.White,
                                        unfocusedTextColor = Color.White,
                                        focusedBorderColor = Color(0xFF8B5CF6),
                                        unfocusedBorderColor = Color.White.copy(alpha = 0.3f)
                                    )
                                )
                                ExposedDropdownMenu(
                                    expanded = expanded,
                                    onDismissRequest = { expanded = false }
                                ) {
                                    ProjectType.values().forEach { type ->
                                        DropdownMenuItem(
                                            text = { Text(type.displayName, color = Color.Black) },
                                            onClick = {
                                                projectType = type
                                                expanded = false
                                            }
                                        )
                                    }
                                }
                            }
                        }

                        // City and Address
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            OutlinedTextField(
                                value = city,
                                onValueChange = { city = it },
                                label = { Text(stringResource(R.string.city), color = Color.White.copy(alpha = 0.7f)) },
                                modifier = Modifier.weight(1f),
                                colors = OutlinedTextFieldDefaults.colors(
                                    focusedTextColor = Color.White,
                                    unfocusedTextColor = Color.White,
                                    focusedBorderColor = Color(0xFF8B5CF6),
                                    unfocusedBorderColor = Color.White.copy(alpha = 0.3f)
                                )
                            )
                        }

                        OutlinedTextField(
                            value = address,
                            onValueChange = { address = it },
                            label = { Text(stringResource(R.string.address), color = Color.White.copy(alpha = 0.7f)) },
                            modifier = Modifier.fillMaxWidth(),
                            colors = OutlinedTextFieldDefaults.colors(
                                focusedTextColor = Color.White,
                                unfocusedTextColor = Color.White,
                                focusedBorderColor = Color(0xFF8B5CF6),
                                unfocusedBorderColor = Color.White.copy(alpha = 0.3f)
                            )
                        )

                        // Budget and Capacity
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            OutlinedTextField(
                                value = budgetInLakh,
                                onValueChange = { budgetInLakh = it },
                                label = { Text(stringResource(R.string.budget), color = Color.White.copy(alpha = 0.7f)) },
                                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                                modifier = Modifier.weight(1f),
                                colors = OutlinedTextFieldDefaults.colors(
                                    focusedTextColor = Color.White,
                                    unfocusedTextColor = Color.White,
                                    focusedBorderColor = Color(0xFF8B5CF6),
                                    unfocusedBorderColor = Color.White.copy(alpha = 0.3f)
                                )
                            )
                            OutlinedTextField(
                                value = seatingCapacity,
                                onValueChange = { seatingCapacity = it },
                                label = { Text(stringResource(R.string.capacity), color = Color.White.copy(alpha = 0.7f)) },
                                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                                modifier = Modifier.weight(1f),
                                colors = OutlinedTextFieldDefaults.colors(
                                    focusedTextColor = Color.White,
                                    unfocusedTextColor = Color.White,
                                    focusedBorderColor = Color(0xFF8B5CF6),
                                    unfocusedBorderColor = Color.White.copy(alpha = 0.3f)
                                )
                            )
                        }

                        // Open Hours
                        OutlinedTextField(
                            value = openHours,
                            onValueChange = { openHours = it },
                            label = { Text(stringResource(R.string.open_hours), color = Color.White.copy(alpha = 0.7f)) },
                            modifier = Modifier.fillMaxWidth(),
                            colors = OutlinedTextFieldDefaults.colors(
                                focusedTextColor = Color.White,
                                unfocusedTextColor = Color.White,
                                focusedBorderColor = Color(0xFF8B5CF6),
                                unfocusedBorderColor = Color.White.copy(alpha = 0.3f)
                            )
                        )

                        // Location Section
                        Text(
                            text = "Location Details",
                            color = Color.White,
                            fontWeight = FontWeight.Medium,
                            fontSize = 16.sp
                        )

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            OutlinedTextField(
                                value = lat,
                                onValueChange = { lat = it },
                                label = { Text(stringResource(R.string.latitude), color = Color.White.copy(alpha = 0.7f)) },
                                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                                modifier = Modifier.weight(1f),
                                colors = OutlinedTextFieldDefaults.colors(
                                    focusedTextColor = Color.White,
                                    unfocusedTextColor = Color.White,
                                    focusedBorderColor = Color(0xFF8B5CF6),
                                    unfocusedBorderColor = Color.White.copy(alpha = 0.3f)
                                )
                            )
                            OutlinedTextField(
                                value = lon,
                                onValueChange = { lon = it },
                                label = { Text(stringResource(R.string.longitude), color = Color.White.copy(alpha = 0.7f)) },
                                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                                modifier = Modifier.weight(1f),
                                colors = OutlinedTextFieldDefaults.colors(
                                    focusedTextColor = Color.White,
                                    unfocusedTextColor = Color.White,
                                    focusedBorderColor = Color(0xFF8B5CF6),
                                    unfocusedBorderColor = Color.White.copy(alpha = 0.3f)
                                )
                            )
                        }

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            OutlinedTextField(
                                value = radiusM,
                                onValueChange = { radiusM = it },
                                label = { Text(stringResource(R.string.radius), color = Color.White.copy(alpha = 0.7f)) },
                                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                                modifier = Modifier.weight(1f),
                                colors = OutlinedTextFieldDefaults.colors(
                                    focusedTextColor = Color.White,
                                    unfocusedTextColor = Color.White,
                                    focusedBorderColor = Color(0xFF8B5CF6),
                                    unfocusedBorderColor = Color.White.copy(alpha = 0.3f)
                                )
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Button(
                                onClick = { /* TODO: Implement location request */ },
                                colors = ButtonDefaults.buttonColors(
                                    containerColor = Color(0xFF8B5CF6)
                                ),
                                shape = RoundedCornerShape(8.dp)
                            ) {
                                Icon(
                                    imageVector = Icons.Default.LocationOn,
                                    contentDescription = null,
                                    modifier = Modifier.size(16.dp)
                                )
                                Spacer(modifier = Modifier.width(4.dp))
                                Text(
                                    text = stringResource(R.string.use_my_location),
                                    fontSize = 12.sp
                                )
                            }
                        }

                        // Toggles
                        Card(
                            colors = CardDefaults.cardColors(
                                containerColor = Color.White.copy(alpha = 0.05f)
                            ),
                            shape = RoundedCornerShape(12.dp)
                        ) {
                            Column(
                                modifier = Modifier.padding(16.dp),
                                verticalArrangement = Arrangement.spacedBy(16.dp)
                            ) {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Column(modifier = Modifier.weight(1f)) {
                                        Text(
                                            text = stringResource(R.string.population_density),
                                            color = Color.White,
                                            fontWeight = FontWeight.Medium
                                        )
                                        Text(
                                            text = "Include raster/TIF layer in backend.",
                                            color = Color.White.copy(alpha = 0.5f),
                                            fontSize = 12.sp
                                        )
                                    }
                                    Switch(
                                        checked = usePopulationDensity,
                                        onCheckedChange = { usePopulationDensity = it },
                                        colors = SwitchDefaults.colors(
                                            checkedThumbColor = Color(0xFF8B5CF6),
                                            checkedTrackColor = Color(0xFF8B5CF6).copy(alpha = 0.5f)
                                        )
                                    )
                                }

                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Column(modifier = Modifier.weight(1f)) {
                                        Text(
                                            text = stringResource(R.string.consider_competition),
                                            color = Color.White,
                                            fontWeight = FontWeight.Medium
                                        )
                                        Text(
                                            text = "Include POIs like cafes/gyms nearby.",
                                            color = Color.White.copy(alpha = 0.5f),
                                            fontSize = 12.sp
                                        )
                                    }
                                    Switch(
                                        checked = considerCompetition,
                                        onCheckedChange = { considerCompetition = it },
                                        colors = SwitchDefaults.colors(
                                            checkedThumbColor = Color(0xFF8B5CF6),
                                            checkedTrackColor = Color(0xFF8B5CF6).copy(alpha = 0.5f)
                                        )
                                    )
                                }
                            }
                        }

                        // Notes
                        OutlinedTextField(
                            value = notes,
                            onValueChange = { notes = it },
                            label = { Text(stringResource(R.string.notes), color = Color.White.copy(alpha = 0.7f)) },
                            modifier = Modifier.fillMaxWidth(),
                            minLines = 3,
                            colors = OutlinedTextFieldDefaults.colors(
                                focusedTextColor = Color.White,
                                unfocusedTextColor = Color.White,
                                focusedBorderColor = Color(0xFF8B5CF6),
                                unfocusedBorderColor = Color.White.copy(alpha = 0.3f)
                            )
                        )

                        // Submit Button
                        Button(
                            onClick = {
                                val scenario = ScenarioData(
                                    projectType = projectType,
                                    city = city,
                                    address = address.ifEmpty { null },
                                    budgetInLakh = budgetInLakh.toDoubleOrNull() ?: 10.0,
                                    seatingCapacity = seatingCapacity.toIntOrNull() ?: 30,
                                    openHours = openHours.ifEmpty { null },
                                    lat = lat.toDoubleOrNull() ?: 12.9698,
                                    lon = lon.toDoubleOrNull() ?: 79.1559,
                                    radiusM = radiusM.toIntOrNull() ?: 500,
                                    usePopulationDensity = usePopulationDensity,
                                    considerCompetition = considerCompetition,
                                    notes = notes.ifEmpty { null }
                                )
                                onSubmit(scenario)
                            },
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(48.dp),
                            enabled = !isLoading,
                            colors = ButtonDefaults.buttonColors(
                                containerColor = Color(0xFF8B5CF6)
                            ),
                            shape = RoundedCornerShape(24.dp)
                        ) {
                            if (isLoading) {
                                CircularProgressIndicator(
                                    modifier = Modifier.size(20.dp),
                                    color = Color.White
                                )
                            } else {
                                Text(
                                    text = stringResource(R.string.analyze_feasibility),
                                    color = Color.White,
                                    fontWeight = FontWeight.Medium
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}


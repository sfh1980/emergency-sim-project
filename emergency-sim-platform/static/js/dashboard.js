// Emergency Services Dashboard JavaScript

// Global variables
let selectedIncidentId = null;
let autoRefreshInterval = null;

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚨 Emergency Services Dashboard initialized');
    loadIncidents();
    startAutoRefresh();
});

/**
 * Load incidents from the API and display them in the table
 */
function loadIncidents() {
    console.log('🔄 Loading incidents...');
    
    // Show loading state
    const tbody = document.getElementById('incidentsBody');
    tbody.innerHTML = '<tr><td colspan="6" class="loading">Loading incidents...</td></tr>';
    
    fetch('/api/incidents')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(incidents => {
            displayIncidents(incidents);
            console.log(`✅ Loaded ${incidents.length} incidents`);
        })
        .catch(error => {
            console.error('❌ Error loading incidents:', error);
            tbody.innerHTML = '<tr><td colspan="6" style="color: red; text-align: center;">Error loading incidents</td></tr>';
        });
}

/**
 * Display incidents in the table
 */
function displayIncidents(incidents) {
    const tbody = document.getElementById('incidentsBody');
    tbody.innerHTML = '';
    
    if (incidents.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: #666;">No incidents found</td></tr>';
        return;
    }
    
    incidents.forEach(incident => {
        const row = document.createElement('tr');
        row.className = 'incident-row';
        row.dataset.incidentId = incident.id;
        
        row.innerHTML = `
            <td><strong>${incident.id}</strong></td>
            <td>${escapeHtml(incident.caller)}</td>
            <td>${escapeHtml(incident.type)}</td>
            <td class="priority-${incident.priority}">${incident.priority}</td>
            <td>${escapeHtml(incident.status)}</td>
            <td>${formatTimestamp(incident.timestamp)}</td>
        `;
        
        // Add click event to load incident details
        row.addEventListener('click', function() {
            selectIncident(incident.id);
        });
        
        tbody.appendChild(row);
    });
    
    // If we had a previously selected incident, try to maintain selection
    if (selectedIncidentId) {
        const selectedRow = document.querySelector(`[data-incident-id="${selectedIncidentId}"]`);
        if (selectedRow) {
            selectedRow.classList.add('selected');
        }
    }
}

/**
 * Select an incident and load its details
 */
function selectIncident(incidentId) {
    console.log(`📋 Selecting incident: ${incidentId}`);
    
    // Update visual selection
    document.querySelectorAll('.incident-row').forEach(row => {
        row.classList.remove('selected');
    });
    
    const selectedRow = document.querySelector(`[data-incident-id="${incidentId}"]`);
    if (selectedRow) {
        selectedRow.classList.add('selected');
    }
    
    selectedIncidentId = incidentId;
    loadIncidentDetails(incidentId);
}

/**
 * Load detailed information for a specific incident
 */
function loadIncidentDetails(incidentId) {
    console.log(`📊 Loading details for incident: ${incidentId}`);
    
    const detailsDiv = document.getElementById('incidentDetails');
    detailsDiv.innerHTML = '<div class="loading">Loading incident details...</div>';
    
    fetch(`/api/incident/${incidentId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(details => {
            displayIncidentDetails(details);
            console.log('✅ Incident details loaded');
        })
        .catch(error => {
            console.error('❌ Error loading incident details:', error);
            detailsDiv.innerHTML = '<p style="color: red;">Error loading incident details</p>';
        });
}

/**
 * Display incident details in the details panel
 */
function displayIncidentDetails(details) {
    const detailsDiv = document.getElementById('incidentDetails');
    
    if (!details) {
        detailsDiv.innerHTML = '<p style="color: #666;">No details found for this incident</p>';
        return;
    }
    
    const vitalSigns = details.emergency_details?.vital_signs || {};
    const patientCondition = details.patient_condition || {};
    
    detailsDiv.innerHTML = `
        <h3>🚨 Incident ${details.incident_id}</h3>
        
        <div class="detail-section">
            <h4>👤 Caller Information</h4>
            <p><strong>Name:</strong> ${escapeHtml(details.caller_info?.name || 'N/A')}</p>
            <p><strong>Age:</strong> ${details.caller_info?.age || 'N/A'} years old</p>
            <p><strong>Sex:</strong> ${escapeHtml(details.caller_info?.sex || 'N/A')}</p>
            <p><strong>Medical History:</strong> ${escapeHtml(details.caller_info?.medical_history || 'N/A')}</p>
        </div>
        
        <div class="detail-section">
            <h4>🚑 Emergency Details</h4>
            <p><strong>Type:</strong> ${escapeHtml(details.emergency_details?.type || 'N/A')}</p>
            <p><strong>Priority:</strong> <span class="priority-${details.emergency_details?.priority || 3}">${details.emergency_details?.priority || 'N/A'}</span></p>
            <p><strong>Symptoms:</strong> ${escapeHtml((details.emergency_details?.symptoms || []).join(', ') || 'N/A')}</p>
        </div>
        
        <div class="detail-section">
            <h4>📍 Location</h4>
            <p><strong>Address:</strong> ${escapeHtml(details.location?.address || 'N/A')}</p>
        </div>
        
        <div class="detail-section">
            <h4>💓 Vital Signs</h4>
            <p><strong>Blood Pressure:</strong> ${escapeHtml(vitalSigns.blood_pressure || 'N/A')}</p>
            <p><strong>Heart Rate:</strong> ${vitalSigns.heart_rate || 'N/A'} bpm</p>
            <p><strong>Temperature:</strong> ${vitalSigns.temperature || 'N/A'}°F</p>
            <p><strong>Oxygen Saturation:</strong> ${vitalSigns.oxygen_saturation || 'N/A'}%</p>
        </div>
        
        <div class="detail-section">
            <h4>🏥 Patient Condition</h4>
            <p><strong>Mental Status:</strong> ${escapeHtml(patientCondition.mental_status || 'N/A')}</p>
            <p><strong>Pain Level:</strong> ${escapeHtml(patientCondition.pain_level || 'N/A')}</p>
            <p><strong>Conscious:</strong> ${patientCondition.conscious ? 'Yes' : 'No'}</p>
        </div>
        
        <div class="detail-section">
            <h4>📝 Operator Notes</h4>
            <p>${escapeHtml(details.operator_notes || 'No notes available')}</p>
        </div>
        
        <div class="detail-section">
            <h4>⏰ Timestamps</h4>
            <p><strong>Call Time:</strong> ${formatTimestamp(details.call_timestamp)}</p>
            <p><strong>Created:</strong> ${formatTimestamp(details.created_at)}</p>
        </div>
    `;
}

/**
 * Start automatic refresh of incident data
 */
function startAutoRefresh() {
    // Clear any existing interval
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
    
    // Refresh every 30 seconds
    autoRefreshInterval = setInterval(() => {
        console.log('🔄 Auto-refreshing incidents...');
        loadIncidents();
    }, 30000);
    
    console.log('⏰ Auto-refresh started (30 second intervals)');
}

/**
 * Stop automatic refresh
 */
function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
        console.log('⏹️ Auto-refresh stopped');
    }
}

/**
 * Format timestamp for display
 */
function formatTimestamp(timestamp) {
    if (!timestamp) return 'N/A';
    
    try {
        const date = new Date(timestamp);
        return date.toLocaleString();
    } catch (error) {
        return 'Invalid date';
    }
}

/**
 * Escape HTML to prevent XSS attacks
 */
function escapeHtml(text) {
    if (!text) return '';
    
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Handle page visibility changes to pause/resume auto-refresh
 */
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        console.log('📱 Page hidden, pausing auto-refresh');
        stopAutoRefresh();
    } else {
        console.log('📱 Page visible, resuming auto-refresh');
        startAutoRefresh();
    }
});

// Export functions for global access
window.loadIncidents = loadIncidents;
window.selectIncident = selectIncident;

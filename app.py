import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
from models.symptom_analyzer import LightweightSymptomAnalyzer
from models.image_analyzer import LightweightImageAnalyzer

# Configure Streamlit page
st.set_page_config(
    page_title="Healthcare Triage System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .priority-critical {
        background-color: #ff4444;
        color: white;
        padding: 0.5rem;
        border-radius: 0.5rem;
        text-align: center;
        font-weight: bold;
    }
    .priority-urgent {
        background-color: #ff8800;
        color: white;
        padding: 0.5rem;
        border-radius: 0.5rem;
        text-align: center;
        font-weight: bold;
    }
    .priority-moderate {
        background-color: #ffaa00;
        color: white;
        padding: 0.5rem;
        border-radius: 0.5rem;
        text-align: center;
        font-weight: bold;
    }
    .priority-low {
        background-color: #00aa00;
        color: white;
        padding: 0.5rem;
        border-radius: 0.5rem;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize analyzers
@st.cache_resource
def load_analyzers():
    return LightweightSymptomAnalyzer(), LightweightImageAnalyzer()

symptom_analyzer, image_analyzer = load_analyzers()

# Main application
def main():
    st.markdown('<h1 class="main-header">🏥 Healthcare Triage System</h1>', unsafe_allow_html=True)
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose Analysis Type", 
                               ["Symptom Analysis", "Image Analysis", "Patient Dashboard", "System Analytics"])
    
    if page == "Symptom Analysis":
        symptom_analysis_page()
    elif page == "Image Analysis":
        image_analysis_page()
    elif page == "Patient Dashboard":
        patient_dashboard_page()
    else:
        analytics_page()

def symptom_analysis_page():
    st.header("🩺 Symptom Analysis & Triage")
    
    # Patient information
    col1, col2 = st.columns(2)
    with col1:
        patient_name = st.text_input("Patient Name", placeholder="Enter patient name")
        patient_age = st.number_input("Age", min_value=0, max_value=120, value=30)
    
    with col2:
        patient_gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
        emergency_contact = st.text_input("Emergency Contact", placeholder="Phone number")
    
    # Symptom input
    st.subheader("Describe Symptoms")
    symptom_text = st.text_area(
        "Please describe your symptoms in detail:",
        placeholder="Example: I have been experiencing chest pain and difficulty breathing for the past 2 hours...",
        height=150
    )
    
    # Additional information
    col1, col2 = st.columns(2)
    with col1:
        pain_scale = st.slider("Pain Level (1-10)", 1, 10, 5)
        duration = st.selectbox("Symptom Duration", 
                               ["Less than 1 hour", "1-6 hours", "6-24 hours", "1-3 days", "More than 3 days"])
    
    with col2:
        medical_history = st.text_area("Relevant Medical History", 
                                     placeholder="Previous conditions, medications, allergies...",
                                     height=100)
    
    if st.button("🔍 Analyze Symptoms", type="primary"):
        if symptom_text.strip():
            with st.spinner("Analyzing symptoms..."):
                # Simulate processing time
                time.sleep(1)
                
                # Analyze symptoms
                results = symptom_analyzer.analyze_symptoms(symptom_text)
                
                # Adjust severity based on pain scale
                adjusted_severity = min(results['severity_score'] + (pain_scale - 5) * 0.5, 10)
                results['severity_score'] = adjusted_severity
                results['priority_level'] = symptom_analyzer._calculate_priority(adjusted_severity)
                
                # Display results
                display_symptom_results(results, patient_name, pain_scale)
                
                # Store in session state for dashboard
                if 'patient_records' not in st.session_state:
                    st.session_state.patient_records = []
                
                record = {
                    'timestamp': datetime.now(),
                    'patient_name': patient_name,
                    'age': patient_age,
                    'symptoms': symptom_text,
                    'severity_score': results['severity_score'],
                    'priority': results['priority_level'],
                    'specialty': results['recommended_specialty'],
                    'pain_scale': pain_scale
                }
                st.session_state.patient_records.append(record)
        else:
            st.error("Please describe your symptoms before analyzing.")

def display_symptom_results(results, patient_name, pain_scale):
    st.success("✅ Analysis Complete!")
    
    # Priority alert
    priority = results['priority_level']
    if priority == "CRITICAL":
        st.markdown(f'<div class="priority-critical">🚨 CRITICAL PRIORITY - IMMEDIATE ATTENTION REQUIRED</div>', 
                   unsafe_allow_html=True)
    elif priority == "URGENT":
        st.markdown(f'<div class="priority-urgent">⚡ URGENT PRIORITY - SEEK CARE WITHIN HOURS</div>', 
                   unsafe_allow_html=True)
    elif priority == "MODERATE":
        st.markdown(f'<div class="priority-moderate">📋 MODERATE PRIORITY - SCHEDULE APPOINTMENT</div>', 
                   unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="priority-low">✅ LOW PRIORITY - ROUTINE CARE</div>', 
                   unsafe_allow_html=True)
    
    # Results display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Severity Score", f"{results['severity_score']:.1f}/10", 
                 delta=f"Pain Level: {pain_scale}/10")
    
    with col2:
        st.metric("Confidence", f"{results['confidence_score']:.1f}%")
    
    with col3:
        st.metric("Estimated Wait Time", results['estimated_wait_time'])
    
    # Detailed results
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏥 Recommended Specialty")
        st.info(results['recommended_specialty'])
        
        st.subheader("🎯 Key Symptoms Identified")
        for symptom in results['key_symptoms']:
            st.write(f"• {symptom.title()}")
    
    with col2:
        st.subheader("📋 Recommendations")
        for rec in results['recommendations']:
            st.write(rec)
    
    # Severity visualization
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = results['severity_score'],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Severity Score"},
        delta = {'reference': 5},
        gauge = {
            'axis': {'range': [None, 10]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 3], 'color': "lightgreen"},
                {'range': [3, 6], 'color': "yellow"},
                {'range': [6, 8], 'color': "orange"},
                {'range': [8, 10], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 8
            }
        }
    ))
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

def image_analysis_page():
    st.header("📸 Medical Image Analysis")
    
    st.info("Upload medical images for basic analysis. This tool provides preliminary assessment only.")
    
    # Image upload
    uploaded_file = st.file_uploader("Choose a medical image", 
                                   type=['png', 'jpg', 'jpeg'],
                                   help="Supported formats: PNG, JPG, JPEG")
    
    image_type = st.selectbox("Image Type", ["skin", "wound", "general"])
    
    if uploaded_file is not None:
        # Display uploaded image
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Uploaded Image")
            st.image(uploaded_file, caption="Medical Image", use_column_width=True)
        
        with col2:
            if st.button("🔍 Analyze Image", type="primary"):
                with st.spinner("Analyzing image..."):
                    time.sleep(2)  # Simulate processing
                    
                    # Analyze image
                    results = image_analyzer.analyze_image(uploaded_file, image_type)
                    
                    # Display results
                    display_image_results(results)

def display_image_results(results):
    if 'error' in results:
        st.error(results['error'])
        return
    
    st.success("✅ Image Analysis Complete!")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Confidence Score", f"{results['confidence_score']:.1f}%")
    
    with col2:
        severity = results['analysis_results']['severity_score']
        st.metric("Severity Score", f"{severity:.1f}/10")
    
    with col3:
        review_needed = "Yes" if results['requires_professional_review'] else "No"
        st.metric("Professional Review", review_needed)
    
    # Findings
    st.subheader("🔍 Analysis Findings")
    for finding in results['analysis_results']['findings']:
        st.write(f"• {finding}")
    
    # Recommendations
    st.subheader("📋 Recommendations")
    for rec in results['recommendations']:
        st.write(rec)
    
    # Technical details (expandable)
    with st.expander("Technical Analysis Details"):
        analysis = results['analysis_results']
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Color Analysis:**")
            st.json(analysis['color_analysis'])
        
        with col2:
            st.write("**Texture Analysis:**")
            st.json(analysis['texture_analysis'])

def patient_dashboard_page():
    st.header("👥 Patient Dashboard")
    
    if 'patient_records' not in st.session_state or not st.session_state.patient_records:
        st.info("No patient records available. Analyze some symptoms first!")
        return
    
    records = st.session_state.patient_records
    df = pd.DataFrame(records)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Patients", len(df))
    
    with col2:
        critical_count = len(df[df['priority'] == 'CRITICAL'])
        st.metric("Critical Cases", critical_count)
    
    with col3:
        avg_severity = df['severity_score'].mean()
        st.metric("Avg Severity", f"{avg_severity:.1f}")
    
    with col4:
        urgent_count = len(df[df['priority'].isin(['CRITICAL', 'URGENT'])])
        st.metric("Urgent Cases", urgent_count)
    
    # Priority distribution
    priority_counts = df['priority'].value_counts()
    fig = px.pie(values=priority_counts.values, names=priority_counts.index, 
                title="Priority Distribution")
    st.plotly_chart(fig, use_container_width=True)
    
    # Recent patients table
    st.subheader("Recent Patients")
    display_df = df.sort_values('timestamp', ascending=False).head(10)
    display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
    st.dataframe(display_df[['timestamp', 'patient_name', 'priority', 'severity_score', 'specialty']], 
                use_container_width=True)

def analytics_page():
    st.header("📊 System Analytics")
    
    # System performance metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("System Uptime", "99.9%", delta="0.1%")
    
    with col2:
        st.metric("Avg Response Time", "1.2s", delta="-0.3s")
    
    with col3:
        st.metric("Analysis Accuracy", "87.5%", delta="2.1%")
    
    # Simulated analytics data
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    daily_patients = np.random.poisson(15, len(dates))
    
    analytics_df = pd.DataFrame({
        'date': dates,
        'patients': daily_patients,
        'critical_cases': np.random.poisson(2, len(dates)),
        'avg_severity': np.random.normal(4.5, 1.5, len(dates))
    })
    
    # Patient volume over time
    fig = px.line(analytics_df, x='date', y='patients', 
                 title='Daily Patient Volume')
    st.plotly_chart(fig, use_container_width=True)
    
    # Severity distribution
    fig = px.histogram(analytics_df, x='avg_severity', nbins=20,
                      title='Average Daily Severity Distribution')
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()

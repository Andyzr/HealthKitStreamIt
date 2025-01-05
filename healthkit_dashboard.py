import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import xml.etree.ElementTree as ET

# Configure Streamlit
st.set_page_config(page_title="HealthKit Data Visualization", layout="wide")

# Define HealthKit metrics mapping
HEALTHKIT_METRICS = {
    'Activity': [
        'HKQuantityTypeIdentifierStepCount',
        'HKQuantityTypeIdentifierDistanceWalkingRunning',
        'HKQuantityTypeIdentifierFlightsClimbed',
        'HKQuantityTypeIdentifierActiveEnergyBurned',
        'HKQuantityTypeIdentifierBasalEnergyBurned',
    ],
    'Vital Signs': [
        'HKQuantityTypeIdentifierHeartRate',
        'HKQuantityTypeIdentifierRestingHeartRate',
        'HKQuantityTypeIdentifierHeartRateVariabilitySDNN',
        'HKQuantityTypeIdentifierOxygenSaturation',
        'HKQuantityTypeIdentifierRespiratoryRate',
        'HKQuantityTypeIdentifierBodyTemperature',
        'HKQuantityTypeIdentifierBloodPressureSystolic',
        'HKQuantityTypeIdentifierBloodPressureDiastolic',
    ],
    'Body Measurements': [
        'HKQuantityTypeIdentifierHeight',
        'HKQuantityTypeIdentifierBodyMass',
        'HKQuantityTypeIdentifierBodyFatPercentage',
        'HKQuantityTypeIdentifierLeanBodyMass',
        'HKQuantityTypeIdentifierBodyMassIndex',
    ],
    'Sleep': [
        'HKCategoryTypeIdentifierSleepAnalysis',
    ],
    'Nutrition': [
        'HKQuantityTypeIdentifierDietaryWater',
        'HKQuantityTypeIdentifierDietaryEnergyConsumed',
        'HKQuantityTypeIdentifierDietaryProtein',
        'HKQuantityTypeIdentifierDietaryFatTotal',
        'HKQuantityTypeIdentifierDietaryCarbohydrates',
    ],
    'Mindfulness': [
        'HKCategoryTypeIdentifierMindfulSession',
    ]
}

def parse_healthkit_export(uploaded_file):
    """Parse Apple HealthKit export XML file and return formatted DataFrame."""
    try:
        tree = ET.parse(uploaded_file)
        root = tree.getroot()
        
        records = []
        # Flatten the metrics list for searching
        all_metrics = [metric for category in HEALTHKIT_METRICS.values() for metric in category]
        
        for record in root.findall('.//Record'):
            record_type = record.get('type')
            if record_type in all_metrics:
                try:
                    value = float(record.get('value'))
                    records.append({
                        'type': record_type,
                        'value': value,
                        'unit': record.get('unit'),
                        'date': datetime.strptime(record.get('startDate'), '%Y-%m-%d %H:%M:%S %z'),
                        'category': next(cat for cat, metrics in HEALTHKIT_METRICS.items() 
                                      if record_type in metrics)
                    })
                except (ValueError, TypeError):
                    # Skip records with non-numeric values
                    continue
                    
        return pd.DataFrame(records)
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None

def create_visualization(df, metric_type, date_range):
    """Create appropriate visualization based on metric type."""
    filtered_df = df[
        (df['type'] == metric_type) &
        (df['date'].dt.date >= date_range[0]) &
        (df['date'].dt.date <= date_range[1])
    ]
    
    # Aggregate data based on metric type
    if 'HeartRate' in metric_type:
        # For heart rate, show daily min, max, and average
        daily_data = filtered_df.groupby(filtered_df['date'].dt.date).agg({
            'value': ['mean', 'min', 'max']
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily_data['date'], y=daily_data['value']['mean'],
                               name='Average', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=daily_data['date'], y=daily_data['value']['max'],
                               name='Maximum', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=daily_data['date'], y=daily_data['value']['min'],
                               name='Minimum', line=dict(color='green')))
    else:
        # For other metrics, show daily totals or averages
        agg_func = 'sum' if any(keyword in metric_type for keyword in ['StepCount', 'Distance', 'Energy']) else 'mean'
        daily_data = filtered_df.groupby(filtered_df['date'].dt.date).agg({
            'value': agg_func
        }).reset_index()
        
        fig = px.line(daily_data, x='date', y='value',
                     title=f'Daily {metric_type.split("Identifier")[1]} Over Time')
    
    fig.update_layout(height=500)
    return fig, daily_data

def main():
    st.title('Enhanced Apple HealthKit Data Visualization')
    
    st.info("Upload your Apple HealthKit export file (size limit is set in config.toml)")
    uploaded_file = st.file_uploader("Upload your Apple HealthKit export (XML)", type=['xml'])
    
    if uploaded_file:
        with st.spinner('Processing your HealthKit data... This might take a moment for large files.'):
            df = parse_healthkit_export(uploaded_file)
            
        if df is not None and not df.empty:
            # Sidebar filters
            st.sidebar.header('Filters')
            
            # Category and metric selection
            category = st.sidebar.selectbox('Select Category', list(HEALTHKIT_METRICS.keys()))
            available_metrics = [metric for metric in HEALTHKIT_METRICS[category] 
                               if metric in df['type'].unique()]
            
            if available_metrics:
                metric_type = st.sidebar.selectbox('Select Metric', available_metrics)
                
                # Date range filter
                date_range = st.sidebar.date_input(
                    'Select Date Range',
                    [df['date'].min(), df['date'].max()]
                )
                
                # Create and display visualization
                fig, daily_data = create_visualization(df, metric_type, date_range)
                st.plotly_chart(fig, use_container_width=True)
                
                # Display summary statistics
                st.subheader('Summary Statistics')
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric('Average', f"{daily_data['value'].mean():.1f}")
                with col2:
                    st.metric('Maximum', f"{daily_data['value'].max():.1f}")
                with col3:
                    st.metric('Minimum', f"{daily_data['value'].min():.1f}")
                with col4:
                    st.metric('Total Days', len(daily_data))
                
                # Display raw data
                st.subheader('Raw Data')
                st.dataframe(daily_data)
            else:
                st.warning(f"No data available for the selected category: {category}")
                st.write("Available categories in your data:", df['category'].unique())
                
if __name__ == '__main__':
    main()
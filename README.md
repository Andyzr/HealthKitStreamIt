# HealthKit Data Visualization Dashboard

A Streamlit application that visualizes Apple HealthKit exported data, providing interactive analysis and insights into your health metrics.

[Demo](https://healthkitstreamit-andyzr.streamlit.app/)

## Features

- Support for multiple health metrics categories:
  - Activity (steps, distance, flights climbed)
  - Vital Signs (heart rate, blood pressure, respiratory rate)
  - Body Measurements (weight, height, BMI)
  - Sleep Analysis
  - Nutrition (water, energy, macronutrients)
  - Mindfulness
- Interactive date range filtering
- Daily trend visualization
- Summary statistics
- Raw data export capabilities
- Support for large HealthKit export files (up to 500MB)

## Prerequisites

- Python 3.8 or higher
- Apple Health data export from your iOS device

### How to Export Your HealthKit Data

1. Open the Health app on your iPhone
2. Tap your profile picture/icon
3. Scroll down and tap "Export All Health Data"
4. Choose a location to save the exported zip file
5. Extract the zip file and locate the `export.xml` file

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Andyzr/HealthKitStreamIt.git
cd HealthKitStreamIt
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create the configuration directory and file for handling large files:
```bash
mkdir -p .streamlit
```

5. Create `.streamlit/config.toml` with the following content:
```toml
[server]
maxUploadSize = 500
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run healthkit_dashboard.py
```

2. Open your web browser and navigate to the provided URL (typically `http://localhost:8501`)

3. Upload your HealthKit export file (XML format)

4. Use the sidebar to:
   - Select health metric categories
   - Choose specific metrics to visualize
   - Set date ranges for analysis

5. Interact with the visualizations and view summary statistics

## Files Structure

```
healthkit-dashboard/
├── .streamlit/
│   └── config.toml
├── requirements.txt
├── healthkit_dashboard.py
└── README.md
```

## Dependencies

```
streamlit==1.29.0
pandas==2.0.3
plotly==5.18.0
numpy==1.24.3
```

## Troubleshooting

### Common Issues

1. **File Size Error**
   - Ensure you have the `.streamlit/config.toml` file properly configured
   - Try reducing the date range in your Health app export

2. **XML Parsing Error**
   - Make sure you're uploading the correct export file
   - Verify the file isn't corrupted during export/transfer

3. **No Data Available**
   - Confirm that you have recorded data for the selected metrics
   - Check the date range filter settings

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

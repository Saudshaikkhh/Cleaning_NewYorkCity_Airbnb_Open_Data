# Airbnb NYC 2019 Data Analysis

A comprehensive data analysis and visualization tool for processing Airbnb rental data from New York City (2019). This project provides automated data cleaning, validation, and visualization capabilities to help understand rental patterns, pricing trends, and geographical distribution of Airbnb listings.

## Project Overview

This Python-based analysis tool processes raw Airbnb data from NYC 2019, performs comprehensive data cleaning operations, and generates detailed visualizations to reveal insights about the rental market. The tool is designed to handle real-world data challenges including missing values, outliers, and data quality issues commonly found in rental listing datasets.

## Key Features

### Data Processing Capabilities
- **Automated Data Loading**: Seamlessly loads CSV data with initial exploration and profiling
- **Comprehensive Data Cleaning**: Handles missing values, standardizes text formatting, and validates data integrity
- **Geographic Validation**: Filters listings to ensure they fall within NYC geographical boundaries
- **Outlier Detection**: Identifies and handles unrealistic pricing and booking requirements
- **Duplicate Removal**: Ensures data uniqueness and integrity

### Data Quality Improvements
- **Missing Value Handling**: Fills missing property names and host information with appropriate defaults
- **Date Standardization**: Converts review dates to proper datetime format with error handling
- **Text Normalization**: Standardizes neighborhood and room type formatting for consistency
- **Price Filtering**: Removes unrealistic pricing outliers (>$1000/night) to improve analysis accuracy
- **Booking Validation**: Filters extreme minimum night requirements (>365 days)

### Visualization Suite
- **Price Distribution Analysis**: Histogram with kernel density estimation showing pricing patterns
- **Room Type Breakdown**: Count plots displaying the distribution of different accommodation types
- **Neighborhood Popularity**: Horizontal bar chart highlighting the top 10 most popular neighborhoods
- **Geographic Price Mapping**: Scatter plot visualization showing price distribution across NYC geography

## Technical Requirements

### Dependencies
```
pandas >= 1.3.0
matplotlib >= 3.5.0
seaborn >= 0.11.0
numpy >= 1.21.0
```

### System Requirements
- Python 3.7 or higher
- Minimum 4GB RAM for processing large datasets
- At least 500MB free disk space for output files

## Installation and Setup

1. **Clone or download the project files**
2. **Install required dependencies**:
   ```bash
   pip install pandas matplotlib seaborn numpy
   ```
3. **Ensure your data file is named**: `AB_NYC_2019.csv` and placed in the same directory as the script
4. **Run the analysis**:
   ```bash
   python airbnb_analysis.py
   ```

## Input Data Requirements

The script expects a CSV file named `AB_NYC_2019.csv` with the following columns:
- `name`: Property listing name
- `host_name`: Host's name
- `last_review`: Date of last review
- `reviews_per_month`: Average reviews per month
- `room_type`: Type of accommodation
- `neighbourhood_group`: Borough information
- `neighbourhood`: Specific neighborhood
- `minimum_nights`: Minimum booking requirement
- `price`: Nightly price
- `latitude`: Geographic latitude
- `longitude`: Geographic longitude

## Output Structure

The script automatically creates the following directory structure:

```
project_directory/
├── processed_data/
│   └── cleaned_airbnb_data.csv
├── reports/
│   ├── raw_data_visualization.png
│   └── cleaned_data_visualization.png
└── airbnb_analysis.py
```

### Generated Files

**Cleaned Dataset** (`processed_data/cleaned_airbnb_data.csv`)
- Processed and validated data ready for further analysis
- All data quality issues addressed
- Geographic coordinates validated for NYC boundaries

**Visualization Reports**
- `raw_data_visualization.png`: Analysis of original, unprocessed data
- `cleaned_data_visualization.png`: Analysis after data cleaning and validation

## Data Cleaning Process

### Geographic Validation
The script validates that all listings fall within NYC boundaries:
- **Latitude**: 40.5° to 41.0° North
- **Longitude**: -74.5° to -73.0° West

### Price Filtering
- Removes listings with prices exceeding $1,000 per night
- Maintains realistic pricing for analysis accuracy

### Booking Requirements
- Filters out listings requiring more than 365 minimum nights
- Focuses on typical short-term rental patterns

### Missing Data Strategy
- Property names: Replaced with "No Name"
- Host names: Replaced with "Anonymous"
- Review metrics: Missing values set to 0
- Date fields: Invalid dates handled gracefully

## Visualization Details

### Price Distribution
- Histogram with 50 bins showing price frequency
- Kernel density estimation overlay for trend identification
- X-axis limited to $1,000 for clarity

### Room Type Analysis
- Count plot ordered by frequency
- Shows distribution of entire homes, private rooms, and shared spaces

### Neighborhood Ranking
- Horizontal bar chart of top 10 neighborhoods by listing count
- Sorted by popularity for easy identification of hotspots

### Geographic Distribution
- Scatter plot using longitude and latitude coordinates
- Color-coded by price using viridis palette
- Bounded to NYC area for focused analysis

## Usage Examples

### Basic Analysis
```python
# Load and explore data
raw_df = load_and_explore()

# Clean data
raw_df, cleaned_df = clean_data(raw_df)

# Generate visualizations
raw_viz = create_visualizations(raw_df, "Before Cleaning")
cleaned_viz = create_visualizations(cleaned_df, "After Cleaning")
```

### Custom Analysis
The cleaned dataset can be used for additional analysis:
```python
# Load processed data
df = pd.read_csv('processed_data/cleaned_airbnb_data.csv')

# Perform custom analysis
avg_price_by_borough = df.groupby('neighbourhood_group')['price'].mean()
```

## Performance Considerations

- **Memory Usage**: Large datasets may require 2-4GB RAM during processing
- **Processing Time**: Typical runtime 30-60 seconds for 50,000 listings
- **Output Size**: Visualization files are high-resolution (300 DPI) for publication quality

## Troubleshooting

### Common Issues
- **File Not Found**: Ensure `AB_NYC_2019.csv` is in the correct directory
- **Memory Error**: Reduce dataset size or increase available RAM
- **Permission Error**: Ensure write permissions for output directories

### Data Quality Warnings
- **Low Data Retention**: If many rows are removed, check geographic bounds
- **Missing Visualizations**: Verify matplotlib backend compatibility
- **Empty Neighborhoods**: May indicate data quality issues in source file

## Future Enhancements

- **Time Series Analysis**: Seasonal pricing and availability trends
- **Predictive Modeling**: Price prediction based on location and features
- **Interactive Dashboards**: Web-based visualization interface
- **Advanced Filtering**: Custom geographic and price range selections
- **Statistical Testing**: Hypothesis testing for market insights

## License and Usage

This tool is designed for educational and analytical purposes. Ensure compliance with Airbnb's terms of service when using their data. The code is provided as-is for data analysis and visualization purposes.

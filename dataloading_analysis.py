import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set up directories
def setup_directories():
    """Create necessary directories for saving files"""
    directories = ['reports', 'processed_data', 'reports/before_cleaning', 'reports/after_cleaning']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Directories created successfully!")

def load_and_explore_data(file_path):
    """Load CSV data and perform initial exploration"""
    print("📊 PROCESS 1: DATA LOADING AND INITIAL EXPLORATION")
    print("=" * 60)
    
    try:
        # Load the data
        df = pd.read_csv(file_path)
        print(f"✅ Data loaded successfully!")
        print(f"📋 Dataset shape: {df.shape}")
        print(f"📋 Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # Basic info
        print("\n🔍 DATASET OVERVIEW:")
        print("-" * 30)
        print(df.info())
        
        # Missing values analysis
        print("\n❌ MISSING VALUES ANALYSIS:")
        print("-" * 30)
        missing_data = df.isnull().sum()
        missing_percentage = (missing_data / len(df)) * 100
        missing_df = pd.DataFrame({
            'Missing Count': missing_data,
            'Percentage': missing_percentage
        }).sort_values('Missing Count', ascending=False)
        print(missing_df[missing_df['Missing Count'] > 0])
        
        # Basic statistics
        print("\n📈 BASIC STATISTICS:")
        print("-" * 30)
        print(df.describe())
        
        # Data types
        print("\n🏷️ DATA TYPES:")
        print("-" * 30)
        print(df.dtypes)
        
        # Unique values for categorical columns
        categorical_cols = ['room_type', 'neighbourhood_group', 'neighbourhood']
        print("\n🏷️ UNIQUE VALUES IN CATEGORICAL COLUMNS:")
        print("-" * 30)
        for col in categorical_cols:
            if col in df.columns:
                print(f"{col}: {df[col].nunique()} unique values")
                print(f"Top 5: {df[col].value_counts().head().to_dict()}")
                print()
        
        return df
        
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found!")
        print("Please make sure the file exists in the current directory.")
        return None
    except Exception as e:
        print(f"❌ Error loading data: {str(e)}")
        return None

def create_before_cleaning_visualizations(df):
    """Create visualizations before data cleaning"""
    print("\n📊 CREATING BEFORE CLEANING VISUALIZATIONS...")
    print("-" * 50)
    
    # Set up the plotting style
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # Create a comprehensive grid of plots
    fig = plt.figure(figsize=(20, 16))
    fig.suptitle('AIRBNB DATA ANALYSIS - BEFORE CLEANING', fontsize=20, fontweight='bold')
    
    # 1. Price distribution
    plt.subplot(3, 3, 1)
    sns.histplot(df['price'], bins=50, kde=True, alpha=0.7)
    plt.title('Price Distribution (Before Cleaning)', fontweight='bold')
    plt.xlabel('Price ($)')
    plt.ylabel('Frequency')
    
    # 2. Room type distribution
    plt.subplot(3, 3, 2)
    room_counts = df['room_type'].value_counts()
    plt.pie(room_counts.values, labels=room_counts.index, autopct='%1.1f%%')
    plt.title('Room Type Distribution (Before)', fontweight='bold')
    
    # 3. Neighbourhood group distribution
    plt.subplot(3, 3, 3)
    if 'neighbourhood_group' in df.columns:
        neighbourhood_counts = df['neighbourhood_group'].value_counts()
        sns.barplot(x=neighbourhood_counts.values, y=neighbourhood_counts.index)
        plt.title('Neighbourhood Groups (Before)', fontweight='bold')
        plt.xlabel('Count')
    
    # 4. Minimum nights distribution
    plt.subplot(3, 3, 4)
    sns.histplot(df['minimum_nights'], bins=50, kde=True, alpha=0.7)
    plt.title('Minimum Nights Distribution (Before)', fontweight='bold')
    plt.xlabel('Minimum Nights')
    plt.ylabel('Frequency')
    
    # 5. Reviews per month distribution
    plt.subplot(3, 3, 5)
    sns.histplot(df['reviews_per_month'].dropna(), bins=30, kde=True, alpha=0.7)
    plt.title('Reviews per Month (Before)', fontweight='bold')
    plt.xlabel('Reviews per Month')
    plt.ylabel('Frequency')
    
    # 6. Geographic distribution
    plt.subplot(3, 3, 6)
    plt.scatter(df['longitude'], df['latitude'], alpha=0.5, s=1)
    plt.title('Geographic Distribution (Before)', fontweight='bold')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    
    # 7. Price vs Reviews relationship
    plt.subplot(3, 3, 7)
    sns.scatterplot(x='number_of_reviews', y='price', data=df, alpha=0.6)
    plt.title('Price vs Number of Reviews (Before)', fontweight='bold')
    plt.xlabel('Number of Reviews')
    plt.ylabel('Price ($)')
    
    # 8. Host listings distribution
    plt.subplot(3, 3, 8)
    host_counts = df['host_name'].value_counts().head(10)
    sns.barplot(x=host_counts.values, y=host_counts.index)
    plt.title('Top 10 Hosts by Listings (Before)', fontweight='bold')
    plt.xlabel('Number of Listings')
    
    # 9. Availability distribution
    plt.subplot(3, 3, 9)
    sns.histplot(df['availability_365'], bins=30, kde=True, alpha=0.7)
    plt.title('Availability 365 Days (Before)', fontweight='bold')
    plt.xlabel('Available Days')
    plt.ylabel('Frequency')
    
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('reports/before_cleaning/comprehensive_analysis_before.png', 
                dpi=300, bbox_inches='tight')
    plt.show()
    
    # Create additional detailed plots
    create_detailed_before_plots(df)
    
    print("✅ Before cleaning visualizations saved to 'reports/before_cleaning/'")

def create_detailed_before_plots(df):
    """Create additional detailed plots for before cleaning analysis"""
    
    # Price analysis by room type
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 2, 1)
    sns.boxplot(x='room_type', y='price', data=df)
    plt.title('Price Distribution by Room Type (Before)', fontweight='bold')
    plt.xticks(rotation=45)
    
    # Geographic price distribution
    plt.subplot(2, 2, 2)
    scatter = plt.scatter(df['longitude'], df['latitude'], 
                         c=df['price'], cmap='coolwarm', alpha=0.6, s=1)
    plt.colorbar(scatter, label='Price ($)')
    plt.title('Geographic Price Distribution (Before)', fontweight='bold')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    
    # Correlation heatmap
    plt.subplot(2, 2, 3)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    correlation_matrix = df[numeric_cols].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, fmt='.2f')
    plt.title('Correlation Heatmap (Before)', fontweight='bold')
    
    # Missing data visualization
    plt.subplot(2, 2, 4)
    missing_data = df.isnull().sum().sort_values(ascending=False)
    missing_data = missing_data[missing_data > 0]
    if len(missing_data) > 0:
        sns.barplot(x=missing_data.values, y=missing_data.index)
        plt.title('Missing Data Count (Before)', fontweight='bold')
        plt.xlabel('Missing Values Count')
    else:
        plt.text(0.5, 0.5, 'No Missing Data', ha='center', va='center', 
                fontsize=16, transform=plt.gca().transAxes)
        plt.title('Missing Data Count (Before)', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('reports/before_cleaning/detailed_analysis_before.png', 
                dpi=300, bbox_inches='tight')
    plt.show()

def generate_before_cleaning_report(df):
    """Generate a comprehensive report of the data before cleaning"""
    print("\n📋 GENERATING BEFORE CLEANING REPORT...")
    print("-" * 50)
    
    report = []
    report.append("AIRBNB DATA ANALYSIS REPORT - BEFORE CLEANING")
    report.append("=" * 60)
    report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Basic statistics
    report.append("DATASET OVERVIEW:")
    report.append("-" * 20)
    report.append(f"Total records: {len(df):,}")
    report.append(f"Total columns: {len(df.columns)}")
    report.append(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    report.append("")
    
    # Missing data analysis
    report.append("MISSING DATA ANALYSIS:")
    report.append("-" * 20)
    missing_data = df.isnull().sum()
    missing_percentage = (missing_data / len(df)) * 100
    for col, count in missing_data.items():
        if count > 0:
            report.append(f"{col}: {count:,} ({missing_percentage[col]:.2f}%)")
    report.append("")
    
    # Data quality issues
    report.append("DATA QUALITY ISSUES IDENTIFIED:")
    report.append("-" * 30)
    
    # Price outliers
    price_outliers = len(df[df['price'] > 1000])
    report.append(f"Price outliers (>$1000): {price_outliers:,}")
    
    # Minimum nights outliers
    min_nights_outliers = len(df[df['minimum_nights'] > 365])
    report.append(f"Minimum nights outliers (>365): {min_nights_outliers:,}")
    
    # Geographic outliers (assuming NYC bounds)
    geo_outliers = len(df[
        (df['latitude'] < 40.5) | (df['latitude'] > 41) |
        (df['longitude'] < -74.5) | (df['longitude'] > -73)
    ])
    report.append(f"Geographic outliers (outside NYC bounds): {geo_outliers:,}")
    
    # Duplicates
    duplicates = df.duplicated().sum()
    report.append(f"Duplicate records: {duplicates:,}")
    report.append("")
    
    # Statistical summary
    report.append("STATISTICAL SUMMARY:")
    report.append("-" * 20)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        report.append(f"\n{col.upper()}:")
        report.append(f"  Mean: {df[col].mean():.2f}")
        report.append(f"  Median: {df[col].median():.2f}")
        report.append(f"  Std Dev: {df[col].std():.2f}")
        report.append(f"  Min: {df[col].min():.2f}")
        report.append(f"  Max: {df[col].max():.2f}")
    
    # Save report
    with open('reports/before_cleaning/analysis_report_before.txt', 'w') as f:
        f.write('\n'.join(report))
    
    print("✅ Before cleaning report saved to 'reports/before_cleaning/analysis_report_before.txt'")
    return report

def main():
    """Main function to run Process 1"""
    print("🚀 STARTING AIRBNB DATA ANALYSIS PIPELINE")
    print("=" * 60)
    
    # Setup directories
    setup_directories()
    
    # Load and explore data
    file_path = input("Enter the path to your Airbnb CSV file (or press Enter for 'your_airbnb_data.csv'): ").strip()
    if not file_path:
        file_path = 'your_airbnb_data.csv'
    
    df = load_and_explore_data(file_path)
    
    if df is not None:
        # Create before cleaning visualizations
        create_before_cleaning_visualizations(df)
        
        # Generate before cleaning report
        generate_before_cleaning_report(df)
        
        # Save the original data for reference
        df.to_csv('processed_data/original_data.csv', index=False)
        print("✅ Original data saved to 'processed_data/original_data.csv'")
        
        print("\n🎉 PROCESS 1 COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("Next: Run Process 2 for data cleaning and transformation")
        print("File: process2_data_cleaning.py")
        
        return df
    else:
        print("❌ Process 1 failed. Please check your data file and try again.")
        return None

if __name__ == "__main__":
    main()
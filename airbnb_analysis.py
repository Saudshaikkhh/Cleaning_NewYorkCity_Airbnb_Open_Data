import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Create directories if they don't exist
os.makedirs('processed_data', exist_ok=True)
os.makedirs('reports', exist_ok=True)

# Step 1: Data Loading and Initial Exploration
def load_and_explore():
    df = pd.read_csv('AB_NYC_2019.csv')
    print("Initial Data Shape:", df.shape)
    print("\nInitial Data Info:")
    print(df.info())
    return df

# Step 2: Data Cleaning and Processing
def clean_data(df):
    # Create a copy for before/after comparison
    df_cleaned = df.copy()
    
    # 1. Fill missing names
    df_cleaned['name'].fillna('No Name', inplace=True)
    df_cleaned['host_name'].fillna('Anonymous', inplace=True)
    
    # 2. Convert last_review to datetime
    df_cleaned['last_review'] = pd.to_datetime(
        df_cleaned['last_review'], 
        errors='coerce'
    )
    
    # 3. Fill missing reviews
    df_cleaned['reviews_per_month'].fillna(0, inplace=True)
    
    # 4. Standardize text formatting
    text_cols = ['room_type', 'neighbourhood_group', 'neighbourhood']
    for col in text_cols:
        df_cleaned[col] = df_cleaned[col].str.title().str.strip()
    
    # 5. Filter unrealistic values
    df_cleaned = df_cleaned[df_cleaned['minimum_nights'] <= 365]
    df_cleaned = df_cleaned[df_cleaned['price'] <= 1000]
    
    # 6. Validate geo-coordinates (NYC bounds)
    nyc_bounds = {
        'latitude': (40.5, 41),
        'longitude': (-74.5, -73)
    }
    df_cleaned = df_cleaned[
        (df_cleaned['latitude'] >= nyc_bounds['latitude'][0]) &
        (df_cleaned['latitude'] <= nyc_bounds['latitude'][1]) &
        (df_cleaned['longitude'] >= nyc_bounds['longitude'][0]) &
        (df_cleaned['longitude'] <= nyc_bounds['longitude'][1])
    ]
    
    # 7. Remove duplicates
    df_cleaned.drop_duplicates(inplace=True)
    
    # Save cleaned data
    df_cleaned.to_csv('processed_data/cleaned_airbnb_data.csv', index=False)
    return df, df_cleaned

# Step 3: Visualization Functions
def create_visualizations(df, title_suffix):
    fig, axs = plt.subplots(2, 2, figsize=(18, 14))
    fig.suptitle(f'Airbnb Data Analysis - {title_suffix}', fontsize=20)
    
    # Price Distribution
    sns.histplot(df['price'], bins=50, kde=True, ax=axs[0, 0])
    axs[0, 0].set_title('Price Distribution')
    axs[0, 0].set_xlim(0, 1000)
    
    # Room Type Distribution
    sns.countplot(
        x='room_type', 
        data=df, 
        order=df['room_type'].value_counts().index,
        ax=axs[0, 1]
    )
    axs[0, 1].set_title('Room Type Distribution')
    axs[0, 1].tick_params(axis='x', rotation=45)
    
    # Top Neighborhoods
    top_neighborhoods = df['neighbourhood'].value_counts().head(10)
    top_neighborhoods.sort_values().plot(
        kind='barh', 
        ax=axs[1, 0],
        color='skyblue'
    )
    axs[1, 0].set_title('Top 10 Neighborhoods')
    
    # Geographic Price Distribution
    scatter = sns.scatterplot(
        x='longitude', 
        y='latitude', 
        hue='price',
        data=df,
        palette='viridis',
        alpha=0.6,
        ax=axs[1, 1],
        size=0.5
    )
    axs[1, 1].set_title('Geographic Price Distribution')
    axs[1, 1].set_xlim(-74.5, -73)
    axs[1, 1].set_ylim(40.5, 41)
    scatter.legend_.remove()
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    return fig

# Main Execution
if __name__ == "__main__":
    # Load and explore data
    raw_df = load_and_explore()
    
    # Clean data
    raw_df, cleaned_df = clean_data(raw_df)
    
    print("\nCleaned Data Info:")
    print(cleaned_df.info())
    
    print("\nData Cleaning Report:")
    print(f"Original entries: {len(raw_df)}")
    print(f"Cleaned entries: {len(cleaned_df)}")
    print(f"Rows removed: {len(raw_df) - len(cleaned_df)}")
    
    # Create visualizations
    raw_viz = create_visualizations(raw_df, "Before Cleaning")
    cleaned_viz = create_visualizations(cleaned_df, "After Cleaning")
    
    # Save visualizations
    raw_viz.savefig('reports/raw_data_visualization.png', dpi=300)
    cleaned_viz.savefig('reports/cleaned_data_visualization.png', dpi=300)
    plt.close('all')
    
    print("\nProcessing complete!")
    print(f"Cleaned data saved to: processed_data/cleaned_airbnb_data.csv")
    print(f"Visualizations saved to: reports/ directory")
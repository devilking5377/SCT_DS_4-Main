import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap

# Load dataset
df = pd.read_csv('US_Accidents_March23.csv')

# Display basic information
df.info()
df.head()

# Check missing values
missing_values = df.isnull().sum()
print(missing_values[missing_values > 0])

# Drop rows with missing Start_Time and Weather_Condition
df = df.dropna(subset=['Start_Time', 'Weather_Condition'])

# Convert to datetime
df['Start_Time'] = pd.to_datetime(df['Start_Time'], errors='coerce')
df['Hour'] = df['Start_Time'].dt.hour

df[['Start_Time', 'Hour']].head()

# Set plot size
plt.figure(figsize=(10, 5))
# Create countplot
sns.countplot(data=df, x="Hour", hue="Hour", palette="coolwarm", legend=False)
# Labels and title
plt.xlabel("Hour of the Day")
plt.ylabel("Number of Accidents")
plt.title("Accidents by Hour of the Day")
# Save plot (optional)
plt.tight_layout()
plt.savefig("accidents_per_hour.png")
# Show plot
plt.show()

# ===== Weather Condition Plot =====
plt.figure(figsize=(10, 5))

# Get top 10 weather conditions
top_weather = df['Weather_Condition'].value_counts().nlargest(10).index

# Plot countplot
sns.countplot(y='Weather_Condition', 
              data=df[df['Weather_Condition'].isin(top_weather)],
              color='skyblue')

# Labels and title
plt.xlabel("Number of Accidents")
plt.ylabel("Weather Condition")
plt.title("Top 10 Weather Conditions in Accidents")

# Save plot (optional)
plt.tight_layout()
plt.savefig("weather_conditions.png")

# Show plot
plt.show()

# ===== Folium Heatmap =====
import folium
from folium.plugins import HeatMap

# Filter for non-null coordinates
df_map = df[['Start_Lat', 'Start_Lng']].dropna()

# Sample a subset to reduce rendering time (e.g., 20,000 rows)
df_sample = df_map.sample(n=20000, random_state=42)

# Create base map centered on average coordinates
map_accidents = folium.Map(location=[df_sample['Start_Lat'].mean(), df_sample['Start_Lng'].mean()],
                           zoom_start=5)

# Add heatmap layer
HeatMap(data=df_sample[['Start_Lat', 'Start_Lng']], radius=8).add_to(map_accidents)

# Display map
map_accidents
# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt

# Load the data from a CSV file
df = pd.read_csv('movies.csv')
print(df.describe())
# Convert the Release Date to datetime and extract the year
df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')
df['Year'] = df['Release Date'].dt.year

# Split the Genres column into a list of genres and explode it to have one genre per row
df['Genres'] = df['Genres'].str.split(',')
df = df.explode('Genres')

# Group by Year and Genre to count the number of movies for each genre per year
genre_counts = df.groupby(['Year', 'Genres']).size().reset_index(name='Count')

# Calculate the total number of movies released each year
yearly_counts = df.groupby('Year').size().reset_index(name='Total_Movies')

# Merge the genre counts with the total movie counts per year
genre_proportion = pd.merge(genre_counts, yearly_counts, on='Year')

# Calculate the proportion of each genre
genre_proportion['Proportion'] = genre_proportion['Count'] / genre_proportion['Total_Movies']

# Pivot the data to get a stacked format suitable for plotting
pivot_data = genre_proportion.pivot(index='Year', columns='Genres', values='Proportion').fillna(0)

# Sort genres within each year by proportion
sorted_pivot_data = pd.DataFrame()

# Iterate through each year to sort genres by proportion
for year in pivot_data.index:
    # Sort the genres by their proportion for the current year
    sorted_row = pivot_data.loc[year].sort_values()
    sorted_pivot_data = sorted_pivot_data._append(sorted_row)

# Plotting the sorted stacked bar chart
sorted_pivot_data.plot(kind='bar', stacked=True, figsize=(16, 10), colormap='tab20')

plt.title('Sorted Stacked Bar Chart of Genre Popularity Trends Over Time')
plt.xlabel('Year')
plt.ylabel('Proportion of Movies')
plt.legend(title='Genres', bbox_to_anchor=(1.05, 1), loc='upper left')


plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.subplots_adjust(right=0.8) 
plt.show()
# Save the chart as an image
chart_path = 'analysis/pandas_chart.png'
plt.savefig(chart_path)
plt.close()  # Close the figure to avoid display issues
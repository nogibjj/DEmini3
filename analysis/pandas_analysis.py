# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('movies.csv')
print(df.describe())
df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')
df['Year'] = df['Release Date'].dt.year


df['Genres'] = df['Genres'].str.split(',')
df = df.explode('Genres')


genre_counts = df.groupby(['Year', 'Genres']).size().reset_index(name='Count')

# Calculate the total number of movies released each year
yearly_counts = df.groupby('Year').size().reset_index(name='Total_Movies')

genre_proportion = pd.merge(genre_counts, yearly_counts, on='Year')

# Calculate the proportion of each genre
genre_proportion['Proportion'] = genre_proportion['Count'] / genre_proportion['Total_Movies']


pivot_data = genre_proportion.pivot(index='Year', columns='Genres', values='Proportion').fillna(0)


sorted_pivot_data = pd.DataFrame()

for year in pivot_data.index:

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

# chart_path = 'analysis/pandas_chart.png'
# plt.savefig(chart_path)
# plt.close()  
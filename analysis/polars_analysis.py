# Import necessary libraries
import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from a CSV file
df = pl.read_csv('movies.csv')

# Convert the Release Date to datetime format and extract the year
df = df.with_columns(
    pl.col('Release Date').str.strptime(pl.Date, "%Y-%m-%d", strict=False).alias('Release Date')
)
df = df.with_columns(df['Release Date'].dt.year().alias('Year'))

# Split and explode the Genres column
df = df.with_columns(df['Genres'].str.split(','))
df = df.explode('Genres')

# Filter out rows with missing ratings
df = df.filter(pl.col('Rating').is_not_null())

# Convert to Pandas for easier visualization with seaborn
df_pd = df.to_pandas()

# Plotting the distribution of ratings for each genre using seaborn
plt.figure(figsize=(14, 8))
sns.boxplot(data=df_pd, x='Genres', y='Rating')
plt.title('Genre-Specific Rating Distribution')
plt.xlabel('Genres')
plt.ylabel('Rating')
plt.xticks(rotation=90)
plt.grid(True)
plt.show()
# Save the chart as an image
chart_path = 'analysis/polars_chart.png'
plt.savefig(chart_path)
plt.close()  # Close the figure to avoid display issues


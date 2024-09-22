# Import necessary libraries
import pandas as pd
import polars as pl
import timeit
from memory_profiler import memory_usage

# Function to benchmark Pandas
def pandas_benchmark():
    # Load data
    df = pd.read_csv('movies.csv')

    # Convert Release Date to datetime and extract the year
    df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')
    df['Year'] = df['Release Date'].dt.year

    # Split and explode Genres
    df['Genres'] = df['Genres'].str.split(',')
    df = df.explode('Genres')

    # Group and calculate average rating by year and genre
    result = df.groupby(['Year', 'Genres'])['Rating'].mean().reset_index()
    return result

# Function to benchmark Polars
def polars_benchmark():
    # Load data
    df = pl.read_csv('movies.csv')

    # Convert Release Date to datetime and extract the year
    df = df.with_columns(
        pl.col('Release Date').str.strptime(pl.Date, "%Y-%m-%d", strict=False).alias('Release Date')
    )
    df = df.with_columns(df['Release Date'].dt.year().alias('Year'))

    # Split and explode Genres
    df = df.with_columns(df['Genres'].str.split(','))
    df = df.explode('Genres')

    # Group and calculate average rating by year and genre
    result = df.group_by(['Year', 'Genres']).agg(pl.col('Rating').mean().alias('Average Rating'))
    return result

# Timing and Memory Profiling
def profile_function(func, name):
    # Measure execution time
    execution_time = timeit.timeit(func, number=10)  # Run 10 times and take the average

    # Measure memory usage
    mem_usage = memory_usage((func, (), {}), interval=0.1, timeout=1)
    max_mem_usage = max(mem_usage)

    print(f"{name} - Execution Time: {execution_time:.4f} seconds, Max Memory Usage: {max_mem_usage:.2f} MB")

# Main entry point
if __name__ == '__main__':
    print("Running benchmarks...\n")
    profile_function(pandas_benchmark, "Pandas")
    profile_function(polars_benchmark, "Polars")

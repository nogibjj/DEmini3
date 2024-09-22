# Define variables
PYTHON = python
PANDAS_ANALYSIS = analysis/pandas_analysis.py
POLARS_ANALYSIS = analysis/polars_analysis.py
BENCHMARK = analysis/benchmark.py
REPORT = reports/benchmark_report.md

# Default target
all: generate_report

# Target to run Pandas analysis
pandas_analysis:
	@echo "Running Pandas analysis..."
	$(PYTHON) $(PANDAS_ANALYSIS)

# Target to run Polars analysis
polars_analysis:
	@echo "Running Polars analysis..."
	$(PYTHON) $(POLARS_ANALYSIS)

# Target to run Benchmark
benchmark:
	@echo "Running Benchmark..."
	$(PYTHON) $(BENCHMARK)

# Target to generate report
generate_report: pandas_analysis polars_analysis benchmark
	@echo "Generating Report..."
	@echo "# Analysis and Benchmark Report" > $(REPORT)
	@echo "## Pandas Analysis Results" >> $(REPORT)
	@cat analysis/pandas_analysis_output.md >> $(REPORT)
	@echo "\n## Polars Analysis Results" >> $(REPORT)
	@cat analysis/polars_analysis_output.md >> $(REPORT)
	@echo "\n## Benchmark Results" >> $(REPORT)
	@cat analysis/benchmark_output.md >> $(REPORT)
	@echo "Report generated at $(REPORT)"

# Clean generated files
clean:
	@echo "Cleaning up..."
	@rm -f $(REPORT)
	@rm -f analysis/*_output.md
	@echo "Cleanup complete."

.PHONY: all pandas_analysis polars_analysis benchmark generate_report clean



install: 
	pip3 install --upgrade pip && pip3 install -r requirements.txt

format: 
	black *.py

lint:
	flake8 --ignore=E501,W503 *.py
	
test: 
	python3 -m pytest -cov=main test_main.py

clean:
	rm -rf .pytest_cache

generate_report:
	# Run Python script to generate the report
	python -c "from main import load_data, calculate_statistics, generate_md_report, benchmark_pandas_vs_polars, load_data_pl, calculate_statistics_pl, create_histogram_pl; \
	data_pl = load_data_pl('rdu-weather-history.csv'); \
	stats_pl = calculate_statistics_pl(data_pl); \
	create_histogram_pl(data_pl, 'Temperature Maximum', 'temperature_maximum_distribution.png'); \
	pandas_profile, polars_profile = benchmark_pandas_vs_polars('rdu-weather-history.csv'); \
	generate_md_report(stats_pl, ['temperature_maximum_distribution.png'], pandas_profile, polars_profile, 'summary_report.md');"

	# Git commands to add, commit, and push the report and PNG files
	@if [ -n "$$(git status --porcelain)" ]; then \
	    git config --local user.email "action@github.com"; \
	    git config --local user.name "GitHub Action"; \
	    git add summary_report.md temperature_maximum_distribution.png; \
	    git commit -m 'Add generated markdown report and histogram image'; \
	    git push; \
	else \
	    echo "No changes to commit."; \
	fi


all: install format lint test generate_report

NBA Data Analysis
===============

Summary
-------------------
**positions**: classifying NBA players into positions using a KNearestNeighbors classifier on season statistics

**styles**: clustering NBA teams and players based on their play styles determined by the frequencies of play types

**tiers**: clustering NBA players into tiers using the k-means clustering algorithm on advanced statistics


Check out the [deployed web app] (http://nba-analysis.herokuapp.com/).

Data
-------------------
All the data was scraped from the [NBA's publicly available stats] (http://stats.nba.com/)


Getting Started
-------------------
All of the needed libraries can be installed using `pip install -r requirements.txt` in the repository directory.

Install the package using `python setup.py install`.

Unless you have the required database URI, change the package `config.py` file to have `data_source = 'local'`.

Prior to running the app, you will likely want to scrape the data, to do this run `python nba_analysis/scraping/*.py`. Do this after changing the package config so that the data is downloaded locally. All the data should be downloaded into the directory `nba_analysis/data/`.

To run the web app, run `python runserver.py` and point your browser to `http://localhost:5000/`.

Alternatively, to run individual analyses, navigate to the `nba_analysis/analysis` directory (must enter subdirectory due to hard-coded data paths) and run `python <analysis_script> <params>`.

Disclaimer
-------------------
All of these experiments/mini-projects are more for proof-of-concept and practice than true analysis. The analysis is rudimentary and the scikit-learn algorithms used could be tuned much further by manipulating parameters.

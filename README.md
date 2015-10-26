NBA Data Analysis
===============

Summary
-------------------
**eras**: comparison of various NBA statistics (home court advantage, points per game) across time.

**positions**: classifying NBA players into positions using a KNearestNeighbors classifier on season statistics

**shots**: classifying shot make/miss using a Naive Bayes classifier on shot data from the 2014-2015 NBA season for a given player

**tiers**: clustering NBA players into tiers using the k-means clustering algorithm on advanced statistics

**tracking**: visualization of ball tracking data scraped from stats.nba.com


Sources
-------------------
* [Fivethirtyeight] (https://github.com/fivethirtyeight/data/tree/master/nba-elo)

* [Basketball-Reference] (http://www.basketball-reference.com/leagues/NBA_2015_advanced.html)

* [NBA Stats (scraped)] (http://stats.nba.com/)


Libraries
-------------------

All of the needed libraries can be installed using `pip install -r requirements.txt` in the repository directory.


Disclaimer
-------------------

All of these experiments/mini-projects are more for proof-of-concept and practice than true analysis. Most of the data sets could use significant refinement. Moreover the analysis is rudimentary and the scikit-learn algorithms used could be tuned much further by manipulating parameters.

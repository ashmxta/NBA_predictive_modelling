# ECE324: Predictive Modeling of NBA Game Outcomes
This github repo contains all coding artifacts used for model training and to produce figures for our final project report. To learn more about our project, feel free to view our [final presentation](https://docs.google.com/presentation/d/1wbNToctD4GDqJdecT4lifqlGs3gQBpBkTQs6nnlTFOg/edit?usp=sharing). 

## Directory organization
This repo contains 6 folders:
- raw_data: contains webscraped game data, organzied by team by year in CSV file format
- cleaned_data: contains cleaned datasets (with and without dates) and data visualization artifacts
- data_scripts: contains scripts used to pull and processing data (web-scrapping)
- MLP: contains collab notebooks of MLP models
- time_series: collab notebook containing both 1-D CNN and LSTM models
- tree_models: collab notebooks of RF and XGB models

This is the naming convention used for models: 
- file name: model_dataset.ipynb
- eg. MLP_clean.ipynb
- models: MLP, RF, XGB, time_series
- datasets: kaggle, cleaned, cleaned_dates

The Kaggle dataset can be downloaded from [this link](https://www.kaggle.com/datasets/eoinamoore/historical-nba-data-and-player-box-scores?resource=download
).
The API used for Basketball reference webscrapper can be found at this [link](https://jaebradley.github.io/basketball_reference_web_scraper/api/#get-season-schedule).

## Contributors
- Ashmita Bhattacharyya
- Doga Baskan
- Samson Chow  


Last updated: 6th Apr 2025

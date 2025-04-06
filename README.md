# ECE324: Predictive Modeling of NBA Game Outcomes
This github repo contains all coding artifacts used for model training and to produce figures for our final project report. To learn more about our project, feel free to view our [final presentation](https://docs.google.com/presentation/d/1wbNToctD4GDqJdecT4lifqlGs3gQBpBkTQs6nnlTFOg/edit?usp=sharing). 

## Directory organization
This repo contains 4 folders:
- raw_data: contains webscraped game data, organzied by team by year in CSV file format
- cleaned_data: contains cleaned datasets (with and without dates) and data visualization artifacts
- data_scripts: contains scripts used to pull and processing data (web-scrapping)
- models: contains collab notebooks of our final models

This is the naming convention used in the models folder: 
- file name: model_dataset.ipynb
- eg. MLP_kaggle.ipynb
- models: MLP, RF, XGB, 1-D_CNN, LSTM
- datasets: kaggle, cleaned, cleaned_dates

The Kaggle dataset can be downloaded from [this link](https://www.kaggle.com/datasets/eoinamoore/historical-nba-data-and-player-box-scores?resource=download
).

## Contributors
- Ashmita Bhattacharyya
- Doga Baskan
- Samson Chow  


Last updated: 6th Apr 2025

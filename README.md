# My Taskmaster Analysis Project

The purpose of this project was to apply my learning from the **[Office of National Statics (ONS) Data Science Campus Graduate Program](https://datasciencecampus.ons.gov.uk/long-read/data-science-graduate-programme/)** I was fortunate to be apart of between 2023 and 2015 as part of working in the public sector. As a Data Analyst looking to move into Data Science, I wanted to take the tools, methods and new knowledge into a project where I could gain further experience and have fun experimenting and exploring. I carried this work out during limited spare hours on weekends and evenings.

I decided this project should focus on data from the TV show **[Taskmaster](https://taskmaster.tv)** because it is one of my favourite shows, along with being unique and full of data. As the show is about Celebrities carrying out tasks and competing against each other, there is a vast amount of data and statistics that I wanted to model, obtained from **[Taskmaster Wiki](https://taskmaster.fandom.com/wiki/Taskmaster_Wiki)**. 

My main aims, through Machine Learning Modelling, and other methods, was to predict the winner of Series 21, group the contestents in to segments to see which ones were similar, and determine the overall best contestent, based on the data and exploration of Series 1 - 20. To get here, I carried out exploratory data analysis, which kept growing as I thought of new things I wanted to probe, which turned this project into a complex beast! 

The Repository contains the code and my overall analysis of this project, where I am to include a report of my findings at a future date. This is by no means a business related project, but from my analysis and methods, I can, and have, pull out snippets or functions into other pieces of work where appropriate.  

## Taskmaster Report
To be completed - **report on analysis, methods and findings**

### Abstract
To be completed

## Folders
The following folders are in the (rough) order of how methods and analysis were carried out. 

### 1. Getting Data
This folder contains the scripts to get the data to carry out the analysis:

1. **getting_taskmaster_data.py**: Uses APIs to get the Contestents' scores for each episode and overall series from **[Taskmaster Wiki](https://taskmaster.fandom.com/wiki/Taskmaster_Wiki)** which provides the majority of the data for this project. 
2. **getting_IMDB_ratings.py**: Uses APIs to obtain the [IMDB](https://www.imdb.com/title/tt4934214/) ratings for each episode.
3. **scraping_functins.py**: Contains the functions for the two scripts above.

### 2. Data Cleaning
This folder contains scripts to clean the data or merge tables together:

1. **Cleaning_Data.py**: Cleans the tables created in by the 'Getting_Data' scripts, using the functions in the script **Cleaning_Functions.py**.
2. **Merging_Output_Tables.py**: Once EDA has been carried out (see folder 'EDA'), this script merges all respective tables.
3. **Data for Modelling.py**: This script prepares the final data ready for modelling (see folder 'ML Modelling').
4. **Task Decription Cleaning.py**: This script obtains the task descirptions from the table created in 'Cleaning_Data.py'.

### 3. EDA
This folder contains the scripts for carrying out Exploratory Data Analysis. The 'Function_Scripts' folder contains the function scripts used by the respective main scripts. For example, the 'DQ_Functions.py' script contains the functions used by the 'DQ_Exploration.py' script.

1. **Total_Scores_EDA.py**: Script used to obtain, for example, the total scores, positions and seat winners for each episode and series.
2. **Total_Scores_Visuals.py**: Creates the plots and visuals from the analysis carried out in the 'Total_Scores_EDA.py script.
3. **Further_Scores_EDA.py**: Obtains addition contenstent score information such as episodes won or who won the most tasks.
4. **Team_Task_Analysis.py**: Compares each team and their scores throughout each series.
5. **DQ_Exploration.py**: Determines which contestents were disqualified the most or least, and whether this could have impacted their final position.
6. **Gender_Age_EDA.py**: Explores whether there was potential age or gender bias.
7. **IMDB_Ratings_Analysis.py**: Takes the IMDB ratings table and analyses the data.

### 4. Correlations
This folder contains the **Correlations_Distributions.py** script (and the **Correlation_Functions.py** function script) to determine the correlations between variables.

### 5. ML Modelling
This folder contains the scripts (and function scripts) where the machine learning models are used on the data. It also contains a folder with the saved models as .pkl files.



## Outputs
**Explain outputs/excel files and figures**

The following folders are where data were saved to be used in other scripts, or where figures and plots were stored.

### Data


## Reproducibility
Due to the complexity and niche-ness of this project, and as a result of working on this in my spare time, the majority of the scripts are not reproducible. Instead, this project is a once-off piece of analytical and data science work, specific to what I wanted to explore and model. As I kept adding/updating ideas, the scripts evolved quickly, and as consequence, without repeatable steps.

However, the Machine Learning and API scripts are the only ones that, with some tweaks, could be reused for other data sets or newer Taskmaster Series. 

## Lack of Quality Assurance
A consequence of doing this project on my own and in my spare time means that project is without any quality assurance or additional testing steps (other than what I carried out). This means that it is likely things will be missed and values, outputs, or models may not correct.

Given this however, my main objective for this project was to explore the data and apply Data Science methods from my learning. But given the complicated dataset this was tricky. As this is a once-off piece of exploration and modelling, with no business requirements or impact, the outputs from this work are reasonable and more of a proof to myself that I can apply logic and methods to complex datasets. 

However, where possible I have considered, caveated and made decision on how to progress where data is likely to be incorrect, even if actions have not been taken to fix or make changes.

## Using Chat-GPT
GPT was used in three main ways:
1. Basic debugging and error fixing
2. Writing single lines of code where I do not fully know the correct syntax
3. Writing more complex code where I have an envision or idea I want to pursue, but did not have the time or resources to work it out given a solo and personal project.




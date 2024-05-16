from __future__ import annotations

import logging
from datetime import datetime

from airflow.decorators import dag, task
from airflow.operators.python import is_venv_installed

log = logging.getLogger(__name__)

if not is_venv_installed():
    log.warning("This DAG requires virtualenv, please install it.")
else:
    @dag(schedule=None, 
         start_date=datetime(2021, 1, 1), 
         catchup=False, 
         tags=["big_data"])

    def CS4540_project():

        @task.virtualenv(
            use_dill=True,
            system_site_packages=False,
            requirements=["funcsigs", "sodapy", "pandas", "streamlit_echarts"],
        )

        def acquire():
            import pandas as pd
            from sodapy import Socrata    

            # Paths for saving csv's that will be used
            df_paths = ["/storage/18_49_out.csv", "/storage/50_64_out.csv", "/storage/65_out.csv", "/storage/cov_cases.csv"]

            # The age demogarphics that will be getting data for
            age_demographics = ["18-49", "50-64", "65+"]

            client = Socrata("data.lacity.org", None)

            # Was having issues with timeout on requests as data.lacity.org requests sometimes take a long time. Increased timeout timer
            client.timeout = 50

            # Creates csv's for vaccine information for each age demographic
            for x in range(3):
                # Query datalacity for data based on age demographic
                results = client.get("iv7a-6rrq", where='demographic_value = "' + age_demographics[x] + '" AND county = "Los Angeles"', limit=300000)
                # Save results into pandas dataframe
                df = pd.DataFrame.from_records(results)
                #Save the csv to path
                df.to_csv(df_paths[x])

            # Does the same as above but for a different dataset. This one is for covid infection data
            results = client.get("jsff-uc6b", limit=1000000)
            LA_cov_cases_df = pd.DataFrame.from_records(results)
            LA_cov_cases_df.to_csv("/storage/cov_cases.csv")

            # Return paths to created csv's 
            return df_paths

        @task()
        def clean(input_dfs):

            import pandas as pd

            # The paths and names for the eventually cleaned data
            new_names = ["/storage/18_49_clean_out.csv", "/storage/50_64_clean_out.csv", "/storage/65_clean_out.csv", "/storage/cov_cases_clean_out.csv"]

            i = 0

            # This is where the data is cleaned. Iterates through csv's and cleans each one
            for path in input_dfs:
                # Read csv into dataframe
                curr_df = pd.read_csv(path)
                # Goes through the 'date' column and removes entries of duplicate dates
                curr_df.drop_duplicates(subset=['date'], inplace=True)
                # This is specifically for the covid infections data. Some data in the 'new_deaths" column were negative so this changes any negatives to 0
                if "new_deaths" in curr_df.columns:
                    curr_df.loc[curr_df['new_deaths'].astype(float) < 0, 'new_deaths'] = 0
                # Saves cleaned dataframe as a new cleaned csv
                curr_df.to_csv(new_names[i])
                print(path + " has been cleaned!")
                i += 1

            # Return paths to cleaned csv's
            return new_names

        @task()
        def analyze(input_clean_dfs):

            import pandas as pd

            # Does analysis on data
            for path in input_clean_dfs:
                # Read csv into dataframe    
                df = pd.read_csv(path)
                # Get mean, median and standard deviation for vaccine data csv's based on number of doses
                if "at_least_one_dose" in df.columns:
                    df['at_least_one_dose'] = df['at_least_one_dose'].astype(float)
                    mean = df[["at_least_one_dose"]].mean(axis=0)
                    stddev = df[["at_least_one_dose"]].std(axis=0)
                    median = df[["at_least_one_dose"]].median(axis=0)

                    print("Analysis for: " + str(path))
                    print("mean: " + str(mean))
                    print("median: " + str(median))
                    print("standard deviation: " + str(stddev))

                # Get mean, median and standard deviation for covid infection data based on number of new deaths
                elif "new_deaths" in df.columns:
                    df['new_deaths'] = df['new_deaths'].astype(float)
                    mean = df[["new_deaths"]].mean(axis=0)
                    stddev = df[["new_deaths"]].std(axis=0)
                    median = df[["new_deaths"]].median(axis=0)

                    print("Analysis for: " + str(path))
                    print("mean: " + str(mean))
                    print("median: " + str(median))
                    print("standard deviation: " + str(stddev))
                print("------------------------------------------------------------------------------------------------")
            return 0

        @task()
        def visualize(data):
            print("Visualize here")
            


        order_data = acquire()
        order_summary = clean(order_data)
        analysis = analyze(order_summary)
        visualize(analysis)

    python_demo_dag = CS4540_project()
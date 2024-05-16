# Covid-and-Vaccine-Data-Science
This project creates a data pipeline in Airflow that extracts covid infection and vaccine data from data.lacity.org and cleans it for use in analysis and visualization via streamlit.

##Installation

1. Airflow
   
Airflow is how the data pipeline will be managed. As this project was made on the Windows OS, a container will be used with `docker-compose.yml` being used for setup. 

First create the three folders `dags`, `plugins`, `config`, and `storage`

```
mkdir dags/ logs/ plugins/ config/ storage/
chmod 777 dags logs plugins config storage
```

Next, to start up Airflow, run the following command

```
docker-compose up --build
```

The default port that will be used is 8080 so going to `http://localhost:8080` in your browser should bring you to the Airflow page. If it asks for a username and password, the default for both is `airflow`. These settings and others can be modified in `docker-compose.yml`.

DAGs are the control files for Airflow. Currently, there is only one for the project, `CS4540_project.py` which is data pipeline for this project. The `dags` foler is where all future DAGs should go. 

Any time that a DAG has been modified, you will need to stop and restart the scheduler in order to see the changes in Airflow. This can be done in the Docker Desktop app. 

2. Streamlit

Streamlit along with eCharts is what will be used to display our data in graphs after it has been processed in our pipeline. Once again, a `docker-compose.yml` file is used for setup.

Run the following command while in the `streamlit` folder to get started. 

```
docker-compose up --build
```

Once that is done, going to `http://localhost:8501` in your browser will open Streamlit. 

The `app/app.py` file is what displays the content onto the page. The files in `app/demo_echarts` and `app/dempyecharts` are the actual code for the graphs. Currently, only `demo_echarts/line.py` has been modified for this project. 

Check out https://github.com/andfanilo/streamlit-echarts for more info. 

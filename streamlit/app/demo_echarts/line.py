import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode

import pandas as pd

def process(dates):

    # Function for processing data from csv's for use in graphs

    Data_18_49 = []
    Data_50_64 = []
    Data_65 = []
    Data_total = []

    LA_vacc_18_49_df = pd.read_csv("./data/18_49_clean_out.csv")
    LA_vacc_50_64_df = pd.read_csv("./data/50_64_clean_out.csv")
    LA_vacc_65_df = pd.read_csv("./data/65_clean_out.csv")

    LA_vacc_total_df = pd.concat([LA_vacc_18_49_df, LA_vacc_50_64_df, LA_vacc_65_df])

    # This will get the total vaccinations over the course of an input month for each age demographic
    for date in dates:
        # Gets a slice of the csv that is only the input month as defined by 'date'
        timeframe = LA_vacc_18_49_df[LA_vacc_18_49_df['date'].str.contains(date)]
        # Adds up the amount of vaccinations over that month
        total = timeframe["at_least_one_dose"].astype(float).sum()
        Data_18_49.append(total)
    
    # Repeat for other demographics
    for date in dates:
        timeframe = LA_vacc_50_64_df[LA_vacc_50_64_df['date'].str.contains(date)]
        total = timeframe["at_least_one_dose"].astype(float).sum()
        Data_50_64.append(total)

    for date in dates:
        timeframe = LA_vacc_65_df[LA_vacc_65_df['date'].str.contains(date)]
        total = timeframe["at_least_one_dose"].astype(float).sum()
        Data_65.append(total)

    for date in dates:
        timeframe = LA_vacc_total_df[LA_vacc_total_df['date'].str.contains(date)]
        total = timeframe["at_least_one_dose"].astype(float).sum()
        Data_total.append(total)


    # A 2D array, each one is a set of values for graph
    all_data = [Data_18_49, Data_50_64, Data_65, Data_total]

    return all_data

def process_cov(dates):
    # Function for getting the total new covid cases per month

    data = []

    totals_df = pd.read_csv("./data/totals_clean_out.csv")

    for date in dates:
        timeframe = totals_df[totals_df['date'].str.contains(date)]
        total = timeframe["at_least_one_dose"].astype(float).sum()
        data.append(total)

    return data



def render_basic_area_chart():

    dates = ["2021-01", "2021-02", "2021-03", "2021-04", "2021-05", "2021-06", "2021-07", "2021-08", "2021-09", "2021-10", "2021-11", "2021-12"]

    data = process(dates)


    options = {
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "data": data[3],
                "type": "line",
                "areaStyle": {},
            }
        ],
    }

    st_echarts(options=options)

    data = []

    totals_df = pd.read_csv("./data/cov_cases_clean_out.csv")

    for date in dates:
        timeframe = totals_df[totals_df['date'].str.contains(date)]
        total = timeframe["new_deaths"].astype(float).sum()
        data.append(total)

    options = {
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "data": data,
                "type": "line",
                "areaStyle": {},
                "min": "0",
            }
        ],
    }

    st_echarts(options=options)


def render_stacked_line_chart_2023():
   
    dates = ["2023-01", "2023-02", "2023-03", "2023-04", "2023-05", "2023-06", "2023-07", "2023-08", "2023-09", "2023-10", "2023-11", "2023-12"]

    data = process(dates)


    options = {
        "title": {"text": "2023 Vaccinations"},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": ["18-49", "50-64", "65+"]},
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "toolbox": {"feature": {"saveAsImage": {}}},
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": "18-49",
                "type": "line",
                "stack": "Num Vaccinated",
                "data": data[0],
            },
            {
                "name": "50-64",
                "type": "line",
                "stack": "Num Vaccinated",
                "data": data[1],
            },
            {
                "name": "65+",
                "type": "line",
                "stack": "Num Vaccinated",
                "data": data[2],
            },
        ],
    }
    st_echarts(options=options, height="400px")



def render_stacked_line_chart_2022():
    dates = ["2022-01", "2022-02", "2022-03", "2022-04", "2022-05", "2022-06", "2022-07", "2022-08", "2022-09", "2022-10", "2022-11", "2022-12"]

    data = process(dates)

    options = {
        "title": {"text": "2022 Vaccinations"},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": ["18-49", "50-64", "65+"]},
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "toolbox": {"feature": {"saveAsImage": {}}},
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": "18-49",
                "type": "line",
                "stack": "Num Vaccinated",
                "data": data[0],
            },
            {
                "name": "50-64",
                "type": "line",
                "stack": "Num Vaccinated",
                "data": data[1],
            },
            {
                "name": "65+",
                "type": "line",
                "stack": "Num Vaccinated",
                "data": data[2],
            },
        ],
    }
    st_echarts(options=options, height="400px")



def render_stacked_line_chart_2021():

    dates = ["2021-01", "2021-02", "2021-03", "2021-04", "2021-05", "2021-06", "2021-07", "2021-08", "2021-09", "2021-10", "2021-11", "2021-12"]
    data = process(dates)


    options = {
        "title": {"text": "2021 Vaccinations"},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": ["18-49", "50-64", "65+"]},
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "toolbox": {"feature": {"saveAsImage": {}}},
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": "18-49",
                "type": "line",
                "stack": "Num Vaccinated",
                "data": data[0],
            },
            {
                "name": "50-64",
                "type": "line",
                "stack": "Num Vaccinated",
                "data": data[1],
            },
            {
                "name": "65+",
                "type": "line",
                "stack": "Num Vaccinated",
                "data": data[2],
            },
        ],
    }
    st_echarts(options=options, height="400px")


ST_LINE_DEMOS = {
    "2021 Vaccinations and Covid Deaths": (
        render_basic_area_chart,
        "https://echarts.apache.org/examples/en/editor.html?c=area-basic",
    ),
    "2023 vaccinations by Age": (
        render_stacked_line_chart_2023,
        "https://echarts.apache.org/examples/en/editor.html?c=line-stack",
        ),
    "2022 vaccinations by Age": (
        render_stacked_line_chart_2022,
        "https://echarts.apache.org/examples/en/editor.html?c=line-stack",
    ),
    "2021 vaccinations by Age": (
        render_stacked_line_chart_2021,
        "https://echarts.apache.org/examples/en/editor.html?c=line-stack",
    ),
}

import datetime as dt
import json
import os
import time

import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
import requests
from plotly.subplots import make_subplots
from pytrends.request import TrendReq

# -- Variables --#
WEEKS = 8

hboMax_movies = [
    {"name": "Wonder Woman 1984", "year": 2020, "alt": "HBO Max"},
    {"name": "Godzilla vs. Kong", "year": 2021, "alt": "HBO Max"},
    {"name": "Mortal Kombat", "year": 2021, "alt": "HBO Max"},
    {"name": "The Conjuring: The Devil Made Me Do It", "year": 2021, "alt": "HBO Max"},
    {"name": "In The Heights", "year": 2021, "alt": "HBO Max"},
    {"name": "Space Jam: A New Legacy", "year": 2021, "alt": "HBO Max"},
    {"name": "The Suicide Squad", "year": 2021, "alt": "HBO Max"},
    {"name": "Malignant", "year": 2021, "alt": "HBO Max"},
    {"name": "Dune", "year": 2021, "alt": "HBO Max"},
    {"name": "The Matrix Resurrections", "year": 2021, "alt": "HBO Max"},
]

disneyPlus_movies = [
    {"name": "Jungle Cruise", "year": 2021, "alt": "Disney Plus"},
    {"name": "Cruella", "year": 2021, "alt": "Disney Plus"},
    {"name": "Black Widow", "year": 2021, "alt": "Disney Plus"},
]

theaterOnly_movies = [
    {"name": "Spider-Man: No Way Home", "year": 2021},
    {"name": "Shang-Chi and the Legend of the Ten Rings", "year": 2021},
    {"name": "Venom: Let There Be Carnage", "year": 2021},
    {"name": "F9: The Fast Saga", "year": 2021},
    {"name": "Eternals", "year": 2021},
    {"name": "No Time to Die", "year": 2021},
    {"name": "A Quiet Place Part II", "year": 2021},
    {"name": "Ghostbusters: Afterlife", "year": 2021},
    {"name": "Free Guy", "year": 2021},
]

# -- Movie API -- #
# dotenv.load_dotenv("C:/_CODING/Python/portfolio_passcodes.env")
# TMBD_API_KEY = os.getenv("tmdb_api_key")

TMBD_API_KEY = os.environ.get("tmdb_api_key")
TMBD_API = "https://api.themoviedb.org/3/search/movie"
TMBD_API_IMG = "https://image.tmdb.org/t/p/original/"


# ---- Functions ---- #
# -- Get Week Number Friday Start -- #
def get_week_number(date):
    """
    Given a date, returns the week number based on a Friday start
    :param date: date object
    :return: date object
    """
    year_start = dt.date(date.year, 1, 1)
    return (date - year_start).days // 7 + 1


# -- Get Movie Date -- #
def get_movie_date(film, year):
    """
    Gets the release date of film from the TMBD API, rounded to nearest Monday.
    :param film: name of movie
    :param year: year of movie's release
    :return: the monday closest to the movie's release
    """
    film_data = requests.get(TMBD_API, params={'api_key': TMBD_API_KEY,
                                               'query': film,
                                               'page': 1,
                                               'region': 'US',
                                               'year': year}).json()

    release_date = film_data['results'][0]['release_date']
    rd = dt.date.fromisoformat(release_date)
    return rd


# -- Get Movie Poster -- #
def get_movie_poster(film, year):
    """
    Gets the poster of a movie from the TMBD API.
    :param film: movie name
    :param year: release date
    :return: an image url
    """
    film_data = requests.get(TMBD_API, params={'api_key': TMBD_API_KEY,
                                               'query': film,
                                               'page': 1,
                                               'region': 'US',
                                               'year': year}).json()
    poster = film_data['results'][0]['poster_path']
    poster_path = TMBD_API_IMG + poster

    return poster_path


# -- Get Movie Blurb -- #
def get_movie_blurb(film, year):
    """
    Gets the summary of a movie from the TMBD API.
    :param film: movie name
    :param year: release year
    :return: a string
    """
    film_data = requests.get(TMBD_API, params={'api_key': TMBD_API_KEY,
                                               'query': film,
                                               'page': 1,
                                               'region': 'US',
                                               'year': year}).json()
    overview = film_data['results'][0]['overview']

    return overview


# ---- Get Google Trends ---- #
def get_google_trends(film, start_date, alt='watch online'):
    """
    Pull eight weeks of google trends for searches on streaming vs theater
    :param film: name of movie
    :param start_date: movie release date
    :param alt: name of streamer if movie was not theater-only, i.e. Disney Plus or HBO Max
    :return: dataframe of max interest per week (friday start)
    """
    if film == "F9: The Fast Saga":
        film = "F9"

    pytrends = TrendReq(hl='en-US', tz=300)
    kw_list = [f"{film} {alt}", f"{film} AMC"]

    friday_start = start_date + dt.timedelta((4 - start_date.weekday()) % 7)

    window = dt.timedelta(weeks=WEEKS - 1)

    end_date = friday_start + window
    if end_date >= dt.date.today():
        end_date = dt.date.today()

    timeframe = f"{start_date} {end_date}"

    pytrends.build_payload(kw_list, geo='US', timeframe=timeframe)

    trend_df = pytrends.interest_over_time()
    trend_df = trend_df.resample('W-FRI').max()
    trend_df = trend_df.drop('isPartial', axis=1)

    return trend_df


# -- Set the Time Frame for Box Office Data -- #
def get_timeframe(start_date):
    """
    Calculates six weeks out from start date in Box Office Mojo's format
    :param start_date: movie's release date
    :return: list of week numbers to plug into get_box_office_per_week()
    """
    friday_start = start_date + dt.timedelta((4 - start_date.weekday()) % 7)

    year = friday_start.year
    week_num = get_week_number(friday_start)
    week_num_range = list(np.arange(int(week_num), int(week_num) + WEEKS))

    time_range = []
    for i in range(len(week_num_range)):
        if week_num_range[i] > 52:
            week_num_range[i] = f"{week_num_range[i] - 52}"
            if int(week_num_range[i]) < 10:
                week_num_range[i] = f"0{week_num_range[i]}"
            new_year = year + 1
            time_range.append(
                {'year': new_year, 'week_num': week_num_range[i], 'date': friday_start + dt.timedelta(days=7 * i)})
        else:
            if week_num_range[i] < 10:
                week_num_range[i] = f"0{week_num_range[i]}"
            week_num_range[i] = f'{week_num_range[i]}'
            time_range.append(
                {'year': year, 'week_num': week_num_range[i], 'date': friday_start + dt.timedelta(days=7 * i)})

    return time_range


# -- Get the Data from Box Office Mojo -- #
def get_boxoffice_per_week(film, start_date):
    """
    Pull 6 weeks of domestic box office gross $
    :param film: name of the movie
    :param start_date: movie's release date
    :return: dataframe of box office per week for one title
    """
    time_range = get_timeframe(start_date)
    movie_dict = {}
    bow_movie_weekly = {}

    for week in time_range:
        date = week['date']
        if date + dt.timedelta(days=7) > dt.date.today():
            bow_movie_weekly[date] = 0
        else:
            box_office_data = f"https://www.boxofficemojo.com/weekly/{week['year']}W{week['week_num']}/"
            box_office_weekly = pd.read_html(box_office_data)[0]
            bow_all = box_office_weekly[['Release', 'Gross']]
            bow_movie = bow_all.loc[bow_all['Release'].str.lower() == film.lower()]
            if bow_movie.empty:
                bow_movie_weekly[date] = 0
            else:
                bow_movie_weekly[date] = bow_movie['Gross'].item()

    movie_dict[film] = bow_movie_weekly
    movie_df = pd.DataFrame.from_dict(movie_dict)
    movie_df.reset_index(inplace=True)
    movie_df = movie_df.rename(columns={'index': 'date'})
    movie_df['date'] = pd.to_datetime(movie_df['date'])

    return movie_df


# ---- Chart Both Box Office and Google Trends as Table ---- #
def get_boxoffice_and_trends_table(movie, year, alt='watch online'):
    """
    Combines box office data with google trend data.
    :param movie: name of movie
    :param year: year movie released in US
    :param alt: streaming platform (if none = 'watch online')
    :return: a merged dataframe and html for use in Flask
    """
    release_date = get_movie_date(film=movie, year=year)
    google_trends_df = get_google_trends(film=movie, start_date=release_date, alt=alt)
    box_office_df = get_boxoffice_per_week(film=movie, start_date=release_date)

    merged_data = pd.merge(google_trends_df,
                           box_office_df,
                           how="outer", on="date")
    md = merged_data.sort_values(by='date')
    md.columns = ["Date", "Streaming Interest", "Theater Interest", "Box Office Gross"]
    md.fillna(0, inplace=True)

    most_popular = np.where(md['Streaming Interest'] >= md['Theater Interest'], 'Streaming', 'Theater')
    md.insert(3, 'Most Popular Option', most_popular)

    md['Weekly Holdover'] = md['Box Office Gross'].replace('[\$,]', '', regex=True).astype(int).pct_change()
    md['Weekly Holdover'].replace([np.inf, -np.inf], np.nan, inplace=True)
    md.fillna(0, inplace=True)
    md['Weekly Holdover'] = md['Weekly Holdover'].astype(float).map("{:.1%}".format)

    md['Box Office Gross'] = md['Box Office Gross'].replace('[\$,]', '', regex=True).astype(int)

    table = md.to_html(index=False,
                       formatters={'Box Office Gross': '${:,d}'.format},
                       classes=["table table-hover table-striped table-sm table-bordered"])

    return table, md


# ---- Chart Both Box Office and Google Trends with Plotly ---- #
def get_boxoffice_and_trends_figure(dataframe):
    """
    Visualization of box office and google trend data with plotly
    :param dataframe: a dataframe
    :return: a chart json for use with Flask
    """
    figure = make_subplots(specs=[[{"secondary_y": True}]])

    # -- Bar Chart for Box Office Gross -- #
    figure.add_trace(
        go.Bar(x=dataframe['Date'].iloc[::-1],
               y=dataframe['Box Office Gross'].iloc[::-1],
               name='Box Office Gross',
               marker={'color': '#007D79'},
               hovertemplate="%{fullData.name}: %{y:.2s} <extra></extra>"
               ),
        secondary_y=False
    )

    # -- Scatter for Streaming Search Interest -- #
    figure.add_trace(
        go.Scatter(x=dataframe['Date'],
                   y=dataframe['Streaming Interest'],
                   name='Streaming Interest',
                   line={'width': 5, 'dash': 'dot'},
                   marker={'color': '#FA4D56', "line_width": 2},
                   ),
        secondary_y=True
    )

    # -- Scatter for Theater Search Interest -- #
    figure.add_trace(
        go.Scatter(x=dataframe['Date'],
                   y=dataframe['Theater Interest'],
                   name='Theater Interest',
                   line={'width': 5},
                   marker={'color': '#33B1FF', "line_width": 2},
                   ),
        secondary_y=True
    )

    # -- Figure Update Layout -- #
    figure.update_layout(
        legend=dict(orientation="h", yanchor="top", font={"color": "#E1E1E1"}),
        hovermode='x unified',
        margin=dict(t=20, b=20, pad=5),
        paper_bgcolor="#161616",
        plot_bgcolor="#161616",
        font={'color': "#E1E1E1"},
        xaxis=dict(tickvals=dataframe['Date'],
                   tickformat="%b %d",
                   automargin=True,
                   tickangle=0,
                   tickfont_size=10,
                   linecolor='#404040',
                   showgrid=False),
        yaxis=dict(range=[0, max(dataframe['Box Office Gross']) + 500000],
                   tickfont_size=10,
                   title="Domestic Box Office Gross $",
                   gridcolor='#404040',
                   linecolor='#404040', ),
        yaxis2=dict(range=[0, 100],
                    tickfont_size=10,
                    title="Google Search Interest",
                    showgrid=False),
    )

    chart_json = json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)
    return chart_json


def get_chart_from_database(movie, table):
    """
    Returns a plotly chart json for placement in flask jinja
    :param table: table from database
    :param movie: name of movie
    :return: plotly chart json
    """
    selected_movie = table.query.filter_by(name=movie).first()
    chart = selected_movie.chart
    return chart

# -- Pre-Fill Database For Article -- #

# all_movies = hboMax_movies + disneyPlus_movies + theaterOnly_movies
# Movie.query.delete()
#
# for movie in all_movies:
#     name = movie['name']
#     year = movie['year']
#     if 'alt' in movie:
#         alt = movie['alt']
#     else:
#         alt = "watch online"
#     table, dataframe = get_boxoffice_and_trends_table(name, year, alt)
#     chart = get_boxoffice_and_trends_figure(dataframe)
#
#     new_movie = Movie(
#         name=name,
#         chart=chart,
#         dataframe=dataframe,
#         html_table=table
#     )
#     print(name)
#     movie_db.session.add(new_movie)
#     movie_db.session.commit()

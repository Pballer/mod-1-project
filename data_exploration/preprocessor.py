"""

This module will load and format movie data.

It will read in movie data from IMDB and The Numbers
and prepare both for analysis. The two data sets are
joined based on title and year.  All revenues and
production costs are denominated in USD.

"""


import pandas as pd


def read_movie_data():
    """Load movie data."""
    imdb_title_basics = pd.read_csv(
        './data_exploration/data/imdb.title.basics.csv.gz')

    imdb_title_ratings = pd.read_csv(
        './data_exploration/data/imdb.title.ratings.csv.gz')

    tn_movie_budgets = pd.read_csv(
        './data_exploration/data/tn.movie_budgets.csv.gz')

    return imdb_title_basics, imdb_title_ratings, tn_movie_budgets


def merge_basics_with_ratings(imdb_title_basics, imdb_title_ratings):
    """Merge imdb basics with ratings."""
    imdb_basics_rating = pd.merge(
        imdb_title_basics,
        imdb_title_ratings,
        on=['tconst'],
        how='outer',
        indicator=True,
    )
    return imdb_basics_rating


def format_tn_date(tn_movie_budgets):
    """Format date in TN movie data."""
    tn_movie_budgets.release_date = pd.to_datetime(
        tn_movie_budgets.release_date)

    tn_movie_budgets['release_year'] = tn_movie_budgets.release_date.dt.year


def format_currency_fields(tn_movie_budgets):
    """Convert currency string fields into integers."""
    tn_movie_budgets.loc[:, 'production_budget':'worldwide_gross'] = \
        tn_movie_budgets.loc[:, 'production_budget':'worldwide_gross'] \
        .replace('[^.0-9]', '', regex=True).astype(int)


def calculate_roi(tn_movie_budgets):
    """Calculate ROI for domestic and world."""
    tn_movie_budgets['dom_roi'] = \
        round(
            ((tn_movie_budgets.domestic_gross
              - tn_movie_budgets.production_budget)
             / tn_movie_budgets.production_budget)
            * 100, 2)

    tn_movie_budgets['world_roi'] = \
        round(((tn_movie_budgets.worldwide_gross
                - tn_movie_budgets.production_budget)
               / tn_movie_budgets.production_budget)
              * 100, 2)


def merge_imdb_with_tn(imdb_basics_rating, tn_movie_budgets, title_column):
    """Merge imdb data with tn movie data."""
    return pd.merge(
        imdb_basics_rating,
        tn_movie_budgets,
        left_on=[title_column, 'start_year'],
        right_on=['movie', 'release_year'],
        how='inner',
    )


def concat_imdb_tn_data(imdb_tn_primary_title, imdb_tn_original_title):
    """Concat two movie dataset.  Remove duplicates."""
    imdb_tn_all = pd.concat([imdb_tn_primary_title, imdb_tn_original_title])
    imdb_tn_all.drop_duplicates(inplace=True)
    return imdb_tn_all


def remove_invalid_revenues(imdb_tn_merged):
    """Remove invalid movie revenues."""
    imdb_tn_current = imdb_tn_merged.loc[imdb_tn_merged.start_year < 2020]\
        .copy()

    imdb_tn_current = imdb_tn_current.loc[
        (imdb_tn_current.domestic_gross != 0)
        & (imdb_tn_current.worldwide_gross != 0)
    ]

    return imdb_tn_current


def remove_invalid_genres(imdb_tn_cleaned):
    """Drop invalid genres."""
    imdb_tn_cleaned.dropna(subset=['genres'], inplace=True)


def melt_genres(imdb_tn_cleaned):
    """

    Melt genres column into multiple rows.

    """

    # Split genres into 3 columns.
    imdb_tn_cleaned[['genre1', 'genre2', 'genre3']] = \
        imdb_tn_cleaned.genres.str.split(
            ',',
            expand=True
        )

    # Melt into one genre column.
    genre_melt = imdb_tn_cleaned.melt(
        id_vars=imdb_tn_cleaned.columns[:-3],
        value_vars=['genre1', 'genre2', 'genre3'],
        value_name='genre')

    # Remove null genres.
    genre_melt.dropna(subset=['genre'], inplace=True)
    genre_melt.drop(columns=['variable'], inplace=True)

    return genre_melt


def calculate_number_of_genres_per_movie(imdb_tn_by_genre):
    """Add a genre count for each movie."""
    imdb_tn_by_genre['num_of_genres'] = \
        imdb_tn_by_genre.genres.apply(lambda x: len(x.split(',')))


def drop_unused_columns(imdb_tn_by_genre):
    """Drop duplicate or unused columns."""
    imdb_tn_by_genre.drop(
        columns=['_merge', 'movie', 'start_year'],
        inplace=True)


def transform(imdb_title_basics, imdb_title_ratings, tn_movie_budgets):
    """Prepare movie data for analysis."""
    # Merge basics with ratings.
    imdb_basics_rating = merge_basics_with_ratings(
        imdb_title_basics,
        imdb_title_ratings)

    # Format date column
    format_tn_date(tn_movie_budgets)

    # Convert currency string fields into integers.
    format_currency_fields(tn_movie_budgets)

    # Calculate ROI
    calculate_roi(tn_movie_budgets)

    # Merge imdb with tn on 'primary_title' column.
    imdb_tn_primary_title = merge_imdb_with_tn(
        imdb_basics_rating,
        tn_movie_budgets,
        'primary_title'
    )

    # Merge imdb with tn on 'original_title' column.
    imdb_tn_original_title = merge_imdb_with_tn(
        imdb_basics_rating,
        tn_movie_budgets,
        'original_title'
    )

    # Concat primary title with original title merged data.
    imdb_tn_merged = concat_imdb_tn_data(
        imdb_tn_primary_title,
        imdb_tn_original_title
    )

    # Remove invalid revenues.
    imdb_tn_cleaned = remove_invalid_revenues(imdb_tn_merged)

    # Remove NaN genres.
    remove_invalid_genres(imdb_tn_cleaned)

    # Expand genres column into separate rows per genre.
    imdb_tn_by_genre = melt_genres(imdb_tn_cleaned)

    # Add genre count column.
    calculate_number_of_genres_per_movie(imdb_tn_by_genre)

    # Drop unused columns.
    drop_unused_columns(imdb_tn_by_genre)

    return imdb_tn_by_genre

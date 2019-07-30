"""Module for visualizing movie data."""

import seaborn as sns


def transform_data_for_visualization(data):
    """Prepare data for visualizations."""
    # Drop genres that do not have enough movies for analysis.
    movie_data = filter_movies_by_genre_count(data)
    scale_to_millions(movie_data)
    return movie_data


def sort_genre_by_quartile(data, column, quartile):
    """Sort genres based on quartile."""
    return data.groupby('genre')[column]\
        .quantile(quartile)\
        .sort_values(ascending=False).index


def create_genre_boxplot(data, y_column,
                         sort_by_quartile=.25,
                         figsize=(15, 10),
                         ylable=None):
    """Create boxplot for each genre."""
    # Create genre color map.
    colors = sns.color_palette("Paired", n_colors=7, desat=.9) \
        + sns.color_palette("pastel", n_colors=7, desat=.9)
    genre_color_map = dict(zip(data.genre.unique(), colors))

    # Order boxplots based on quantile.
    quantile_order = sort_genre_by_quartile(data, y_column, sort_by_quartile)
    sns.set(rc={'figure.figsize': figsize})

    box_plot = sns.boxplot(
        x="genre",
        y=y_column,
        data=data,
        order=quantile_order,
        palette=genre_color_map,
        showfliers=False
    )
    box_plot.set_ylabel(ylable if ylable else y_column)

    return box_plot


def most_common_genres_by_count(data, top=14):
    """Return most common genres by count."""
    return data.genre.value_counts()[:top].index


def filter_movies_by_genre_count(data):
    """Drop genres that do not have enough movies for analysis."""
    most_common_genres = most_common_genres_by_count(data)

    most_common_movies_by_genre = data.loc[
        data.genre.isin(most_common_genres)
    ].copy()

    return most_common_movies_by_genre


def scale_to_millions(data):
    """Change scale to millions."""
    data.loc[:, 'production_budget':'worldwide_gross'] = \
        data.loc[:, 'production_budget':'worldwide_gross'] / 1000000

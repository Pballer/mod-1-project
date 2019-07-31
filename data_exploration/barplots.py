"""module creates bar plots and 4-plot chart"""


import matplotlib.pyplot as plt


def create_unsorted_bar_plot(
        data,
        x_column,
        y_column,
        name_of_graph='',
        x_name='',
        y_name='',
        shade='b'):
    """Returns an unsorted bar plot"""
    bar_plot = data.groupby(
        [x_column])[y_column].median().plot.bar(color=shade)
    plt.title(name_of_graph)
    plt.xlabel(x_column if x_name == '' else x_name)
    plt.ylabel(y_column if y_name == '' else y_name)
    return bar_plot


def create_sidebar_plot(
        data,
        x_column,
        y_column,
        name_of_graph='',
        x_name='',
        y_name='',
        shade='b'):
    """Returns a sidebar plot"""
    sidebar_plot = data.groupby(
        [x_column])[y_column].median().sort_values().plot.barh(
            color=shade)
    plt.title(name_of_graph)
    plt.ylabel(x_column if x_name == '' else x_name)
    plt.xlabel(y_column if y_name == '' else y_name)
    return sidebar_plot


def create_bar_plot(
        data,
        x_column,
        y_column,
        name_of_graph='',
        x_name='',
        y_name='',
        shade='b'):
    """Returns a bar plot"""
    bar_plot = data.groupby(
        [x_column])[y_column].median().sort_values(ascending=False).plot.bar(color=shade)
    plt.title(name_of_graph)
    plt.xlabel(x_column if x_name == '' else x_name)
    plt.ylabel(y_column if y_name == '' else y_name)
    return bar_plot


def create_mixed_four_bar_plot_on_x(data,
                                    x_1,
                                    y_11,
                                    y_12,
                                    y_21,
                                    y_22,
                                    width=18,
                                    height=11):
    """Returns 4 plots based on one x variable and four y variables"""
    plt.subplots(nrows=2, ncols=2, figsize=(width, height))
    plt.subplot(2, 2, 1)
    create_sidebar_plot(data, x_1, y_11, shade='b')
    plt.subplot(2, 2, 2)
    create_sidebar_plot(data, x_1, y_12, shade='k')
    plt.subplot(2, 2, 3)
    create_bar_plot(data, x_1, y_21, shade='b')
    plt.subplot(2, 2, 4)
    create_bar_plot(data, x_1, y_22, shade='k')
    plt.tight_layout()
    return plt.show()

import click
import pandas as pd
from pathlib import Path
from rich.console import Console
from rich.table import Table

##############
##############
### Global ###
##############
##############

console = Console() # Get a prettier output using rich

# Get the right path
script_dir = Path(__file__).parent
csv_path = script_dir/"data"/"movies.csv"

data = pd.read_csv("myflix/data/movies.csv") # Use pandas to do all the filtering

# This is a custom decorator function to apply shared click options
def recommend_filters(func):
    # Add the necessary options
    options = [
        click.option("--limit", "-l", default=5, help="Limit the number of results"),
        click.option("--min-rating", "-m", default=0.0, help="Set a minimum acceptable rating"),
        click.option("--genres", "-g", type=str, help="Specify the genres on which you want to get recommendations. Use a comma separated list"),
        click.option("--exclude", "-e", type=str, help="Specify the genres you don't to get recommendations of. Put a comma separated list of genres you're sick of"),
        click.option("--min-votes", "-v", default=500_000, help="Change the acceptable amount of votes to get recommendations. Use a lower value if you want to get more lesser-known movies"),
        click.option("--rating-range", "-r", nargs=2, type=float, default=(0.0, 10.0), help="Set a specific range to get movies so you get different results")
    ]
    for opt in reversed(options): # Apply all of them
        func = opt(func)
    return func




###############
### methods ###
###############

# Then use rich's tables to create the styled output
# Commands will only give this method a subset containing only the important data
def df_to_table(dataset: pd.DataFrame) -> Table:
    # Construct the table
    table = Table(title = "Recommended Movies", show_lines=True)
    table.add_column("")
    table.add_column("Title", style="bold")
    table.add_column("Rating", justify="right")
    table.add_column("Num of votes", justify="right")
    table.add_column("Genres")

    # Add only the columns' values present here
    n = 1
    columns = ["primaryTitle", "averageRating", "numVotes", "genres"]
    for index, row in dataset.iterrows():
        row_data = [str(n)]
        for col in columns:
            row_data.append(str(parse_value(row, col)))
        table.add_row(*row_data)
        n+=1
    return table

# Apply some specific styles depending on the value of the cell and the row
def parse_value(row: pd.Series, col: str):
    value = row[col]
    if pd.isna(value):
        return "-"

    match col:
        case "genres": # Nice little formatting
            value = value.replace(",", ", ")

        case "numVotes": # Ratings on lower values are dubious
            value = int(value)
            if 1_000 <= value < 2_000:
                value = f"[red]{value}[/]"
            elif 2_000 <= value < 5_000:
                value = f"[yellow]{value}[/]"
            else:
                value = f"[green]{value}[/]"
    return value


# Shared method to reuse the filtering logic since all the subcommands will use the same flags. At least for
# the recommend group
def apply_filters(limit, min_rating, rating_range, min_votes, genres, exclude, dataset) -> pd.DataFrame:
    if min_rating and rating_range:
        raise click.UsageError("Options --min-rating and --rating-range are mutually exclusive")

    # Rating range filters
    if min_rating:
        subset = dataset[dataset["averageRating"] >= min_rating]
    else:
        min_r, max_r = rating_range
        subset = dataset[
            (dataset["averageRating"] >= min_r) & (dataset["averageRating"] <= max_r)
        ]

    # Genre filtering
    if genres:
        genres = [s.strip() for s in genres.split(",")]
        regex = "|".join(genres)
        subset = subset[subset["genres"].str.contains(regex, na=False, case=False)]

    # Exclude genres
    if exclude:
        exclude = [s.strip() for s in exclude.split(",")]
        regex = "|".join(exclude)
        subset = subset[~subset["genres"].str.contains(regex, na=False, case=False)]

    subset = subset[subset["numVotes"] >= min_votes] # Minimum amount of votes filter
    subset = subset.head(limit) # Output limiter
    return subset



################
### Commands ###
################

@click.group()
def cli(): # Entry point
    """This is a CLI movie recommendation system"""


@click.command()
@recommend_filters
def recommend(limit, min_rating, rating_range, min_votes, genres, exclude):
    """With this option you will be able to get recommendations based on:\n
        1. Genre\n
        2. A rating range"""
    subset = apply_filters(limit, min_rating, rating_range, min_votes, genres, exclude, data)
    console.print(df_to_table(subset))

cli.add_command(recommend)

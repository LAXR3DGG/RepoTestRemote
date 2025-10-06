import pandas as pd

##################
### Basics TSV ###
##################

# Load the files to sanitize the data
basics = pd.read_csv("title.basics.tsv", sep="\t", dtype=str, na_values="\\N")

# Remove anything that is not a movie
basics = basics[basics["titleType"]=="movie"]

# Drop entries with missing genres or years (if I happen to add an option to limit that)
basics = basics.dropna(subset=["startYear", "genres"])

# Turn the numeric data to actual numeric values
basics["startYear"] = pd.to_numeric(basics["startYear"], errors="coerce")
basics["runtimeMinutes"] = pd.to_numeric(basics["runtimeMinutes"], errors="coerce")


###################
### Ratings TSV ###
###################

# Load the ratings file
ratings = pd.read_csv("title.ratings.tsv", sep="\t", dtype=str, na_values="\\N")

# Convert the rating values to float
ratings["averageRating"] = ratings["averageRating"].astype(float)
ratings["numVotes"] = pd.to_numeric(ratings["numVotes"], errors="coerce")

###############
### Merging ###
###############

movies = pd.merge(basics, ratings, on="tconst", how="inner")

# Add a lowercase column for an easier matching
movies["lowerTitle"] = movies["primaryTitle"].str.lower()

# Sort the movies by average rating values
movies.sort_values(by="averageRating", axis=0, ascending=False, inplace=True, kind="quicksort")

# Remove unused columns
movies.drop(["titleType", "isAdult", "endYear"], axis=1, inplace=True)

# Remove low voted movies to prevent skewed results
movies = movies[movies["numVotes"] >= 1000]


# Save the merged data to a CSV
movies.to_csv("movies.csv", index=False)



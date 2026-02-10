# MR 2nd Movie Recommender
import csv

# this function reads the movie file
# it turns each row into a dictionary
# it also cleans up the text a little
def load_movies(filename):
    movies = []
    try:
        with open(filename, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    movie = {}
                    movie["title"] = row["Title"].strip()
                    movie["director"] = row["Director"].strip().lower()

                    # split genres into a list
                    movie["genres"] = []
                    for g in row["Genre"].split("/"):
                        movie["genres"].append(g.strip().lower())

                    movie["rating"] = row["Rating"].strip()

                    # convert length to int
                    movie["length"] = int(row["Length"])

                    # split actors into a list
                    movie["actors"] = []
                    for a in row["Actors"].split(","):
                        movie["actors"].append(a.strip().lower())

                    movies.append(movie)

                except:
                    print("bad row skipped")

        return movies

    except FileNotFoundError:
        print("movies.csv not found")
        return []


# this filters by genre
# it checks if the text is inside any genre
def filter_genre(movies, text):
    text = text.lower().strip()
    results = []

    for m in movies:
        for g in m["genres"]:
            if text in g:
                results.append(m)
                break

    return results


# this filters by director name
# simple contains check
def filter_director(movies, text):
    text = text.lower().strip()
    results = []

    for m in movies:
        if text in m["director"]:
            results.append(m)

    return results


# this filters by actor
# checks each actor in the list
def filter_actor(movies, text):
    text = text.lower().strip()
    results = []

    for m in movies:
        for a in m["actors"]:
            if text in a:
                results.append(m)
                break

    return results


# this filters by length
# user can give min or max or both
def filter_length(movies, min_len, max_len):
    results = []

    for m in movies:
        ok = True

        if min_len is not None:
            if m["length"] < min_len:
                ok = False

        if max_len is not None:
            if m["length"] > max_len:
                ok = False

        if ok:
            results.append(m)

    return results


# this applies all chosen filters
# it runs them one by one
# this makes AND logic
def apply_filters(all_movies, chosen, values):
    results = all_movies[:]

    if "genre" in chosen:
        results = filter_genre(results, values["genre"])

    if "director" in chosen:
        results = filter_director(results, values["director"])

    if "actor" in chosen:
        results = filter_actor(results, values["actor"])

    if "length" in chosen:
        results = filter_length(
            results,
            values["min_len"],
            values["max_len"]
        )

    return results


# prints movies in a simple way
# prints index and main info
def print_movies(movies):
    if len(movies) == 0:
        print("no movies found")
        return

    i = 1
    for m in movies:
        print(i, m["title"], "|", m["director"], "|", m["length"], "min")
        i += 1


# prints the whole list
# just calls print_movies
def print_full_list(movies):
    print("\nfull movie list\n")
    print_movies(movies)


# handles the search questions
# asks user which filters
def search_flow(movies):
    print("\nchoose filters")
    print("1 genre")
    print("2 director")
    print("3 actor")
    print("4 length")

    picks = input("numbers with commas: ")
    parts = picks.split(",")

    chosen = set()
    values = {}

    for p in parts:
        p = p.strip()

        if p == "1":
            chosen.add("genre")
            values["genre"] = input("enter genre: ")

        if p == "2":
            chosen.add("director")
            values["director"] = input("enter director: ")

        if p == "3":
            chosen.add("actor")
            values["actor"] = input("enter actor: ")

        if p == "4":
            chosen.add("length")
            min_text = input("min length or blank: ").strip()
            max_text = input("max length or blank: ").strip()

            if min_text.isdigit():
                values["min_len"] = int(min_text)
            else:
                values["min_len"] = None

            if max_text.isdigit():
                values["max_len"] = int(max_text)
            else:
                values["max_len"] = None

    results = apply_filters(movies, chosen, values)

    print("\nresults\n")
    print_movies(results)

    if len(results) == 0:
        print("try fewer filters")


# main menu function
# keeps program running
def main():
    print("movie recommender program")
    print("search by genre director actor and length")

    movies = load_movies("movies.csv")

    if len(movies) == 0:
        return

    while True:
        print("\nmenu")
        print("1 search")
        print("2 print all")
        print("3 exit")

        choice = input("choice: ").strip()

        if choice == "1":
            search_flow(movies)

        elif choice == "2":
            print_full_list(movies)

        elif choice == "3":
            print("bye")
            break

        else:
            print("not valid")


# start program
main()

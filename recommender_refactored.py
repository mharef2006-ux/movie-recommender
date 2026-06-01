import json
import random

# region function system
def normalize_movies(movie_list: list):
    return [movie.lower() for movie in movie_list]


def similarity(user_movies_a: list, user_movies_b: list) -> int:
    common_movies = set(normalize_movies(user_movies_a)) & set(normalize_movies(user_movies_b))
    return len(common_movies)


def get_best_match_score(name, users, user_movies_dict):
    scores = []
    for user in users:
        if user != name:
            scores.append(similarity(user_movies_dict[name], user_movies_dict[user]))
    return max(scores) if scores else 0


def get_similar_users(name, users, user_movies_dict):
    similar_users = []
    for user in users:
        if user != name and similarity(user_movies_dict[name], user_movies_dict[user]) != 0:
            similar_users.append(user)
    return similar_users


def get_best_users(name, users, user_movies_dict):
    best_matching_users = []
    for user in users:
        if (
            user != name
            and similarity(user_movies_dict[name], user_movies_dict[user]) != 0
            and similarity(user_movies_dict[name], user_movies_dict[user])
            == get_best_match_score(name, users, user_movies_dict)
        ):
            best_matching_users.append(user)
    return best_matching_users


def recommend_movies(name, users, user_movies_dict):
    recommended_movies = []
    for user in users:
        for movie in normalize_movies(user_movies_dict[user]):
            if movie not in normalize_movies(user_movies_dict[name]):
                if movie not in recommended_movies:
                    recommended_movies.append(movie)
    return recommended_movies

# endregion

# region open_file system
file_loaded = False
try:
    with open("./data.json", "r") as file_:
        data = json.load(file_)
    file_loaded = True

except FileNotFoundError:
    data = {
        "Ali": ["Inception", "Matrix"],
        "Sara": ["Titanic", "Inception"]
    }


# endregion


def main(name, best_match_score, similar_users, recommended_movies):
    print(f"your welcome {name}")

    if best_match_score:
        print(
            f"{random.choice(get_best_users(name, list(data.keys()), data))} "
            f"is the most similar to you"
        )
        print(f"the number of common film: {best_match_score}")
    else:
        print("No similar users found")

    if recommended_movies:
        print(f"Recommended movie: {random.choice(recommended_movies)}")
    else:
        print("No recommendation found")


# region main system

name = input("Enter your name: ")

if name not in data:
    favorite_movies = input(
        'Enter your favorite movies (separate with comma ","): '
    ).split(",")

    data[name] = normalize_movies(favorite_movies)

    if file_loaded:
        with open("./data.json", "w") as file_:
            json.dump(data, file_)

best_match_score = get_best_match_score(name, list(data.keys()), data)
similar_users = get_similar_users(name, list(data.keys()), data)
recommended_movies = recommend_movies(name, similar_users, data)

main(name, best_match_score, similar_users, recommended_movies)

# endregion

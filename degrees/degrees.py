import csv
import sys
# added: import time to track time that every search takes
import time

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    start = time.time()
    print("Loading data...")
    load_data(directory)
    end = time.time()
    elapsed = end-start
    print(f"Data loaded. Loading data took {int(elapsed)} seconds.")
    while True:
        source = person_id_for_name(input("Name: "))
        if source is None:
            sys.exit("Person not found.")
        target = person_id_for_name(input("Name: "))
        if target is None:
            sys.exit("Person not found.")
        start = time.time()
        path = shortest_path(source, target)
        end = time.time()
        if path is None:
            print(f"\nNot connected. The search ran for {int(end-start)} seconds.")
        else:
            degrees = len(path)
            print(f"\nThe search ran for {int(end-start)} seconds.\n{degrees} degrees of separation.")
            path = [(None, source)] + path
            for i in range(degrees):
                person1 = people[path[i][1]]["name"]
                person2 = people[path[i + 1][1]]["name"]
                movie = movies[path[i + 1][0]]["title"]
                print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.
    #   0 create path and stack lists/dicts
    #   1 start with start name --> get row and all associated movies
    #   2 get a movie in the stack and pull all artists
    #   3 check if artist is target, if yes - done,if not - get all movies from artist and add to stack
    If no possible path, returns None.
    """
    # create path and frontier and explored set
    path =[]
    frontier = QueueFrontier()
    explored = set()
    # create starting node
    start = Node(state=source, parent=None, action=None)
    #add starting node to frontier
    frontier.add(start)
    while True:
        # get first node in frontier if not start
        node = frontier.remove()
        # add this node's actor (node.state) to explored dataset --> not actor and movie because then one actor will be taken into consideration multiple times
        explored.add(node.state)
        #get neighbors (=co-actors and co-starring movie) and add to frontier
        neighbors = neighbors_for_person(node.state)
        #add neighbors to frontier
        for neighbor in neighbors:
            if neighbor[1] not in explored and not frontier.contains_state(neighbor[1]):
                new_node = Node(state=neighbor[1], parent=node, action=neighbor[0])
                if new_node.state == target:
                    node = new_node
                    while node.parent is not None:
                        path.append((node.action, node.state))
                        node = node.parent
                    path.reverse()
                    return path
                else:
                    frontier.add(new_node)
            else:
                continue


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()

import re

def clean_movie_title(title):
    title = title.strip().strip(".avi")
    title = re.sub(r"[.\[\]\(\)-]" ," ", title)
    title = re.sub(r"([0-9]{4}).*" ,r",\1", title)
    title = title.replace("  "," ").replace(" ,",",")
    return title.lower().capitalize()
    
with open("films.txt") as file:
    films = file.readlines()    
films_cleaned = set([clean_movie_title(title) for title in films])
container, rest = [], []
url = "http://www.omdbapi.com/?t=%s&apikey=******"
while films_cleaned:
    film = films_cleaned.pop()
    film_year = film.split(",")
    film_query= film_year[0].replace(" ","+")
    year = film_year[-1] if len(film_year) > 1 else None
    film = film_query + "&y=%s" % year if year else film_query
    try:
        resp = urllib.request.urlopen(url % film)
        data = json.loads(resp.read())
    except Exception as e:
        rest.append(film)
        continue
    if "Error" not in data:
        container.append((film,data))
    else:
        rest.append(film)
        
for film,data in container:
    display_values = [film, data[“Title”], data[“imdbRating”],
                      data[“Genre”], 
                      “http://www.imdb.com/title/%s" % data[“imdbID”],
                      data[“Year”], data[“Actors”], 
                      data[“Plot”], data[“Country”]
                     ]
    print(“\t”.join(display_values))

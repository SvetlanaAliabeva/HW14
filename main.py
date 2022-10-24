import sqlite3
import flask
import json


def run_sql(sql):
    with sqlite3.connect('netflix.db') as connection:
        connection.row_factory = sqlite3.Row
        result = []
        for item in connection.execute(sql).fetchall():
            result.append(dict(item))

        return result

app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.get("/movie/<title>")
def step_1(title):
    sql = f'''select title, country, release_year, listed_in as genre, description  from netflix where title='{title}'
          order by date_added desc
          limit 1'''

    result = run_sql(sql)
    if result:
        result = result[0]

    return flask.jsonify(resuly)


@app.get("/movie/<int:year1>/to/<int:year2>")
def step_2(year1, year2):
    sql = f'''select title, release_year from netflix
          where release_year between {year1} and {year2}
          order by release_year asc'''

    return flask.jsonify(run_sql(sql))


@app.get("/rating/<rating>")
def step_3(rating):
    my_dict = {
        "children": ("G", "G"),
        "family" : ("G", "PG", "PG-13"),
        "adult" : ("R", "NC-17")
    }

    sql = f'''
          select title, description from netflix
          where rating in {my_dict.get(rating, ("PG-13", "NC-17"))}'''

    return flask.jsonify(run_sql(sql))


@app.get("/genre/<genre>")
def step_4(genre):
    sql = f'''
          select * from netflix
          where listed_in like '%{genre.title()}' 
          '''

    return flask.jsonify(run_sql(sql))


def step_5(name1='Rose McIver', name2='Ben Lamb'):
    sql = f'''
          select "cast" from netflix
          where "cast" like '%{name1}%' and "cast" like '%{name2}%' 
          '''

    result = run_sql(sql)

    main_name = {}
    for item in result:
        names = item.get('cast').split(", ")
        for name in names:
            if name in main_name.keys():
                main_name[name] += 1
            else:
                main_name[name] = 1

    for item in main_name:
        if item not in (name1, name2) and main_name[item] >= 2:
            return result


def step_6(types = 'TV Show', release_year=2021, genre='TV'):
    sql = f'''
          select * from netflix
          where type ='{types}' 
          and release_year= '{release_year}'
          and listed_in like '%{genre}%'
          '''

    return json.dumps(run_sql(sql), indent=4, ensure_ascii=False)


if __name__ == '__main__':
    # app.run(host="localhost", port=5000, debug=True)
    print(step_6())

from flask import Flask, render_template, request, jsonify
import os, re, datetime
import db
from models import Lang

app = Flask(__name__)


# create the database and table. Insert 10 test books into db
# Do this only once to avoid inserting the test books into
# the db multiple times
if not os.path.isfile("langss.db"):
    db.connect()


# route for landing page
# check out the template folder for the index.html file
# check out the static folder for css and js files
@app.route("/")
def index():
    return render_template("index.html")


def isValid(email):
    regex = re.compile(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    )
    if re.fullmatch(regex, email):
        return True
    else:
        return False


@app.route("/request", methods=["POST"])
def postRequest():
    req_data = request.get_json()
    email = req_data["email"]
    if not isValid(email):
        return jsonify(
            {
                "status": "422",
                "res": "failure",
                "error": "Invalid email format. Please enter a valid email address",
            }
        )
    name = req_data["name"]
    released_year = req_data["released_year"]
    github_rank = req_data["github_rank"]
    link = req_data["link"]
    thumbnail = req_data[" thumbnail"]
    description = req_data["description"]

    langs = [l.serialize() for l in db.view()]

    for l in langs:
        if l["name"] == name:
            return jsonify(
                {
                    # 'error': '',
                    "res": f"Error ⛔❌! Lamguage with Name {name} is already in The List!",
                    "status": "404",
                }
            )

    lang = Lang(
        db.getNewId(),
        name,
        released_year,
        github_rank,
        link,
        thumbnail,
        description,
        datetime.datetime.now(),
    )
    print("new Langugae: ", lang.serialize())
    db.insert(lang)
    new_langs = [b.serialize() for b in db.view()]
    print("Langauages in List: ", new_langs)

    return jsonify(
        {
            # 'error': '',
            "res": lang.serialize(),
            "status": "200",
            "msg": "Success creating a new book!👍😀",
        }
    )


@app.route("/request", methods=["GET"])
def getRequest():
    content_type = request.headers.get("Content-Type")
    langs = [b.serialize() for b in db.view()]
    if content_type == "application/json":
        json = request.json
        for l in langs:
            if l["id"] == int(json["id"]):
                return jsonify(
                    {
                        # 'error': '',
                        "res": l,
                        "status": "200",
                        "msg": "Success getting all Languesges!👍😀",
                    }
                )
        return jsonify(
            {
                "error": f"Error ⛔❌! Language with id '{json['id']}' not found!",
                "res": "",
                "status": "404",
            }
        )
    else:
        return jsonify(
            {
                # 'error': '',
                "res": langs,
                "status": "200",
                "msg": "Success getting all languages in The List!👍😀",
                "no_of_langs": len(langs),
            }
        )


@app.route("/request/<id>", methods=["GET"])
def getRequestId(id):
    req_args = request.view_args
    # print('req_args: ', req_args)
    langs = [l.serialize() for l in db.view()]
    if req_args:
        for l in langs:
            if l["id"] == int(req_args["id"]):
                return jsonify(
                    {
                        # 'error': '',
                        "res": l,
                        "status": "200",
                        "msg": "Success getting Language by ID!👍😀",
                    }
                )
        return jsonify(
            {
                "error": f"Error ⛔❌! Language with id '{req_args['id']}' was not found!",
                "res": "",
                "status": "404",
            }
        )
    else:
        return jsonify(
            {
                # 'error': '',
                "res": langs,
                "status": "200",
                "msg": "Success getting language by ID!👍😀",
                "no_of_books": len(langs),
            }
        )


@app.route("/request", methods=["PUT"])
def putRequest():
    req_data = request.get_json()
    name = req_data["name"]
    released_year = req_data["released_year"]
    github_rank = req_data["github_rank"]
    link = req_data["link"]
    thumbnail = req_data[" thumbnail"]
    description = req_data["description"]
    the_id = req_data["id"]
    langs = [l.serialize() for l in db.view()]
    for l in langs:
        if l["id"] == the_id:
            lang = Lang(
                the_id,
                name,
                released_year,
                github_rank,
                link,
                thumbnail,
                description,
                datetime.datetime.now(),
            )
            print("nwe book: ", lang.serialize())
            db.update(lang)
            new_bks = [b.serialize() for b in db.view()]
            print("books in lib: ", new_bks)
            return jsonify(
                {
                    # 'error': '',
                    "res": lang.serialize(),
                    "status": "200",
                    "msg": f"Success updating the Language Info!👍😀",
                }
            )
    return jsonify(
        {
            # 'error': '',
            "res": f"Error ⛔❌! Failed to update the Language Info!",
            "status": "404",
        }
    )


@app.route("/request/<id>", methods=["DELETE"])
def deleteRequest(id):
    req_args = request.view_args
    print("req_args: ", req_args)
    langs = [l.serialize() for l in db.view()]
    if req_args:
        for l in langs:
            if l["id"] == int(req_args["id"]):
                db.delete(l["id"])
                updated_langs = [l.serialize() for l in db.view()]
                print("updated_bks: ", updated_langs)
                return jsonify(
                    {
                        "res": updated_langs,
                        "status": "200",
                        "msg": "Success deleting Language by ID!👍😀",
                        "no_of_langs": len(updated_langs),
                    }
                )
    else:
        return jsonify(
            {"error": f"Error ⛔❌! No Language ID sent!", "res": "", "status": "404"}
        )


if __name__ == "__main__":
    app.run()

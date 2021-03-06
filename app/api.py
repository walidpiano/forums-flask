from flask import render_template, request, redirect, url_for, jsonify, abort
from app import models
from app import app, post_store


@app.route("/api/topic/all")
def topic_get_all():
    posts = [post.as_dict() for post in post_store.get_all()]
    return jsonify(posts)


@app.route("/api/topic/add", methods=["POST"])
def topic_add_api():
    request_data = request.get_json()
    try:
        new_post = models.Post(title=request.form["title"], content=request.form["content"])
        post_store.add(new_post)
        print(new_post)
        result = jsonify(new_post.as_dict())
    except KeyError:
        result = abort(400, f"couldn't parse the request data!")

    return result


@app.route("/api/topic/delete/<int:id>", methods=["DELETE"])
def topic_delete_api(id):
    try:
        post_store.delete(id)
        result = jsonify({"message": "Item deleted successfully!"})
    except ValueError:
        result = abort(404, f"topic with id: {id} doesn't exist!")

    return result


@app.route("/api/topic/show/<int:id>")
def topic_show_api(id):
    post_to_show = post_store.get_by_id(id)
    try:
        result = jsonify(post_to_show.__dict__())
    except AttributeError:
        result = abort(404, f"topic with id: {id} doesn't exist")

    return result


@app.route("/api/topic/update/<int:id>", methods=["PUT"])
def topic_update_api(id):
    request_data = request.get_json()
    topic_to_update = post_store.get_by_id(id)
    try:
        topic_to_update.title = request_data["title"]
        topic_to_update.content = request_data["content"]
        post_store.update(topic_to_update)
        result = jsonify(topic_to_update.as_dict())
    except AttributeError:
        result = abort(404, f"topic with id: {id} doesn't exist")
    except KeyError:
        result = abort(400, f"couldn't parse the request data")

    return result


@app.errorhandler(400)
def bad_request(error):
    return jsonify(message=error.description)
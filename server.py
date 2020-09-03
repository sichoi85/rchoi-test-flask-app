from definitions import APP_PATH
import sys
sys.path.append(APP_PATH)

import os
from db.BookModel import app
from flask import Flask, jsonify, request, Response
import json
from db.BookModel import Book
import uuid

from storage import blog_storage


# GET /books
DEFAULT_PAGE_LIMIT = 1


@app.route('/books')
def get_books():
    return jsonify({'books': Book.get_all_books()})


@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in Book.get_all_books():
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"]
            }
    return jsonify(return_value)

# GET /books/page/<int:page_number>


@app.route('/books/page/<int:page_number>')
def get_paginated_books(page_number):
    print(type(request.args.get('limit')))
    LIMIT = request.args.get('limit', DEFAULT_PAGE_LIMIT, int)
    return jsonify({'books': Book.get_all_books[page_number * LIMIT - LIMIT:page_number * LIMIT]})


def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

# POST /books


@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if(validBookObject(request_data)):
        Book.add_book(request_data['name'],
                      request_data['price'], request_data['isbn'])
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.99, 'isbn': 9780394800165 }"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg),
                            status=400, mimetype='application/json')
        return response


def valid_put_request_data(request_data):
    if("name" in request_data and "price" in request_data):
        return True
    else:
        return False

# PUT /books/page/<int:page_number>


@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if(not valid_put_request_data(request_data)):
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data should be passed in similar to this {'name': 'bookname', 'price': 7.99 }"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg),
                            status=400, mimetype='application/json')
        return response

    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }
    i = 0
    for book in books:
        currentIsbn = book["isbn"]
        if currentIsbn == isbn:
            books[i] = new_book
        i += 1
    response = Response("", status=204)
    return response


def valid_patch_request_data(request_data):
    if("name" in request_data or "price" in request_data):
        return True
    else:
        return False


@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    if(not valid_patch_request_data(request_data)):
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data should be passed in similar to this {'name': 'bookname', 'price': 7.99 }"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg),
                            status=400, mimetype='application/json')
        return response
    updated_book = {}
    if("price" in request_data):
        updated_book["price"] = request_data['price']
    if("name" in request_data):
        updated_book["name"] = request_data['name']
    for book in books:
        if book["isbn"] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response

# So let's go ahead first start the server up and do a GET request
# and see all the books we have.

# We see that the first book is named 'A', so let's go ahead and
# grab this books ISBN.

# Okay now that we have it, let's send a DELETE request to /books/isbn
# and pass this ISBN in

# So we are getting a 204 status code so that should mean this book was deleted.
# Let's now do a Get Request and see that this is indeed the case.

# Okay so we can see that this book is indeed deleted now.

# So now what happens if we run the Delete method again on that same ISBN?

# Take a second to pause the video and think about this.

# Okay so if we do a DELETE request, you would expect since that ISBN doesn't exist
# that translates to this file not existing in HTTP so we should expect to get back a 404.

# So let's run this again. We do see that we get a 404.

# But if you notice, we ran the same DELETE method twice but got different status codes.

# There is requirement when building a REST API that the DELETE protocol should be
# idempotent.

# What idempotence means is that if you do something to a system multiple times, the system
# remains the same.

# An example of this would be doing a GET request over and over again. Doing the same request
# over and over doesn't change the state of the server.

# The end result of this is you get back the same response over and over.

# This DELETE method needs to be indempotent as well, but as you see the first time
# you run this call you get a 204 response and then the second time you get a 404.

# So how can this be idempotent?

# So the thing to realize is that the server's state (whether the file exists or not) is
# different than the status codes we receive, and idempotence refers to the server state.

# So after that first DELETE, the book is deleted from the server.
# And regardless of how many times you run this this DELETE, the book will still be
# removed from the server.

# The status codes we receive back from the SERVER could also be indempotent (meaning)
# you receive the same status code after each request, but this is NOT necessary
# for the DELETE protocol.

# Since the server's state is the same, the method we developed is indeed indempotent.

# I wanted to clear this up in this video, because it's a fairly tricky concept that
# a lot of people have trouble with and that I haven't seen covered in any other tutorials/
# videos.

# DELETE /books/page/<int:page_number>


@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    i = 0
    books = Book.get_all_books()
    for book in books:
        if book["isbn"] == isbn:
            books.pop(i)
            response = Response("", status=204)
            return response
        i += 1
    invalidBookObjectErrorMsg = {
        "error": "Book with ISBN number provided not found, so unable to delete.",
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg),
                        status=404, mimetype='application/json')
    return response


@app.route('/test', methods=['GET'])
def test():
    return "%s, %s, %s" % (os.environ['password'], os.environ['FLASK_ENV'], os.environ['sql_rchoi_connection_string'])


@app.route("/im_size", methods=["POST"])
def get_image_size():
    file = request.files['image']
    # Read the image via file.stream
    img = Image.open(file.stream)

    return jsonify({'msg': 'success', 'size': [img.width, img.height]})


app.config["PROCESS_IMAGE"] = "./downloads"


@app.route("/process-image", methods=["GET", "POST"])
def process_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            image.save(os.path.join(
                app.config["IMAGE_UPLOADS"], image.filename))
            return google_vision_api.detect_text(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))


app.config['IMAGE_DOWNLOADS'] = './images'


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    con_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_storage_client = blog_storage.BlobStorageClient(con_str)
    if request.method == "POST":
        image = request.files["image"]
        file_name_on_storage = blob_storage_client.upload_file(image)
        return file_name_on_storage


# Start App
if __name__ == '__main__':
    app.run()


# Okay so in this video we ran some test cases and discussed what happens if we
# try to delete the same resource twice.

# We showed that our delete request was idempotent, which is a requirement for building
# a restful API.

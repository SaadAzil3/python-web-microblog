from flask import Flask, render_template, request, jsonify
from datetime import datetime
from pymongo import MongoClient

content_received = ""

def create_app():
    client = MongoClient("mongodb+srv://azilsaad114:6K8OmGrnXoc8IG3B@microblog-app.d6jv8x5.mongodb.net/")

    app = Flask(__name__)
    app.db = client.microblog

    entries = []
    entry_title = ""
    

    @app.route("/adminSaadAzil3", methods=["GET", "POST"])
    def Admin():
        if request.method=="POST":
            entry_title = request.form.get("title")
            entry_image = request.form.get("file")
            entry_content = request.form.get("content")
            date_formated = datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"title":entry_title, "content":entry_content, "date":date_formated, "image":entry_image})
        return render_template("index.html")
    @app.route("/", methods=["GET", "POST"])
    def Home():
        entries = [e for e in app.db.entries.find({})]
        entries = entries[::-1]
        entries_with_date = [(entry["title"], entry["content"], entry["date"], datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d"), len(entry["content"]), entry["image"]) for entry in entries]
        return render_template("article.html", entries=entries_with_date)
    @app.route('/receive_data_from_js', methods=['POST'])
    def receive_data_from_js():
        global content_received
        # Get the data from the request
        data_from_js = request.get_json()

        # Process the data as needed
        content_received = data_from_js.get('content', 'No content received from JavaScript')
        print(content_received)
        return jsonify({'message': 'Data received successfully'})
    
    @app.route("/Blog")
    def Article():
        global content_received
        print(content_received)
        your_variable = content_received
        result = app.db.entries.find_one({"title": your_variable})
        #entries = [e for e in app.db.entries.find({}) if e["title"]==entry_title]
        #entries_with_date = [(entry["title"], entry["content"], entry["date"], datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d"), len(entry["content"])) for entry in entries]
        return render_template("blog.html", entries=result)
    
    


    
    return app
    


import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from supabase import create_client, Client

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

# --- Supabase credentials ---
SUPABASE_URL = "https://cvnuwppsgrhzvmlfxxzb.supabase.co"  # replace with your project URL
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN2bnV3cHBzZ3JoenZtbGZ4eHpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI3Nzg3NjEsImV4cCI6MjA3ODM1NDc2MX0.7IhHKZdeIOLUScF4ui2xhSSxlok1FZVdQoUOtXAcaZA"                     # replace with your anon key
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        roll = request.form["roll"]
        file = request.files["img"]

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            # Upload to Supabase Storage (optional)
            # supabase.storage.from_("profile_images").upload(filename, file)

            # Insert into database
            supabase.table("profiles").insert({
                "name": name,
                "email": email,
                "roll": roll,
                "img": filename
            }).execute()

    # Fetch all data
    response = supabase.table("profiles").select("*").execute()
    data = response.data if response.data else []

    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)

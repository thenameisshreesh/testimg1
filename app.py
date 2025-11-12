import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from supabase import create_client, Client

app = Flask(__name__)

# --- Supabase credentials ---
SUPABASE_URL = "https://cvnuwppsgrhzvmlfxxzb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN2bnV3cHBzZ3JoenZtbGZ4eHpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI3Nzg3NjEsImV4cCI6MjA3ODM1NDc2MX0.7IhHKZdeIOLUScF4ui2xhSSxlok1FZVdQoUOtXAcaZA"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET_NAME = "uploads"


@app.route("/", methods=["GET", "POST"])
def index():
    message = None

    try:
        if request.method == "POST":
            name = request.form["name"]
            email = request.form["email"]
            roll = request.form["roll"]
            file = request.files["img"]

            if file and file.filename:
                filename = secure_filename(file.filename)

                # Read file bytes
                file_bytes = file.read()

                # ✅ Upload to Supabase Storage inside 'profile_images' folder
                supabase.storage.from_(BUCKET_NAME).upload(
                    f"profile_images/{filename}",
                    file_bytes,
                    {"content-type": file.content_type}
                )

                # ✅ Get public URL
                public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(f"profile_images/{filename}")

                # ✅ Insert record into database
                supabase.table("profiles").insert({
                    "name": name,
                    "email": email,
                    "roll": roll,
                    "img": public_url
                }).execute()

                message = "✅ Profile added successfully!"

        # Fetch all profiles
        response = supabase.table("profiles").select("*").execute()
        data = response.data if response.data else []

        return render_template("index.html", data=data, message=message)

    except Exception as e:
        # Log any error (for Vercel logs)
        print("ERROR:", e)
        return "Internal Server Error", 500


if __name__ == "__main__":
    app.run(debug=True)

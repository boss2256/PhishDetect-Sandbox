from flask import Flask, request, redirect, url_for, render_template_string, send_from_directory
from bs4 import BeautifulSoup
import os
from db.db_connection import save_dynamic_user_inputs

app = Flask(__name__)

# Route to serve each scraped website and dynamically modify the form action
@app.route('/<website_name>', methods=['GET', 'POST'])
def serve_website(website_name):
    template_path = f"templates/{website_name}/index.html"

    if request.method == 'POST':
        # Capture form data dynamically from the submitted form
        inputs = request.form.to_dict()
        save_dynamic_user_inputs(website_name, inputs)
        return redirect(url_for('serve_website', website_name=website_name))

    # Check if the template exists
    if os.path.exists(template_path):
        # Load and modify the HTML
        with open(template_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

            # Find the form and set its action to post back to the same route
            for form in soup.find_all('form'):
                form['action'] = f"/{website_name}"
                form['method'] = 'post'  # Ensure it uses POST for data capture

            # Render the modified HTML
            return render_template_string(str(soup))
    else:
        return "404 Not Found", 404

# Route to serve static assets (CSS, JS, images) for each website
@app.route('/<website_name>/<path:filename>')
def serve_static_files(website_name, filename):
    folder_path = os.path.join("templates", website_name)
    if os.path.exists(os.path.join(folder_path, filename)):
        return send_from_directory(folder_path, filename)
    else:
        return "404 Not Found", 404

if __name__ == '__main__':
    app.run(debug=True)

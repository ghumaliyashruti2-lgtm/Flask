from app import create_app
import os
from werkzeug.utils import secure_filename

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    app.config.from_object("config.Config")
    
    
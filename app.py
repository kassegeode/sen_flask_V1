from init_conf import create_app
from flask_cors import CORS

app = create_app()

if __name__ == '__main__':
    CORS(app)
    app.run(host=app.config['QR_HOST'], port=app.config['QR_PORT'])

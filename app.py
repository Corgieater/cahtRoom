from flask import *
import time
from model import *
import boto3

star_point = 0

app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)

app.register_blueprint(model_blueprint)

ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')


s3 = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_ACCESS_KEY,
)


def add_file_to_s3(filename):
    s3.upload_file(
        Bucket=BUCKET_NAME,
        Filename=filename,
        Key=filename
    )


BUCKET_NAME = 'bucket-for-dinners-project'
database = Database()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def save_data():
    # OMG THEY ARE NOT FROM THE SAME PLACE
    img = request.files['file']
    text = request.form['text']

    if text:
        if img:
            filename = f'{time.time()}' + '-' + img.filename
            img.save(filename)
            # 看起來這行是必要的
            print(filename)
            inputs = (None, text, filename)
            add_file_to_s3(filename)

        else:
            inputs = (None, text, None)
        is_added_to_db = database.add_to_database(inputs)
        if is_added_to_db:
            return {
                'ok': True
            }
        else:
            return {
                'error': True
            }

    else:
        return {
            'error': True,
            'message': 'Please enter something'
        }


@app.route('/getlatestdata')
def get_latest_data():
    latest_message = database.get_newest_data_from_database()
    data = {
        'text': latest_message[0],
        'fileName': latest_message[1]
    }
    return jsonify(data)


@app.route('/getolddata')
def get_old_data():
    data = database.get_old_data(0)
    json_data = {
        'data': {
            'text': [],
            'img': []
        }
    }
    for info in data:
        json_data['data']['text'].append(info[0])
        json_data['data']['img'].append(info[1])
    return jsonify(json_data)


if __name__ == '__main__':
    app.run(port=3000, debug=True)

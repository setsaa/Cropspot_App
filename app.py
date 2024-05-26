""" CropSpot Plant Disease Identification

"""
from flask import Flask, render_template, Response, jsonify, session

from image_processing import Processor
from camera_feed import generate_frames, take_picture

app = Flask(__name__, static_url_path='/static')
app.secret_key = '1234'  # Placeholder for development


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/capture_image')
def capture_image():
    image_path = take_picture()
    session['image_path'] = image_path  # Store image path in session
    return jsonify({'image_path': image_path}), 200


@app.route('/results')
def results():
    image_path = session.get('image_path')  # Retrieve image path from session

    if image_path:
        processor = Processor(model_path='model.h5')
        prediction = processor.process_image(image_path)
        prediction_dict = [{'Class': pred[0], 'Probability': f'{pred[1]*100:.2f}%'} for pred in prediction]
        print(prediction_dict)
        return render_template('results.html', prediction=prediction_dict)
    else:
        return "Image not found", 404


if __name__ == '__main__':
    app.run(debug=True)

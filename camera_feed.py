import os

import cv2


def generate_frames(stream_index=2):
    """ Generate frames from the camera feed.

    :param stream_index:
    :return:
    """
    print('Starting camera feed...')
    camera = cv2.VideoCapture(stream_index)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Concatenate frame and yield for streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    camera.release()


def take_picture(stream_index=2, filename="input_image.png"):
    """ Take a single image and save it.

    :param stream_index: Index of the camera to use.
    :param filename: Name of the file to save the image as (including extension).
    :return: The path where the image was saved.
    """
    print('Taking picture...')
    camera = cv2.VideoCapture(stream_index)
    ret, frame = camera.read()

    try:
        # Get the absolute path of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Create the full path to save the image
        image_path = os.path.join(script_dir, filename)

        cv2.imwrite(image_path, frame)
    except Exception as e:
        print('Could not take picture.')
        raise e

    print(f'Successfully captured image at: {image_path}')
    return image_path

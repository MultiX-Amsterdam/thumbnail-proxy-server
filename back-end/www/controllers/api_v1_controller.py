"""The controller for https://[PATH]/api/v1/"""

import time
import uuid
from flask import Blueprint
from flask import request
from flask import jsonify
from util.util import InvalidUsage
from util.util import handle_invalid_usage
from config.config import config
from models.model_operations.task_operations import create_task


bp = Blueprint("api_v1_controller", __name__)


@bp.route("/thumbnail", methods=["POST"])
def thumbnail():
    """
    The function for the front-end to pass the thumbnail server URL request.

    An example of the thumbnail server URL should look like below:
    http://localhost:3333/thumbnail?root=https%3A%2F%2Fbreathecam.org%2F%23v%3D1592%2C395%2C5563%2C2628%2Cpts%26t%3D2104.28%26ps%3D0%26bt%3D20241106020457%26et%3D20241106020457%26startDwell%3D0%26endDwell%3D0%26d%3D2024-11-05%26s%3Dclairton4%26fps%3D9&width=1280&height=720&format=png&fps=9&tileFormat=mp4&startDwell=0&endDwell=0&fromScreenshot&minimalUI&watermark=Breathe%20Project%7CCREATE%20Lab

    So everything after the "?" should be passed to the thumbnail server URL behind the firewall.

    Parameters
    ----------
    priority : int
        The priority of the task.
        Higher priority indicates that the task should be done faster.
        Larger number means higher priority (e.g., 5 has higher priority than 4).
    store_path : str
        The absolute path on this public server where the thumbnail server should rsync the file to.
        Example: "/usr11/uploads/foo.mp4"

    Returns
    -------
    A file returned using the flask.send_file function.
    """
    query_string = request.query_string.decode("utf-8")
    request_json = request.get_json()
    # create a task object
    # check the complete table for the presence of the ID generated for the task
    # have a while loop checking if the ID exit in the task table
    # sleep like 0.5 second in the while loop
    # (check if there is a way to handle this better than the while loop)
    # there is an event listener to detect the insert command of the complete table
    # detect inserts with sql alchemy orm
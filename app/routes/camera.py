from flask import Blueprint, jsonify, request
from app.middleware import token_required  # Ensure you have this middleware for security
from queue import Queue
from app.utils.pipelines import wait_and_run_pipeline
import time
import os

camera_bp = Blueprint("camera", __name__)

task_logs = {}
task_queue = Queue()
task_status = {}


# Background task function
def background_task(task_id):
    """
    This function runs the detection pipeline (with ESP32 trigger)
    in the background and updates the task status and logs.
    """
    def log_callback(msg):
        task_logs[task_id].append(f"{time.strftime('%H:%M:%S')} | {msg}")

    try:
        task_logs[task_id] = []  # Initialize log list

        # Wait for trigger and run pipeline with logging
        status = wait_and_run_pipeline(log_callback=log_callback)
        
        task_status[task_id] = {
            "status": status,
            "message": "Task completed successfully"
        }

    except Exception as e:
        task_status[task_id] = {
            "status": "error",
            "message": str(e)
        }
        task_logs[task_id].append(f"❌ Error: {str(e)}")


# Start detection route (Trigger detection pipeline in background)
@camera_bp.route("/start-detection", methods=["POST"])
@token_required  # Assuming token_required is your middleware to ensure the user is authenticated
def start_detection():
    """
    Start the detection process (with ESP32 trigger) in background.
    """
    task_id = str(int(time.time()))  # Use timestamp as task ID
    task_status[task_id] = {"status": "running", "message": "Task started."}

    # Start the background task in a separate thread
    from threading import Thread
    thread = Thread(target=background_task, args=(task_id,))
    thread.start()

    return jsonify({"task_id": task_id, "status": "Task started."}), 202

# Get task status route
@camera_bp.route("/task-status/<task_id>", methods=["GET"])
@token_required  # Ensure token_required middleware is applied
def get_task_status(task_id):
    """
    Fetch the status of a specific task by task_id.
    """
    if task_id not in task_status:
        return jsonify({"error": "Task not found"}), 404
    
    return jsonify(task_status[task_id])

# Get task results route
@camera_bp.route("/task-results/<task_id>", methods=["GET"])
@token_required  # Ensure token_required middleware is applied
def get_task_results(task_id):
    """
    Fetch the results of a task, including its status and detection result.
    """
    if task_id not in task_status or task_status[task_id]["status"] == "running":
        return jsonify({"error": "Task not completed yet."}), 400
    
    result = task_status[task_id]
    if result["status"] == "error":
        return jsonify({"error": result["message"]}), 500

    return jsonify({
        "status": result["status"],
        "message": result["message"],
        "detection_result": result["status"]
    })

# Get task logs route
@camera_bp.route("/task-logs/<task_id>", methods=["GET"])
@token_required  # Ensure token_required middleware is applied
def get_task_logs(task_id):
    """
    Fetch the logs of a specific task.
    """
    if task_id not in task_logs:
        return jsonify({"logs": []})
    return jsonify({"logs": task_logs[task_id]})

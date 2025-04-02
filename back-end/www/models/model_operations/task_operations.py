"""Functions to operate the task table."""

from models.model import db
from models.model import Task


def create_task(store_path, priority=1):
    """
    Create a task.

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
    task : Task
        The newly created task.
    """
    task = Task(store_path=store_path, priority=priority)

    db.session.add(task)
    db.session.commit()

    return task


def get_task_by_id(task_id):
    """
    Get a task by its ID.

    Parameters
    ----------
    task_id : int
        ID of the task.

    Returns
    -------
    task : Task
        The retrieved task object.
    """
    task = Task.query.filter_by(id=task_id).first()

    return task


def get_all_tasks():
    """
    Get all tasks.

    Returns
    -------
    tasks : list of Task
        The list of retrieved task objects.
    """
    tasks = Task.query.all()

    return tasks


def remove_task(task_id):
    """
    Remove a task.

    Parameters
    ----------
    task_id : int
        ID of the task.

    Raises
    ------
    exception : Exception
        When no task is found.
    """
    task = Task.query.filter_by(id=task_id).first()

    if task is None:
        raise Exception("No task found in the database to delete.")

    db.session.delete(task)
    db.session.commit()

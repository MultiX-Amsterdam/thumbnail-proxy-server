"""Database model for the application."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import MetaData


# Set the naming convention for database columns
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Initalize app with database
db = SQLAlchemy(metadata=MetaData(naming_convention=convention))


class Task(db.Model):
    """
    Class representing a queuing task.

    Attributes
    ----------
    id : int
        Unique identifier.
    created_at : datetime
        A timestamp indicating when the task is created in the queue.
    priority : int
        The priority of the task.
        Higher priority indicates that the task should be done faster.
        Larger number means higher priority (e.g., 5 has higher priority than 4).
    store_path : str
        The absolute path on this public server where the thumbnail server should rsync the file to.
        Example: "/usr11/uploads/foo.mp4"
    request_url : str
        The URL that should be passed to the thumbnail server behind the firewall.
    """
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    priority = db.Column(db.Integer, nullable=False, default=1)
    store_path = db.Column(db.Text(), nullable=False)
    request_url = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return "<Task id=%r created_at=%r priority=%r>" % (
            self.id, self.created_at, self.priority)


class Complete(db.Model):
    """
    Class representing a completed task.

    Attributes
    ----------
    id : int
        Unique identifier.
    completed_at : datetime
        A timestamp indicating when the task is completed.
    task_id : int
        The Task ID in the Task table (foreign key).
    """
    id = db.Column(db.Integer, primary_key=True)
    completed_at = db.Column(db.DateTime, server_default=func.now())
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    # Relationships
    task = db.relationship("Task", backref=db.backref("complete", lazy=True), lazy=True)

    def __repr__(self):
        return "<Complete id=%r completed_at=%r task_id=%r>" % (
            self.id, self.completed_at, self.task_id)
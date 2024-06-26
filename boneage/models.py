import os
from sqlalchemy import event
from sqlalchemy.exc import SQLAlchemyError

from boneage import db

class BoneAge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(1), nullable=False)
    age = db.Column(db.Float, nullable=False)
    pid = db.Column(db.String(20), nullable=False)
    study_datetime = db.Column(db.DateTime(), nullable=False)
    predictions = db.Column(db.Text(), nullable=True)
    instance_datetime = db.Column(db.DateTime(), nullable=False)
    instance_id = db.Column(db.String(200), nullable=False)
    series_id = db.Column(db.String(200), nullable=False)
    study_id = db.Column(db.String(200), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    create_predictions_date = db.Column(db.DateTime(), nullable=True)
    path_image = db.Column(db.String(300), nullable=True)
    status = db.Column(db.String(20), nullable=True, server_default='Wait')

# Event listener for the deletion of Model
@event.listens_for(BoneAge, 'before_delete')
def receive_before_delete(mapper, connection, target):
    if os.path.exists(target.path_image):
        try:
            os.remove(target.path_image)
            # print(f"Deleted file: {target.path_image}")
        except Exception as e:
            print(f"Error deleting file: {target.path_image}, Error: {e}")
            raise SQLAlchemyError(f"Error deleting file: {target.path_image}, Error: {e}")
    else:
        print(f"File not found: {target.path_image}")
        raise SQLAlchemyError(f"File not found: {target.path_image}")
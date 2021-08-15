from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()
Base = declarative_base()


def setup_db(app, database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    db.create_all()


def cleanup_db(app, database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    db.drop_all()
    db.session.close()


# Association Tables
user_workout_assoc_table = Table('user_workout', Base.metadata,
                                 Column('user_id', ForeignKey('user.id'), primary_key=True),
                                 Column('workout_id', ForeignKey('workout.id'), primary_key=True)
                                 )

workout_set_assoc_table = Table('workout_set', Base.metadata,
                                Column('workout_id', ForeignKey('workout.id'), primary_key=True),
                                Column('set_id', ForeignKey('set.id'), primary_key=True)
                                )

exercise_muscle_assoc_table = Table('exercise_muscle', Base.metadata,
                                    Column('exercise_id', ForeignKey('exercise.id'), primary_key=True),
                                    Column('muscle_id', ForeignKey('muscle.id'), primary_key=True)
                                    )

exercise_set_assoc_table = Table('exercise_set', Base.metadata,
                                 Column('exercise_id', ForeignKey('exercise.id'), primary_key=True),
                                 Column('set_id', ForeignKey('set.id'), primary_key=True)
                                 )


class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)


class Plan(db.Model):
    __tablename__ = 'plan'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String(500), nullable=True)


class Workout(db.Model):
    __tablename__ = 'workout'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=True)
    date = Column(DateTime, nullable=False)
    user = relationship("User",
                        secondary=user_workout_assoc_table,
                        backref=db.backref('workouts',
                                           lazy=True,
                                           cascade="all, delete-orphan"
                                           )
                        )
    sets = relationship("Set",
                        secondary=workout_set_assoc_table,
                        backref=db.backref('workouts',
                                           lazy=True,
                                           cascade="all, delete-orphan"
                                           )
                        )


class Exercise(db.Model):
    __tablename__ = 'exercise'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    instructions = Column(String(500), nullable=True)
    sets = relationship("Set",
                        secondary=exercise_set_assoc_table,
                        backref=db.backref('exercises',
                                           lazy=True,
                                           cascade="all, delete-orphan"
                                           )
                        )
    muscles = relationship("Muscle",
                           secondary=exercise_muscle_assoc_table,
                           backref=db.backref('exercises',
                                              lazy=True)
                           )


class Set(db.Model):
    __tablename__ = 'set'

    id = Column(Integer, primary_key=True)
    set_number = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    repetitions = Column(Integer, nullable=False)
    workout = relationship('Workout', backref=db.backref('sets'), lazy=True, cascade="all, delete-orphan")


class Muscle(db.Model):
    __tablename__ = 'muscle'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)

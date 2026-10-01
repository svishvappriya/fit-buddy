import os
from datetime import datetime
from typing import Generator, List, Optional
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session

# Configure absolute path to fitbuddy.db at the project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "fitbuddy.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# SQLAlchemy engine setup with check_same_thread=False for SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    goal = Column(String, nullable=False)
    intensity = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    plans = relationship("WorkoutPlan", back_populates="user", cascade="all, delete-orphan", lazy="joined")


class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_plan = Column(Text, nullable=False)
    updated_plan = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="plans")


def get_db() -> Generator[Session, None, None]:
    """Dependency generator providing transactional database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_user(user_id: int, name: str, age: int, weight: float, goal: str, intensity: str) -> User:
    """Insert or update user record with explicit session lifecycle."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.name = name
            user.age = age
            user.weight = weight
            user.goal = goal
            user.intensity = intensity
        else:
            user = User(
                id=user_id,
                name=name,
                age=age,
                weight=weight,
                goal=goal,
                intensity=intensity,
                created_at=datetime.utcnow()
            )
            db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()


def save_plan(user_id: int, plan: str) -> WorkoutPlan:
    """Save initial workout plan for a user."""
    db = SessionLocal()
    try:
        workout = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
        if workout:
            workout.original_plan = plan
            workout.updated_plan = None
            workout.created_at = datetime.utcnow()
        else:
            workout = WorkoutPlan(
                user_id=user_id,
                original_plan=plan,
                updated_plan=None,
                created_at=datetime.utcnow()
            )
            db.add(workout)
        db.commit()
        db.refresh(workout)
        return workout
    finally:
        db.close()


def update_plan(user_id: int, updated_text: str) -> Optional[WorkoutPlan]:
    """Update the updated_plan column for an existing user."""
    db = SessionLocal()
    try:
        workout = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
        if workout:
            workout.updated_plan = updated_text
            db.commit()
            db.refresh(workout)
            return workout
        return None
    finally:
        db.close()


def get_original_plan(user_id: int) -> Optional[str]:
    """Fetch original plan text by user id."""
    db = SessionLocal()
    try:
        workout = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
        if workout:
            return workout.original_plan
        return None
    finally:
        db.close()


def get_user(user_id: int) -> Optional[User]:
    """Fetch single user object by user id."""
    db = SessionLocal()
    try:
        return db.query(User).filter(User.id == user_id).first()
    finally:
        db.close()


def get_all_users_with_plans() -> List[User]:
    """Fetch all users joined with their workout plans."""
    db = SessionLocal()
    try:
        return db.query(User).order_by(User.id.asc()).all()
    finally:
        db.close()

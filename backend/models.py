from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    userID = Column(Integer, primary_key=True, index=True)
    fullName = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    passwordHash = Column(String, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
class MealType(Base):
    __tablename__ = "meal_types"
    mealTypeID = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=False)
class Recipe(Base):
    __tablename__ = "recipes"
    recipeID = Column(Integer, primary_key=True, index=True)
    mealTypeID = Column(Integer, ForeignKey("meal_types.mealTypeID"), nullable=False)
    title = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    prepTime = Column(String, nullable=False)
    ingredients = Column(JSON, nullable=False)
    instructions = Column(JSON, nullable=False)
    imageUrl = Column(String, nullable=True)

    meal_type = relationship("MealType")
class WeightRecord(Base):
    __tablename__ = "weight_records"
    recordID = Column(Integer, primary_key=True, index=True)
    userID = Column(Integer, ForeignKey("users.userID"), nullable=False)
    weight = Column(Float, nullable=False)
    recordDate = Column(DateTime, default=datetime.utcnow)
class BodyPart(Base):
    __tablename__ = "body_parts"
    bodyPartID = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=False)

class ExerciseVideo(Base):
    __tablename__ = "exercise_videos"
    videoID = Column(Integer, primary_key=True, index=True)
    bodyPartID = Column(Integer, ForeignKey("body_parts.bodyPartID"), nullable=False)
    title = Column(String, nullable=False)
    duration = Column(String, nullable=False)
    videoUrl = Column(String, nullable=False)
    thumbnailUrl = Column(String, nullable=True)
class Favorite(Base):
    __tablename__ = "favorites"
    userID = Column(Integer, ForeignKey("users.userID"), primary_key=True)
    recipeID = Column(Integer, ForeignKey("recipes.recipeID"), primary_key=True)

class QuestionAnswer(Base):
    __tablename__ = "question_answers"
    qaID = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    isActive = Column(Boolean, default=True)
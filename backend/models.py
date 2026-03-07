from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

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

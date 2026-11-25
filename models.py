from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable= False)
    description: Mapped[str] = mapped_column(String(300), nullable = True)
    completed: Mapped[bool] = mapped_column(Boolean, default= False)
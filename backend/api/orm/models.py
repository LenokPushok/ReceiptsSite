from sqlalchemy import Column, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, NUMERIC
from sqlalchemy.orm import relationship

from api.orm.base import Base


class User(Base):
    username = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    role_id = Column(UUID, ForeignKey("role.id"), nullable=False)

    role = relationship("Role", back_populates="users", uselist=False)
    reviews = relationship("Review", back_populates="user", uselist=True)


class Role(Base):
    title = Column(Text, nullable=False)

    users = relationship("User", back_populates="role", uselist=True)


class File(Base):
    path = Column(Text, nullable=False)


class Movie(Base):
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    imdb_rating = Column(NUMERIC, nullable=False)
    logo_file_id = Column(UUID, ForeignKey("file.id"), nullable=False)

    logo_file = relationship("File", uselist=False)
    reviews = relationship("Review", back_populates="movie", uselist=True)


class Review(Base):
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    movie_id = Column(UUID, ForeignKey("movie.id"), nullable=False)
    content = Column(Text, nullable=False)
    rating = Column(NUMERIC, nullable=False)
    status = Column(Text, nullable=False)

    user = relationship("User", back_populates="reviews", uselist=False)
    movie = relationship("Movie", back_populates="reviews", uselist=False)

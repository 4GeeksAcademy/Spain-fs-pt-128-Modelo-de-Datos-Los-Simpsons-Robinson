from flask_sqlalchemy import SQLAlchemy
from typing import List, Optional
from sqlalchemy import String, func, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

# Tablas intermedias corregidas
favorite_character = Table(
    "favorite_character",
    db.metadata,
    Column("id", db.Integer, primary_key=True),
    Column("user_id", ForeignKey("user.id"), nullable=False),
    Column("character_id", ForeignKey("character.id"), nullable=True)
)

favorite_location = Table(
    "favorite_location",
    db.metadata,
    Column("id", db.Integer, primary_key=True),
    Column("user_id", ForeignKey("user.id"), nullable=False),
    Column("location_id", ForeignKey("location.id"), nullable=True)
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    
    # Nombres actualizados a favorites_characters
    favorites_characters: Mapped[List["Character"]] = relationship(
        "Character",
        secondary=favorite_character,
        back_populates="users_who_favorited",
    )

    # Nombres actualizados a favorites_locations
    favorites_locations: Mapped[List["Location"]] = relationship(
        "Location",
        secondary=favorite_location,
        back_populates="users_who_favorited"
    )

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
        }

    def serialize_complete(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "favorites": {                
                "characters": [dict(character.serialize(), type="personaje") for character in self.favorites_characters],
                "locations": [dict(location.serialize(), type="ubicacion") for location in self.favorites_locations]
            }
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    age: Mapped[Optional[int]] = mapped_column(nullable=True)
    birthdate: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(String(60))
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    occupation: Mapped[str] = mapped_column(String(255))
    
    users_who_favorited: Mapped[List["User"]] = relationship(
        secondary=favorite_character,
        back_populates="favorites_characters",
    )

    phrases: Mapped[List["Phrase"]] = relationship(
        back_populates="character"
    )
    status: Mapped[str] = mapped_column(String(120), nullable=False)

    def __repr__(self):
        return self.name

    def serialize(self):
        return {
            "id": self.id,
            "age": self.age,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "name": self.name,
            "occupation": self.occupation,            
            "phrases": ", ".join([phrase.text for phrase in self.phrases]) if self.phrases else "Unknown",
            "status": self.status
        }


class Phrase(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))
    character: Mapped["Character"] = relationship(back_populates="phrases")

    def serialize(self):
        return self.text


class Location(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)    
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    image_path: Mapped[str] = mapped_column(String(255), nullable=False)
    town: Mapped[str] = mapped_column(String(255), nullable=False)
    use: Mapped[str] = mapped_column(String(255), nullable=False)
    
    users_who_favorited: Mapped[List["User"]] = relationship(
        secondary=favorite_location,
        back_populates="favorites_locations",
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image_path,
            "town": self.town,
            "use": self.use,            
            "description": self.description if self.description else "Unknown"
        }


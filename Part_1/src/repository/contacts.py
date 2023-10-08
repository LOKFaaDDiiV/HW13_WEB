from typing import List
from datetime import datetime, timedelta

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactUpdate


async def find_contacts(db: Session, user: User,
                        firstname: str = None, lastname: str = None, email: str = None) -> List[Contact]:

    query = db.query(Contact).filter(Contact.user_id == user.id)

    if firstname:
        query = query.filter(Contact.firstname.ilike(f"%{firstname}%"))
    if lastname:
        query = query.filter(Contact.lastname.ilike(f"%{lastname}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))

    contact = query.all()

    return contact


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def get_birthdays(num_days: int, user: User, db: Session) -> List[Contact]:

    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    today = datetime.now().date()
    end_date = today + timedelta(days=num_days)
    nearest_birthdays = []

    for contact in contacts:

        contact_birth_in_this_year = contact.born_date.replace(year=today.year)

        if today <= contact_birth_in_this_year <= end_date:
            nearest_birthdays.append(contact)

    return nearest_birthdays


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:

    contact = Contact(firstname=body.firstname, lastname=body.lastname, phone_number=body.phone_number,
                      email=body.email, born_date=body.born_date, user=user)

    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact


async def update_contact(contact_id: int, body: ContactUpdate, user: User, db: Session) -> Contact | None:

    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()

    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.phone_number = body.phone_number
        contact.email = body.email
        contact.born_date = body.born_date
        db.commit()

    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:

    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()

    if contact:
        db.delete(contact)
        db.commit()

    return contact

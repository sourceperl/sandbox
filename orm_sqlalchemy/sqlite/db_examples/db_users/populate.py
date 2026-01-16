import logging

from db import Address, User, engine
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

Session = sessionmaker(bind=engine)

with Session() as session:
    try:
        user1 = User(name='John Doe')
        user1.addresses = [
            Address(email_address='john@example.com'),
            Address(email_address='john.doe@example.com')
        ]

        user2 = User(name='Jane Smith')
        user2.addresses = [
            Address(email_address='jane@example.com'),
            Address(email_address='jane.smith@example.com')
        ]

        session.add_all([user1, user2])

        # the commit is where most database errors actually occur
        session.commit()

    except IntegrityError as e:
        # specific error: e.g., duplicate email or null constraint
        session.rollback()
        logger.error(f'integrity error (duplicate or constraint): {e}')
    except SQLAlchemyError as e:
        # general sqlalchemy error
        session.rollback()
        logger.error(f'database error: {e}')
    except Exception as e:
        # catch-all for logic errors
        session.rollback()
        logger.error(f'unexpected error: {e}')
        logger.error(f'unexpected error: {e}')

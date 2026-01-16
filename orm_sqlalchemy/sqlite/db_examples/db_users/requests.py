from db import Address, User, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(engine)

with Session() as session:
    for user in session.query(User).join(Address).all():
        print(f'User: {user.name}')
        for address in user.addresses:
            print(f' - Address: {address.email_address}')

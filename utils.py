from database import Base, engine


def initialize_tables(cls):
    def wrapper(*args, **kwargs):
        Base.metadata.create_all(bind=engine)
        return cls(*args, **kwargs)
    return wrapper

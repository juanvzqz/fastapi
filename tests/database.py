# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# # from sqlalchemy.ext.declarative import declarative_base
# from app.main import app
# from app.config import settings
# from app.database import get_db, Base
# import pytest
#
#
# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:' \
#                           f'{settings.database_password}@' \
#                           f'{settings.database_hostname}:{settings.database_port}/' \
#                           f'{settings.database_name}_test'
#
#
# # Create Test DB
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
#
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
# # Check documentation: Fixture Scopes
# @pytest.fixture(scope="function")
# def session():
#     # First drop all tables
#     Base.metadata.drop_all(bind=engine)
#     # Second create the new tables
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# # Fixture to create and drop tables every time we run a test
# # This avoids duplication exceptions
# @pytest.fixture(scope="function")
# def client(session):
#     def override_get_db():
#         try:
#             yield session
#         finally:
#             session.close()
#
#     app.dependency_overrides[get_db] = override_get_db
#     yield TestClient(app)

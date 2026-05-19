import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.schemas import GameCreate
from app import service


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_add_game_creates_game(db_session):
    created = service.add_game(
        db_session,
        GameCreate(
            title="Hades",
            genre="Roguelike",
            platform="PC",
            release_year=2020,
            cover_url="https://example.com/hades.jpg",
        ),
    )

    assert created.id
    assert created.title == "Hades"


def test_get_game_by_id(db_session):
    created = service.add_game(
        db_session,
        GameCreate(title="Celeste", genre="Platformer", platform="PC"),
    )

    fetched = service.fetch_game(db_session, created.id)
    assert fetched.id == created.id
    assert fetched.title == "Celeste"


def test_get_game_unknown_id_raises_value_error(db_session):
    with pytest.raises(ValueError):
        service.fetch_game(db_session, "unknown-id")


def test_list_games_returns_total(db_session):
    service.add_game(db_session, GameCreate(title="FIFA 25", genre="Sports", platform="PS5"))
    service.add_game(db_session, GameCreate(title="Forza", genre="Racing", platform="Xbox"))

    result = service.fetch_all_games(db_session, limit=20, offset=0)
    assert result.total == 2
    assert len(result.items) == 2


def test_search_games_by_title(db_session):
    service.add_game(db_session, GameCreate(title="Halo Infinite", genre="FPS", platform="Xbox"))
    service.add_game(db_session, GameCreate(title="Stardew Valley", genre="Simulation", platform="PC"))

    result = service.find_games(db_session, q="halo", limit=20, offset=0)
    assert result.total == 1
    assert result.items[0].title == "Halo Infinite"

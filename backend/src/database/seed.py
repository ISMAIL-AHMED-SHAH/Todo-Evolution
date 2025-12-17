"""
Database seeding script for development and testing

This script creates sample users and tasks for development and testing purposes.
It's safe to run multiple times - it will skip creating duplicate users.
"""
import logging
from sqlmodel import Session, select
from src.database.database import engine, get_db_session
from src.models.user import User
from src.models.task import Task
from src.auth.auth_handler import get_password_hash

logger = logging.getLogger(__name__)


def seed_users(session: Session) -> dict[str, User]:
    """
    Seed sample users for development

    Creates three test users if they don't already exist:
    - demo@example.com (Demo User)
    - alice@example.com (Alice)
    - bob@example.com (Bob)

    Args:
        session: Database session

    Returns:
        dict: Dictionary mapping email to User object
    """
    users_data = [
        {"email": "demo@example.com", "password": "demo123"},
        {"email": "alice@example.com", "password": "alice123"},
        {"email": "bob@example.com", "password": "bob123"},
    ]

    users = {}

    for user_data in users_data:
        # Check if user already exists
        existing_user = session.exec(
            select(User).where(User.email == user_data["email"])
        ).first()

        if existing_user:
            logger.info(f"User {user_data['email']} already exists, skipping")
            users[user_data["email"]] = existing_user
        else:
            # Create new user
            user = User(
                email=user_data["email"],
                password_hash=get_password_hash(user_data["password"])
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            users[user_data["email"]] = user
            logger.info(f"Created user: {user_data['email']}")

    return users


def seed_tasks(session: Session, users: dict[str, User]) -> None:
    """
    Seed sample tasks for development

    Creates sample tasks for each user if they don't have tasks yet.

    Args:
        session: Database session
        users: Dictionary of users (email -> User)
    """
    # Demo user tasks
    demo_user = users.get("demo@example.com")
    if demo_user:
        # Check if user already has tasks
        existing_tasks = session.exec(
            select(Task).where(Task.user_id == demo_user.id)
        ).all()

        if not existing_tasks:
            demo_tasks = [
                Task(
                    user_id=demo_user.id,
                    title="Welcome to the Todo App!",
                    description="This is a sample task. You can edit or delete it.",
                    completed=False
                ),
                Task(
                    user_id=demo_user.id,
                    title="Buy groceries",
                    description="Milk, bread, eggs, and cheese",
                    completed=False
                ),
                Task(
                    user_id=demo_user.id,
                    title="Complete project documentation",
                    description="Write comprehensive documentation for the API",
                    completed=True
                ),
                Task(
                    user_id=demo_user.id,
                    title="Review pull requests",
                    description="Review and merge pending PRs",
                    completed=False
                ),
            ]
            for task in demo_tasks:
                session.add(task)
            logger.info(f"Created {len(demo_tasks)} tasks for demo@example.com")

    # Alice's tasks
    alice = users.get("alice@example.com")
    if alice:
        existing_tasks = session.exec(
            select(Task).where(Task.user_id == alice.id)
        ).all()

        if not existing_tasks:
            alice_tasks = [
                Task(
                    user_id=alice.id,
                    title="Finish quarterly report",
                    description="Complete Q4 analysis and projections",
                    completed=False
                ),
                Task(
                    user_id=alice.id,
                    title="Team meeting preparation",
                    description="Prepare slides for Monday's team sync",
                    completed=True
                ),
                Task(
                    user_id=alice.id,
                    title="Code review",
                    description="Review backend API changes",
                    completed=False
                ),
            ]
            for task in alice_tasks:
                session.add(task)
            logger.info(f"Created {len(alice_tasks)} tasks for alice@example.com")

    # Bob's tasks
    bob = users.get("bob@example.com")
    if bob:
        existing_tasks = session.exec(
            select(Task).where(Task.user_id == bob.id)
        ).all()

        if not existing_tasks:
            bob_tasks = [
                Task(
                    user_id=bob.id,
                    title="Fix authentication bug",
                    description="Investigate and fix the login issue reported by users",
                    completed=True
                ),
                Task(
                    user_id=bob.id,
                    title="Update dependencies",
                    description="Upgrade all packages to latest stable versions",
                    completed=False
                ),
                Task(
                    user_id=bob.id,
                    title="Write unit tests",
                    description="Add test coverage for new API endpoints",
                    completed=False
                ),
                Task(
                    user_id=bob.id,
                    title="Deploy to staging",
                    description="Deploy latest changes to staging environment",
                    completed=True
                ),
                Task(
                    user_id=bob.id,
                    title="Performance optimization",
                    description="Optimize database queries for faster response times",
                    completed=False
                ),
            ]
            for task in bob_tasks:
                session.add(task)
            logger.info(f"Created {len(bob_tasks)} tasks for bob@example.com")

    session.commit()


def seed_database():
    """
    Main function to seed the database with sample data

    Creates:
    - 3 sample users (demo, alice, bob)
    - Sample tasks for each user

    Safe to run multiple times - skips existing data.
    """
    logger.info("Starting database seeding...")

    try:
        with get_db_session() as session:
            # Seed users
            users = seed_users(session)
            logger.info(f"Seeded {len(users)} users")

            # Seed tasks
            seed_tasks(session, users)
            logger.info("Seeded tasks for all users")

        logger.info("Database seeding completed successfully!")
        logger.info("\nTest credentials:")
        logger.info("  demo@example.com / demo123")
        logger.info("  alice@example.com / alice123")
        logger.info("  bob@example.com / bob123")

    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        raise


def clear_database():
    """
    Clear all data from the database

    WARNING: This will delete ALL users and tasks!
    Use only in development/testing environments.
    """
    logger.warning("Clearing database...")

    try:
        with get_db_session() as session:
            # Delete all tasks
            tasks = session.exec(select(Task)).all()
            for task in tasks:
                session.delete(task)

            # Delete all users
            users = session.exec(select(User)).all()
            for user in users:
                session.delete(user)

            session.commit()
            logger.info("Database cleared successfully")

    except Exception as e:
        logger.error(f"Error clearing database: {e}")
        raise


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Run seeding
    seed_database()

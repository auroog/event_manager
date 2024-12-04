from builtins import repr
from datetime import datetime, timezone
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import User, UserRole

@pytest.mark.asyncio
async def test_user_role(db_session: AsyncSession, user: User, admin_user: User, manager_user: User):
    """
    Testing user role.
    """
    assert user.role == UserRole.AUTHENTICATED
    assert admin_user.role == UserRole.ADMIN
    assert manager_user.role == UserRole.MANAGER

@pytest.mark.asyncio
async def test_has_role(user: User, admin_user: User, manager_user: User):
    """
    Tests to ensure the user's role.
    """
    assert user.has_role(UserRole.AUTHENTICATED)
    assert not user.has_role(UserRole.ADMIN)
    assert admin_user.has_role(UserRole.ADMIN)
    assert manager_user.has_role(UserRole.MANAGER)

@pytest.mark.asyncio
async def test_user_repr(user: User):
    """
    Tests for accurate representation of the User object.
    """
    assert repr(user) == f"<User {user.nickname}, Role: {user.role.name}>", "__repr__ should include nickname and role"

@pytest.mark.asyncio
async def test_failed_login_attempts_increment(db_session: AsyncSession, user: User):
    """
    Tests that failed login attempts increment.
    """
    initial_attempts = user.failed_login_attempts
    user.failed_login_attempts += 1
    await db_session.commit()
    await db_session.refresh(user)
    assert user.failed_login_attempts == initial_attempts + 1

@pytest.mark.asyncio
async def test_last_login_update(db_session: AsyncSession, user: User):
    """
    Tests updating the last login timestamp.
    """
    new_last_login = datetime.now(timezone.utc)
    user.last_login_at = new_last_login
    await db_session.commit()
    await db_session.refresh(user)
    assert user.last_login_at == new_last_login

@pytest.mark.asyncio
async def test_account_lock_and_unlock(db_session: AsyncSession, user: User):
    """
    Tests locking and unlocking the user account.
    """
    # Initially, the account should not be locked.
    assert not user.is_locked

    # Lock the account and verify.
    user.lock_account()
    await db_session.commit()
    await db_session.refresh(user)
    assert user.is_locked

    # Unlock the account and verify.
    user.unlock_account()
    await db_session.commit()
    await db_session.refresh(user)
    assert not user.is_locked

@pytest.mark.asyncio
async def test_email_verification(db_session: AsyncSession, user: User):
    """
    Tests the email verification function
    """
    # Initially, the email should not be verified.
    assert not user.email_verified

    # Verify the email and check.
    user.verify_email()
    await db_session.commit()
    await db_session.refresh(user)
    assert user.email_verified

@pytest.mark.asyncio
async def test_user_profile_pic_url_update(db_session: AsyncSession, user: User):
    """
    Tests the profile picture update.
    """
    # Initially, the profile pic should be updated.

    # Verify the email and check.
    profile_pic_url = "http://myprofile/picture.png"
    user.profile_picture_url = profile_pic_url
    await db_session.commit()
    await db_session.refresh(user)
    assert user.profile_picture_url == profile_pic_url, "The profile picture did not update"

@pytest.mark.asyncio
async def test_user_linkedin_url_update(db_session: AsyncSession, user: User):
    """
    Tests the profile picture update.
    """
    # Initially, the linkedin should  be updated.

    # Verify the linkedin profile url.
    profile_linkedin_url = "http://www.linkedin.com/profile"
    user.linkedin_profile_url = profile_linkedin_url
    await db_session.commit()
    await db_session.refresh(user)
    assert user.linkedin_profile_url == profile_linkedin_url, "The profile picture did not update"


@pytest.mark.asyncio
async def test_user_github_url_update(db_session: AsyncSession, user: User):
    """
    Tests the profile picture update.
    """
    # Initially, the linkedin should  be updated.

    # Verify the linkedin profile url.
    profile_github_url = "http://www.github.com/profile"
    user.github_profile_url = profile_github_url
    await db_session.commit()
    await db_session.refresh(user)
    assert user.github_profile_url == profile_github_url, "The github did not update"

@pytest.mark.asyncio
async def test_default_role_assignment(db_session: AsyncSession):
    """
    Tests that a user without any role.
    """
    user = User(nickname="noob", email="newuser@example.com", hashed_password="hashed_password")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    assert user.role == UserRole.ANONYMOUS, "Default role should be 'anonymous' if not specified"

@pytest.mark.asyncio
async def test_update_user_role(db_session: AsyncSession, user: User):
    """
    Tests updating the user's role and ensuring it persists correctly.
    """
    user.role = UserRole.ADMIN
    await db_session.commit()
    await db_session.refresh(user)
    assert user.role == UserRole.ADMIN

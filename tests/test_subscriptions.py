import pytest
from src.subscriptions import SubscriptionManager as sm
from sqlalchemy.exc import IntegrityError

def test_subscribe_user_to_source_success(manager):
    manager.subscribe_user_to_source(1, 1) # Subscribed alice to bbc news
    #check
    alice_subs = manager.get_user_feed(1)
    assert alice_subs.get("BBC News") is not None

def test_subscribe_user_to_source_nonexistent_user(manager):
    with pytest.raises(ValueError, match="No such a user"):
        manager.subscribe_user_to_source(4, 1)

def  test_subscribe_user_to_source_nonexistent_source(manager):
    with pytest.raises(ValueError, match="No such a source"):
        manager.subscribe_user_to_source(1, 6)

def test_subscribe_user_to_source_duplicate_subscription(manager):
    with pytest.raises(IntegrityError):
        manager.subscribe_user_to_source(1, 2)# Alice to CNN
        manager.subscribe_user_to_source(1, 2)# Again, should raise IntegrityError

def test_get_user_feed_success(manager):
    manager.subscribe_user_to_source(1, 3) # Subscribed alice to TechCrunch news
    #check
    alice_subs = manager.get_user_feed(1)
    assert alice_subs["TechCrunch"] == (3, "https://techcrunch.com/feed/")

def test_get_user_feed_empty_for_new_user(manager):
    bob_subs =  manager.get_user_feed(2)
    assert len(bob_subs) == 0

def test_get_user_feed_nonexistent_user(manager):
    with pytest.raises(ValueError, match="No such a user"):
        nonexistent_user_subs = manager.get_user_feed(5)

def test_unsubscripe_success(manager):
    manager.subscribe_user_to_source(3, 1)#subsribe charlie to BBC News
    #Unsubscribe
    feeds = manager.get_user_feed(3)
    assert feeds.get("BBC News") is not None
    manager.unsubscripe(3, 1)
    feeds = manager.get_user_feed(3)
    assert feeds.get("BBC News") is None


def test_unsubscripe_nonexistent(manager):
    with pytest.raises(ValueError, match="No such a subscription"):
        manager.unsubscripe(3, 5)
"""Subscription service: check active subscription and CRUD operations.

This file was recreated to remove previous merge conflict markers.
"""
from datetime import datetime, timezone
from typing import Optional

from infrastructure.databases.mssql import session
from infrastructure.models import Subscription


class SubscriptionService:
    def __init__(self, db_session=None):
        self.session = db_session or session

    def check_household_subscription_active(self, household_id: int) -> bool:
        if not household_id:
            # Admin/system calls may pass no household; treat as allowed
            return True
        return self.get_active_subscription(household_id) is not None

    def get_active_subscription(self, household_id: int) -> Optional[Subscription]:
        if not household_id:
            return None

        subscription = (
            self.session.query(Subscription)
            .filter_by(household_id=household_id, is_active=True)
            .first()
        )

        if not subscription:
            return None

        # Compare end_date taking timezone-awareness into account
        now = datetime.now(timezone.utc)
        if hasattr(subscription.end_date, "tzinfo") and subscription.end_date.tzinfo:
            return subscription if subscription.end_date >= now else None
        return subscription if subscription.end_date >= datetime.utcnow() else None

    def create_subscription(
        self,
        household_id: int,
        plan_id: int,
        start_date: datetime,
        end_date: datetime,
        is_active: bool = True,
        allow_multiple: bool = False,
    ) -> Subscription:
        if not allow_multiple and self.get_active_subscription(household_id):
            raise ValueError("Household already has an active subscription")

        subscription = Subscription(
            household_id=household_id,
            plan_id=plan_id,
            start_date=start_date,
            end_date=end_date,
            is_active=is_active,
            created_at=datetime.now(timezone.utc).replace(tzinfo=None),
            updated_at=datetime.now(timezone.utc).replace(tzinfo=None),
        )
        self.session.add(subscription)
        self.session.commit()
        self.session.refresh(subscription)
        return subscription

    def list_subscriptions(self):
        return self.session.query(Subscription).all()

    def get_subscription(self, subscription_id: int) -> Optional[Subscription]:
        return self.session.query(Subscription).filter_by(id=subscription_id).first()

    def update_subscription(
        self,
        subscription_id: int,
        household_id: int = None,
        plan_id: int = None,
        start_date: datetime = None,
        end_date: datetime = None,
        is_active: bool = None,
    ) -> Subscription:
        subscription = self.get_subscription(subscription_id)
        if not subscription:
            raise ValueError("Subscription not found")
        if household_id is not None:
            subscription.household_id = household_id
        if plan_id is not None:
            subscription.plan_id = plan_id
        if start_date is not None:
            subscription.start_date = start_date
        if end_date is not None:
            subscription.end_date = end_date
        if is_active is not None:
            subscription.is_active = is_active
        subscription.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
        self.session.commit()
        return subscription

    def delete_subscription(self, subscription_id: int):
        subscription = self.get_subscription(subscription_id)
        if not subscription:
            raise ValueError("Subscription not found")
        self.session.delete(subscription)
        self.session.commit()

    # Owner-specific helpers (data isolation enforced by caller)
    def get_own_subscription(self, household_id: int) -> Optional[Subscription]:
        if not household_id:
            raise ValueError("Household ID is required")
        return self.get_active_subscription(household_id)

    def update_own_subscription(
        self, household_id: int, plan_id: int, start_date: datetime = None, end_date: datetime = None
    ) -> Subscription:
        subscription = self.get_active_subscription(household_id)
        if not subscription:
            raise ValueError("No active subscription to update")
        subscription.plan_id = plan_id
        if start_date is not None:
            subscription.start_date = start_date
        if end_date is not None:
            subscription.end_date = end_date
        subscription.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
        self.session.commit()
        return subscription

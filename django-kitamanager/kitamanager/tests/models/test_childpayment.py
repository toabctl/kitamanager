import pytest
from django.db.utils import IntegrityError

from kitamanager.models import ChildPaymentPlan, ChildPaymentTable, ChildPaymentTableEntry


@pytest.mark.django_db
def test_childpaymentplan_create():
    """
    Create a single ChildPaymentPlan
    """
    ChildPaymentPlan.objects.create(name="plan1")

    # 2nd one with different name should work
    ChildPaymentPlan.objects.create(name="plan2")

    # 2nd one with same name is not allowed
    with pytest.raises(IntegrityError):
        ChildPaymentPlan.objects.create(name="plan1")


@pytest.mark.django_db
def test_childpaymenttable_create():
    """
    Create ChildPaymentTable's
    """
    p1 = ChildPaymentPlan.objects.create(name="plan1")
    p2 = ChildPaymentPlan.objects.create(name="plan2", comment="a comment")

    ChildPaymentTable.objects.create(plan=p1, start="2020-01-01", end="2020-12-31")
    ChildPaymentTable.objects.create(plan=p1, start="2021-01-01", end="2021-12-31")

    # same tables, but for the other plan should work
    ChildPaymentTable.objects.create(plan=p2, start="2020-01-01", end="2020-12-31")
    ChildPaymentTable.objects.create(plan=p2, start="2021-01-01", end="2021-12-31")

    # overlapping date should not work
    with pytest.raises(IntegrityError):
        ChildPaymentTable.objects.create(plan=p2, start="2021-06-01", end="2023-12-31")


@pytest.mark.django_db
def test_childpaymenttableentry_create():
    """
    Create ChildPaymentTable's
    """
    p1 = ChildPaymentPlan.objects.create(name="plan1")
    p2 = ChildPaymentPlan.objects.create(name="plan2")

    t11 = ChildPaymentTable.objects.create(plan=p1, start="2020-01-01", end="2020-12-31")
    t12 = ChildPaymentTable.objects.create(plan=p1, start="2021-01-01", end="2021-12-31")

    # same tables, but for the other plan should work
    t21 = ChildPaymentTable.objects.create(plan=p2, start="2020-01-01", end="2020-12-31")
    t22 = ChildPaymentTable.objects.create(plan=p2, start="2021-01-01", end="2021-12-31")

    # same table/age/name should work in different tables
    ChildPaymentTableEntry.objects.create(table=t11, age=[0, 1], name="ganztag", pay=100, requirement=0.1)
    ChildPaymentTableEntry.objects.create(table=t12, age=[0, 1], name="ganztag", pay=100, requirement=0.1)
    ChildPaymentTableEntry.objects.create(table=t21, age=[0, 1], name="ganztag", pay=100, requirement=0.1)
    ChildPaymentTableEntry.objects.create(table=t22, age=[0, 1], name="ganztag", pay=100, requirement=0.1)

    # different age/name should work in the same table
    ChildPaymentTableEntry.objects.create(table=t11, age=[0, 1], name="ganztag_erweitert", pay=100, requirement=0.1)
    ChildPaymentTableEntry.objects.create(table=t11, age=[0, 2], name="ganztag", pay=100, requirement=0.1)

    # same table/age/name with different pay/requirement in the same table shouldn't work
    with pytest.raises(IntegrityError):
        ChildPaymentTableEntry.objects.create(table=t11, age=[0, 1], name="ganztag_erweitert", pay=200, requirement=0.2)

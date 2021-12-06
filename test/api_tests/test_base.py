import pytest

from calculator.models import Profile

@pytest.mark.django_db
def test_test():
	assert len(Profile.objects.all()) == 0

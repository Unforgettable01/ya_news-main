import pytest
from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (('news:home', None),
     ('users:login', None),
     ('users:logout', None),
     ('users:signup', None),
     ('news:detail', pytest.lazy_fixture('get_id_new')),
     )
)
def test_home_availability_for_anonymous_user(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:delete', pytest.lazy_fixture('get_id_comment')),
        ('news:edit', pytest.lazy_fixture('get_id_comment')),
    )
)
def test_redirects(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    excepted_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, excepted_url)


@pytest.mark.parametrize(
        'parametrized_client, status_code',
        (
            (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
            (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        )
)
@pytest.mark.parametrize(
        'name, args',
        (
            ('news:edit', pytest.lazy_fixture('get_id_comment')),
            ('news:delete', pytest.lazy_fixture('get_id_comment')),
        )
)
def test_author_can_edit_delete(author_client, name, args, parametrized_client, status_code):
    url = reverse(name, args=args)
    response = parametrized_client.get(url)
    assert response.status_code == status_code

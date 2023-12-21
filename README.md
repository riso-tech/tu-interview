This project using Django Cookiecutter

Read this setting to start project https://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html

### Filter

    `q` is search in first_name and last_name
    `status` filter `in` status split by `,`
    `company`, `department`, `position` filter by object id

    `page` pagination with page number

    `option` demotration response data based on request
    1 is full information
    other or null will return `contact_info` only

```shell

curl --location 'http://localhost:8000/api/test/user_filter/?q=a&status=1%2C2%2C3&company=1&department=1&position=1'

Postman test:
UserDB 80K
page_size 1K
response in 259ms
SQL: 5 queries


```

### File path

```python
    one/users/api/views.py  # API, rate limit
    one/users/api/serializers.py # User serializer remove fields, get FK data
    one/users/tests/test_drf_views.py # TestUserFilterViewSet
```

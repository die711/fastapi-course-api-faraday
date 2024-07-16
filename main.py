from fastapi import FastAPI
from api import users, courses

app = FastAPI(
    title='Fast API LMS',
    description='LMS for managing students and courses',
    version='0.0.1',
    contact={
        'name': 'Diego Resendiz Ojeda',
        'email': 'di_564@hotmail.com',
    },
    license_info={
        'name': 'Apache 2.0',
        'url': 'https://www.apache.org/licenses/LICENSE-2.0.html',
    }
)

app.include_router(users.router)
app.include_router(courses.router)


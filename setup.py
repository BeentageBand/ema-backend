from setuptools import setup, find_packages

setup(
    name='ema',
    version='1.0',
    author='beentageband',
    author_email='beentageband@gmail.com',
    description='RESTful Service for EMA (Event Manager Application)',
    url='https://github.com/BeentageBand/rest-demo',
    packages=find_packages(),
    install_requires=[
        'asgiref',
        'django',
        'djangorestframework',
        'pytz',
        'sqlparse'
    ],
    python_requires='>=3.6',
)

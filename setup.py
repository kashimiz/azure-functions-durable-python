from setuptools import setup


setup(
    name='azure-functions-durable-python',
    version='1.0.0b10',
    description='Durable Functions Support For Python Functionapp',
    license='MIT',
    packages=['azure.durable_functions',
              'azure.durable_functions.models'],
    extras_require={
        'dev': [
            'flake8==3.7.8',
            'pytest==5.0.1'
        ]
    },
    include_package_data=True,
    test_suite='tests'
)

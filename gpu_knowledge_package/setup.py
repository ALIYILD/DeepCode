from setuptools import setup, find_packages

setup(
    name='gpu-knowledge',
    version='1.0.0',
    description='GPU Expert Knowledge System for Multi-Agent AI Teams',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    package_data={
        'gpu_knowledge': ['*.pkl'],
    },
    install_requires=[
        # Add any dependencies here
    ],
    python_requires='>=3.8',
)

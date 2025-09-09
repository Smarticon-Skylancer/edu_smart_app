from setuptools import setup, find_packages

setup(
    name="cgpa_calculator_app",
    version="1.0.0",
    description="A Streamlit app for GPA/CGPA calculation with admin and user management",
    author="Ayuba Micheal",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "pandas",
        "bcrypt"
    ],
)

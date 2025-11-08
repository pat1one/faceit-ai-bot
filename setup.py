from setuptools import setup, find_packages

setup(
    name="faceit-ai-bot",
    version="0.1.0",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        line.strip()
        for line in open("requirements.txt")
        if line.strip() and not line.startswith("#")
    ],
    author="pat1one",
    author_email="your.email@example.com",
    description="AI-powered bot for FACEIT game analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pat1one/faceit-ai-bot",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
)
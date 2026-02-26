from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="instabot",
    version="1.0.0",
    author="Jatin",
    author_email="jatin@example.com",
    description="Instagram DM bot powered by Google Gemini AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/23f2001706/insta",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Communications :: Chat",
    ],
    python_requires=">=3.8",
    install_requires=[
        "flask>=2.3.0",
        "google-generativeai>=0.3.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "instabot=insta_bot.cli:cli",
        ],
    },
)

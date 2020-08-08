from setuptools import setup

setup(
    name="lolbot",
    version=open("version.txt").read(),
    description="A fun bot",
    url="https://lolbot.lmao.tf",
    author="S Stewart",
    python_requires=">=3.6",
    setup_requires=["wheel"],
)

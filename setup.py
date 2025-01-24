from setuptools import setup, find_packages

setup(
    name="Cloudits",
    package_dir={"": "src"},
    version="0.1.0",
    description="Your project description",
    use_incremental=True,
    packages=find_packages(),
    install_requires=[
        # Standard dependencies
        "incremental",
        # Incremental must be installed separately from requirements.txt
    ],
)


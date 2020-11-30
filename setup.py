from setuptools import setuptools

setuptools.setup(
    name="lotus-notes",
    version="1.0.47",
    packages = ["src"],
	license = 'MIT',
    author="Nipuna Weerapperuma, Spencer Bass, David Jaworski, Carlos Morales-Diaz, & Hannah Williams",
    description="Lotus - A hand-written notes application with scheduler.",
    url="https://github.com/nipunaw/Lotus/tree/design-prototype",
    install_requires=["opencv-python-headless", "PyQt5", "wsl", "wheel", "pytesseract"],
    include_package_data=True,
    entry_points = {
        'console_scripts': ['lotus = src.command_line:main'],
    },
    python_requires='>=3.7'
)

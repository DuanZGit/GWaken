from setuptools import setup, find_packages

setup(
    name="sleep-monitor",
    version="1.0.0",
    description="智能睡眠监测系统，适配红米手环2",
    author="Anomaly Detection Team",
    packages=find_packages(),
    install_requires=[
        "Flask==2.3.3",
        "PyBluez==0.23",
        "requests==2.31.0",
    ],
    entry_points={
        'console_scripts': [
            'sleep-monitor=sleep_monitor.main:main',
            'sleep-monitor-api=sleep_monitor.run_api:main',
        ],
    },
    python_requires='>=3.6',
)
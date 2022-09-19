from setuptools import setup

setup(
    name = 'json_diff',
    version = '0.0.1',
    packages = ['json_diff', 'json_diff.cli_tool'],
    entry_points = {
        'console_scripts': [
            'json_diff = json_diff.cli_tool.diff:main',
            'json_patch = json_diff.cli_tool.patch:main',
        ]
    }
)

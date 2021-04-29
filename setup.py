from setuptools import setup, find_packages

setup(
    name='vyos-config-deploy-tool',
    version='0.1.0',
    packages=find_packages(),
    python_requires='>=3.8,<4',
    install_requires=[
        'click~=7.1',
        'pexpect~=4.8',
    ],
    entry_points={
        'console_scripts': [
            'vyos-config-deploy-tool=vyos_config_deploy_tool.cli:main',
        ],
    }
)

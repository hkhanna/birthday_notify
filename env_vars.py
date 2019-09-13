# Utilities for management of environment variables
import os
import logging

log = logging.getLogger(__name__)

def load_file(filename='.env'):
    """Loads environment variables from .env file if not set in the environment"""
    if not os.path.isfile(filename):
        log.warning(f'Environment file {filename} not found')
        return

    with open(filename) as f:
        for line in f:
            if line.startswith('#'):
                continue
            key, value = line.strip().split('=', 1)
            key = key.strip()
            value = value.strip()

            os.environ.setdefault(key, value)

def get_required(required_vars):
    """Confirm that the passed environment vars exist and return the values"""
    var_values = []
    missing_vars = []
    for var_name in required_vars:
        try:
            var_values.append(os.environ[var_name])
        except KeyError:
            missing_vars.append(var_name)

    if len(missing_vars) != 0:
        missing_vars = ', '.join(missing_vars)
        log.error(f"Missing environment variables: {missing_vars}")
        exit(1)

    return var_values
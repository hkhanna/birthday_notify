# Utilities for management of environment variables
import os
import logging

log = logging.getLogger(__name__)


def load_file(filename=".env"):
    """Loads environment variables from .env file if not set in the environment"""
    if not os.path.isfile(filename):
        log.warning("Environment file {} not found".format(filename))
        return

    with open(filename) as f:
        for line in f:
            if line.startswith("#"):
                continue
            key, value = line.strip().split("=", 1)
            key = key.strip()
            value = value.strip()

            if len(value) != 0:
                os.environ.setdefault(key, value)


def get_required(required_vars):
    """Confirm that the passed environment vars exist and return the values"""
    var_values = []
    missing_vars = []
    for var_name in required_vars:
        try:
            var_value = os.environ[var_name]

            # If the environment variable is set but blank, consider it missing.
            if len(var_value) != 0:
                var_values.append(var_value)
            else:
                missing_vars.append(var_name)
        except KeyError:
            missing_vars.append(var_name)

    if len(missing_vars) != 0:
        missing_vars = ", ".join(missing_vars)
        log.error("Missing environment variables: {}".format(missing_vars))
        exit(1)

    return var_values

#!/usr/bin/env python3
#
# Provides a connection to the mutation database.
#
import sqlite3

import base


def connect():
    """
    Connects to the database and returns the new :class:`Connection` object.
    """
    return Connection()


class Connection(object):
    """
    Context manager that maintains a connection to an sqlite database
    containing the mutation data from the ``csv`` files.
    """
    def __init__(self):
        super(Connection, self).__init__()
        self._connection = None

    def __enter__(self):
        """
        Called when the context manager is entered. Opens a connection to a new
        or cached sqlite database containing the data from the ``csv`` files.
        """
        # Test if connection is already set up
        if self._connection:
            try:
                self._connection.close()
            except Exception:
                pass
            raise Exception('Connection already open when entering!')

        # Set up connection
        self._connection = sqlite3.connect(base.PATH_DB)

        # Enable foreign keys
        c = self._connection.cursor()
        c.execute('PRAGMA foreign_keys = ON;')
        self._connection.commit()

        # Set row factory (to enable name based access)
        self._connection.row_factory = sqlite3.Row

        return self._connection

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Called when the context manager is exited. Closes the connection.
        """
        if self._connection:
            self._connection.close()
            self._connection = None


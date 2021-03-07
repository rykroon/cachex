from redis import ConnectionPool, Redis 


connection_pool = None


def connect(*args, **kwargs):
    """
        Create a new Connection Pool
    """
    global connection_pool
    connection_pool = ConnectionPool(*args, **kwargs)
    return connection_pool


def get_client():
    """
        Get a connection from the connection pool
    """
    return Redis(connection_pool=connection_pool)
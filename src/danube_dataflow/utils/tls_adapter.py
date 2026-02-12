import ssl
import requests

from requests.adapters import HTTPAdapter


class TLSAdapter(HTTPAdapter):
    """
    A custom HTTPAdapter that allows specifying a custom TLS cipher security level.

    This is useful for connecting to older servers that require non-default TLS
    configurations, while still using a standard requests.Session interface.

    Attributes:
        security_level (str): The OpenSSL cipher/security level to use.
    """

    def __init__(self, security_level: str, *args, **kwargs):
        """
        Initialize the TLSAdapter with a specific TLS security level.

        Args:
            security_level (str): The OpenSSL cipher/security level to be used.
            *args: Positional arguments forwarded to the HTTPAdapter.
            **kwargs: Keyword arguments forwarded to the HTTPAdapter.
        """
        self.security_level = security_level
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        """
        Initialize the PoolManager with a custom SSL context using the specified security level.
        """
        ctx = ssl.create_default_context()
        ctx.set_ciphers(self.security_level)
        pool_kwargs["ssl_context"] = ctx
        return super().init_poolmanager(*pool_args, **pool_kwargs)


def create_tls_session(security_level: str) -> requests.Session:
    """
    Create and return a requests.Session configured with a custom TLS security level.

    This session lowers or raises the default OpenSSL security level for compatibility with the server.

    Args:
        security_level: The required level of security that the TLSAdapter must use.

    Returns:
        requests.Session: A session object using a custom TLS adapter.
    """
    session = requests.Session()
    session.mount("https://", TLSAdapter(security_level))

    return session

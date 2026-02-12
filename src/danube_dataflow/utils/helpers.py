from bs4 import Tag
from requests.sessions import Session

from .tls_adapter import create_tls_session


def receive_custom_session() -> Session:
    """
    Receive the custom session with the specified custom TLS security level.

    Returns:
        requests.Session: A session object using a custom TLS adapter.
    """
    return create_tls_session("DEFAULT@SECLEVEL=1")


def find_required_element(element: Tag, tag: str | list[str], **kwargs) -> Tag:
    """
    Find a single required child element within a BeautifulSoup Tag.

    Args:
        element:
            The BeautifulSoup tag on which the search is performed.
        tag:
            The name of the tag or list of tags to search for.
        **kwargs:
            Additional keyword arguments forwarded to BeautifulSoup's 'find' method.

    Returns:
        The matching BeautifulSoup Tag.

    Raises:
        ValueError:
            If no matching element is found.
    """
    result = element.find(tag, **kwargs)

    if not result:
        raise ValueError(
            f"Could not find element {tag} in {element.name} with attributes {kwargs}"
        )

    return result


def find_required_elements(element: Tag, tag: str | list[str], **kwargs) -> list[Tag]:
    """
    Find multiple required child elements within a BeautifulSoup Tag.

    Args:
        element: The BeautifulSoup tag on which the search is performed.
        tag: The name of the tag or list of tags to search for.
        **kwargs: Additional keyword arguments forwarded to BeautifulSoup's 'find_all" method.

    Returns:
        The matching BeautifulSoup Tag.

    Raises:
        ValueError: If no matching element is found.
    """
    results = element.find_all(tag, **kwargs)

    if results is None:
        raise ValueError(
            f"Could not find elements {tag} in {element.name} with attributes {kwargs}"
        )

    return results

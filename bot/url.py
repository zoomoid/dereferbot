from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

common_query_params = [
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_content",
    "utm_term",
]

known_query_params = {
    "spotify.com": ["si", "context", "pt"],
    "twitter.com": ["s", "t"]
}

def root_hostname(hostname: str) -> str:
    """
    root_hostname returns the root hostname of an arbitrary domain name

    :return: a string that is the root DNS name of an arbitrary hostname.

    .. deprecated:: 1.7.0
       The object-oriented interface offers more customizability over how to sanitize different types of hosts
    """
    return ".".join(hostname.split(".")[-2:])

def clean_url(url: str) -> str:
    """
    Removes known query parameters from a given url as a string

    :return: a cleaned url as a proper url-encoded string.

    .. deprecated:: 1.7.0
       The object-oriented interface offers more customizability over how to sanitize different types of hosts
    """
    p = urlparse(url)
    if p.hostname == None:
        return url

    key = root_hostname(p.hostname)

    query_params_for_hostname = common_query_params

    if key in known_query_params:
        query_params_for_hostname += known_query_params[key]

    qsl = parse_qsl(p.query)

    # filter query strings
    new_qs = [(key, value) for (key, value) in qsl if key not in query_params_for_hostname]
    new_qs = urlencode(new_qs)
    new_url = p._replace(query=new_qs)
    new_url = urlunparse(new_url)
    return new_url

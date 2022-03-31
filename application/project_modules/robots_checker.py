from requests_cache import CachedSession
from urllib.parse import urlparse


def get_url_name(url):
    """
    Gets the name of a website, without any paths.
    :param url: url
    :return: a string
    """
    name = urlparse(url).netloc
    return name


def get_robots_txt(website):
    """
    Gets the robots.txt file from a website as a string
    :param website: url
    :return: a string
    """
    protocol = "https://"
    robots_path = "/robots.txt"
    # -- Add In Missing HTTPS -- #
    if "://" not in website:
        website = protocol + website
    # -- Remove The Path -- #
    if website.count('/') > 2:
        website = website[:website.rfind("/")+1]
    session = CachedSession()
    robot_text = session.get(website + robots_path).text

    return robot_text


def create_robots_html(website):
    """
    Converts the website's robot.txt string into an HTML with CSS classes.
    :param website: url
    :return: html string
    """
    robot_text = get_robots_txt(website)
    robots_html = ''
    for line in robot_text.splitlines():

        if line.startswith('#') or line.startswith("Sitemap"):
            new_line = "<div class='smaller text-muted'>" + line + "</div><br>"
            robots_html += new_line

        if line.startswith('User'):
            new_line = "<div class='fs-6'>" + line + "</div>"
            robots_html += new_line

        if line.startswith('Disallow'):
            new_line = "<p class='disallow'><span class='badge bg-danger'>" + line.split(":")[0] + "</span>" \
                       + ":" + line.split(":")[1] + "</p>"
            robots_html += new_line

        if line.startswith('Allow'):
            new_line = "<p class='allow'><span class='badge bg-success'>" + line.split(":")[0] + "</span>" \
                       + ":" + line.split(":")[1] + "</p>"
            robots_html += new_line

    return robots_html

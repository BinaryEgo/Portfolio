from requests_cache import CachedSession
from urllib.parse import urlparse


def get_url_name(url):
    name = urlparse(url).netloc
    return name


def get_robots_txt(website):
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

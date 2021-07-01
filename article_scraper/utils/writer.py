import os
import errno

from article_scraper.constants import APP_DIR


def write_review(text, filename):
    filename = APP_DIR + "/reviews/" + filename
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    if os.path.exists(filename):
        choice = "a"
    else:
        choice = "w"
    with open(filename, choice) as f:
        f.write(text)

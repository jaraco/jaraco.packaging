import os

from six.moves import urllib

from jaraco.packaging import cheese


def test_revived_distribution():
    base = 'https://pypi.python.org/packages/source/'
    nose_timer_path = 'n/nose-timer/nose-timer-0.3.0.tar.gz'
    url = urllib.parse.urljoin(base, nose_timer_path)
    cheese.RevivedDistribution(url)
    os.remove('nose-timer-0.3.0.tar.gz')

import unittest

from urllib.parse import urlparse, urlunparse
from bot.spotify_cleaner import hook_spotify_link


class TestSpotifyLinkHook(unittest.TestCase):
    def test_sanity(self):
        url = "https://spotify.link/L1Sb5i2ruDb" # Pendulum - Tarantula
        ps = urlparse(url)
        res, _ = hook_spotify_link(ps)
        self.assertEqual(res, "https://open.spotify.com/track/7ifq3etzDP60X1IRaFVngl?si=&context=spotify%3Aplaylist%3A0cHYJorAnBeis7dDP1dxao")
        pass


if __name__ == "__main__":
    unittest.main()

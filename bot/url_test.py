import unittest

from bot.url import clean_url, root_hostname


class TestRootHostname(unittest.TestCase):
    def test_exact_match(self):
        self.assertEqual(root_hostname("spotify.com"), "spotify.com")
        self.assertEqual(root_hostname("twitter.com"), "twitter.com")
        self.assertEqual(root_hostname("zoomoid.dev"), "zoomoid.dev")
        pass

    def test_wildcard_match(self):
        self.assertEqual(root_hostname("*.spotify.com"), "spotify.com")
        self.assertEqual(root_hostname("*.twitter.com"), "twitter.com")
        pass

    def test_subdomain_match(self):
        self.assertEqual(root_hostname("open.spotify.com"), "spotify.com")
        self.assertEqual(root_hostname("share.twitter.com"), "twitter.com")
        self.assertEqual(root_hostname("xyz.zoomoid.dev"), "zoomoid.dev")
        self.assertEqual(root_hostname("abc.xyz.zoomoid.dev"), "zoomoid.dev")

    def test_empty_hostname(self):
        self.assertEqual(root_hostname(""), "")


class TestCleanUrl(unittest.TestCase):
    def test_spotify_link(self):
        cleaned = clean_url(
            "https://open.spotify.com/socialsession/mKpwIGQwex54E4FyGOe1EfUHQ0I77ZtXSmEnkUCb4ewPsmL7RAGxrFIPIsREOzZfE5m8Je9Iuxymee9rQgKva7XKrUlguiQVhjGqs98u8YH?si=kyrVCdkPTzmt70l5_EFG3A&utm_source=copy-link"
        )
        self.assertNotIn("si=", cleaned)
        self.assertNotIn("utm_", cleaned)

        cleaned = clean_url(
            "https://open.spotify.com/playlist/5bgzPP7BCRCVBqq5xeCwGh?si=Tm1-G7EVRAe5WoXEkPhoxw&pt=eeef5ed3806aa865738065d8f4e567ce"
        )
        self.assertNotIn("si=", cleaned)
        self.assertNotIn("pt=", cleaned)

        self.assertNotIn(
            "si=",
            clean_url(
                "https://open.spotify.com/track/5pNa5eBYoAQcYh35SDYkGI?si=774c625761924a77"
            ),
        )

        self.assertNotIn(
            "si=",
            clean_url(
                "https://open.spotify.com/track/39IkdI5kRWyM5DjyBh4Khp?si=3r9gGryaT7SKJvQRZ-Yk4Q"
            ),
        )
        self.assertEqual(
            "https://open.spotify.com/track/39IkdI5kRWyM5DjyBh4Khp",
            clean_url("https://open.spotify.com/track/39IkdI5kRWyM5DjyBh4Khp"),
        )

    def test_twitter_link(self):
        self.assertEqual(
            "https://twitter.com/noway4u_sir/status/1581387356560855040",
            clean_url(
                "https://twitter.com/noway4u_sir/status/1581387356560855040?s=20&t=royf7igr_Ul3JU8WO5yfBA"
            ),
        )
        self.assertEqual(
            "https://twitter.com/noway4u_sir/status/1581387356560855040",
            clean_url(
                "https://twitter.com/noway4u_sir/status/1581387356560855040?s=20"
            ),
        )
        self.assertEqual(
            "https://twitter.com/noway4u_sir/status/1581387356560855040",
            clean_url("https://twitter.com/noway4u_sir/status/1581387356560855040"),
        )

    def test_generic_link(self):
        self.assertNotIn(
            "utm_source=",
            clean_url(
                "https://www.instagram.com/reel/Cja5fOFpeb2/?utm_source=ig_web_copy_link"
            ),
        )

    def test_empty_link(self):
        self.assertEqual(
            "https://open.spotify.com/track/5pNa5eBYoAQcYh35SDYkGI",
            clean_url("https://open.spotify.com/track/5pNa5eBYoAQcYh35SDYkGI"),
        )
        self.assertEqual(
            "https://open.spotify.com/track",
            clean_url("https://open.spotify.com/track"),
        )
        self.assertEqual("https://zoomoid.dev", clean_url("https://zoomoid.dev"))

    def test_invalid_link(self):
        self.assertEqual("fsffps:/ierfhnsf.cr", clean_url("fsffps:/ierfhnsf.cr"))


if __name__ == "__main__":
    unittest.main()

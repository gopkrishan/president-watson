import configparser
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights


class Politician:
    """
    Uses data sourced from a Twitter feed to find out the person's personality
    traits.
    """
    def __init__(self, handle):
        self.twitter_handle = handle

        names = configparser.ConfigParser()
        names.read('app/static/config/twitter_handles.ini')
        self.name = names['Twitter Handles'][self.twitter_handle]

        self.set_api_keys()
        self.receive_twitter_data()
        self.set_profile_picture()
        self.analyze_tweets()
        self.flatten_data()
        self.set_personality_values()

    def set_api_keys(self):
        """
        Receives the api keys from the text file. Will be replaced by
        configparser in the future.
        """
        keys = configparser.ConfigParser()
        keys.read('app/static/config/api_keys.ini')

        self.twitter_consumer_key = keys['Twitter']['consumer_keys']
        self.twitter_consumer_secret = keys['Twitter']['consumer_secret']
        self.twitter_access_token = keys['Twitter']['access_token']
        self.twitter_access_secret = keys['Twitter']['access_secret']

        self.pi_username = keys['Watson']['username']
        self.pi_password = keys['Watson']['password']

    def receive_twitter_data(self):
        """
        Uses the Twitter keys assigned in set_api_keys() to receive the latest
        200 tweets from the Twitter feed.
        """
        twitter_api = twitter.Api(
                                 consumer_key=self.twitter_consumer_key,
                                 consumer_secret=self.twitter_consumer_secret,
                                 access_token_key=self.twitter_access_token,
                                 access_token_secret=self.twitter_access_secret
                                 )
        self.statuses = twitter_api.GetUserTimeline(
                                              screen_name=self.twitter_handle,
                                              count=200,
                                              include_rts=False
                                              )

    def set_profile_picture(self):
        """
        Uses the latest tweet to get the profile picture from the user.
        """
        img = self.statuses[0].user.profile_image_url
        self.profile_pic = img.replace("_normal", "")

    def analyze_tweets(self):
        """
        Uploads the string of tweets to the Personality Insights AI of Watson
        to receive the values of the personality traits.
        """
        personality_insights = PersonalityInsights(
                                                  username=self.pi_username,
                                                  password=self.pi_password
                                                  )

        twitter_messages = ""
        for status in self.statuses:
            if (status.lang == 'en'):
                twitter_messages += str(status.text.encode('utf-8')) + " "

        self.pi_result = personality_insights.profile(twitter_messages)

    def flatten_data(self):
        """
        Makes the data sourced from the Personality Insights AI easier to read.

        (Sourced from Codeacademy)
        """
        data = {}
        for a in self.pi_result['tree']['children']:
            if 'children' in a:
                for b in a['children']:
                    if 'children' in b:
                        for c in b['children']:
                            if 'children' in c:
                                for d in c['children']:
                                    if (d['category'] == 'personality'):
                                        data[d['id']] = d['percentage']
                                        if 'children' not in c:
                                            if c['category'] == 'personality':
                                                data[c['id']] = c['percentage']
        self.flattened_data = data

    def set_personality_values(self):
        """
        Makes the values of the personality traits available for other modules
        to easily use.
        """
        self.cheerfulness = self.flattened_data["Cheerfulness"]
        self.trust = self.flattened_data["Trust"]
        self.cautiousness = self.flattened_data["Cautiousness"]
        self.orderliness = self.flattened_data["Orderliness"]
        self.liberalism = self.flattened_data["Liberalism"]
        self.anxiety = self.flattened_data["Anxiety"]
        self.achievement = self.flattened_data["Achievement striving"]
        self.altruism = self.flattened_data["Altruism"]
        self.vulnerability = self.flattened_data["Vulnerability"]
        self.discipline = self.flattened_data["Self-discipline"]
        self.consciousness = self.flattened_data["Self-consciousness"]
        self.assertiveness = self.flattened_data["Assertiveness"]
        self.friendliness = self.flattened_data["Friendliness"]
        self.immoderation = self.flattened_data["Immoderation"]
        self.depression = self.flattened_data["Depression"]
        self.emotionality = self.flattened_data["Emotionality"]
        self.morality = self.flattened_data["Morality"]
        self.cooperation = self.flattened_data["Cooperation"]
        self.anger = self.flattened_data["Anger"]
        self.duitifulness = self.flattened_data["Dutifulness"]
        self.excitement = self.flattened_data["Excitement-seeking"]
        self.artistic = self.flattened_data["Artistic interests"]
        self.gregariousness = self.flattened_data["Gregariousness"]
        self.imagination = self.flattened_data["Imagination"]
        self.adventurousness = self.flattened_data["Adventurousness"]
        self.sympathy = self.flattened_data["Sympathy"]
        self.activity = self.flattened_data["Activity level"]
        self.modesty = self.flattened_data["Modesty"]
        self.efficacy = self.flattened_data["Self-efficacy"]
        self.intellect = self.flattened_data["Intellect"]

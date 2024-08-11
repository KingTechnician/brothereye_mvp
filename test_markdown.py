import markdown


markdown_information = """
To conduct an investigation into the recent developments of MrBeast, I will analyze the provided sources and focus on Twitter threads and subreddits.

### Key Points and Findings

1. **MrBeast's Statement on Ava Kris Tyson**:
   - MrBeast (Jimmy Donaldson) expressed his dismay and disapproval of Ava Kris Tyson's alleged online conduct, stating that he was "appalled and against such unacceptable behaviors" on the social media platform X (formerly Twitter).
   - He mentioned that he had taken immediate action to remove Ava from his company and channel.

2. **Ava Kris Tyson's Allegations**:
   - Tyson was accused of engaging in inappropriate online interactions with an individual identified as LavaGS, who was 13 years old at the time, and sharing explicit content.
   - Tyson denied the allegations and apologized for any past actions that may have hurt or offended anyone, announcing her departure from MrBeast's channel.

3. **Reddit User "Dawson"'s Claims**:
   - Dawson, a self-proclaimed former employee of MrBeast, alleged that MrBeast was aware of the situation beforehand and that Ava Kris Tyson posed a significant liability.

4. **MrBeast's Monetization on Twitter**:
   - Elon Musk asked MrBeast to post videos on Twitter, but MrBeast initially refused due to Twitter's poor monetization.
   - Elon Musk allegedly "fixed" the issue, leading to a new monetization experience, which some users found suspicious and potentially illegal.

5. **MrBeast's Video on Twitter**:
   - MrBeast posted a video on Twitter, which was seen by many users repeatedly, leading to speculation about the platform's algorithm and potential manipulation.

### Sources

1. https://twitter.com/MrBeast/status/1816299504674464113
2. https://www.reddit.com/r/Twitter/comments/19akce3/mr_beasts_video_tweet_plaguing_the_for_you_page/
3. https://twitter.com/mrbeast_update
4. https://twitter.com/mrbeast
5. https://www.newsweek.com/mrbeast-ava-kris-tyson-reddit-youtube-video-1930271
"""

html_version = markdown.markdown(markdown_information)

print(html_version)
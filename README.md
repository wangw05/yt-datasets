# Generating datasets from Youtube
## Overview
This tool collects video information such as the number of views and video tags by utilizing the [Youtube Data API v3](https://developers.google.com/youtube/v3/). Running this script on a Youtube channel will generate a csv dataset with the listed information below. An example of a dataset created using this tool can be found [here](https://github.com/wangw05/bwb-yt-dataset).
## Usage
Run ```pip3 install -r requirements.txt```

Create document named ```config.py``` within folder. Enable Youtube Data API v3 [within the Google Cloud dashboard](https://console.cloud.google.com/apis/library) and place requested API within ```config.py``` using format ```API_KEY={YOUR_API_KEY_HERE}```.

Within ```main.py```, change ```CHANNEL_ID={YOUTUBE_CHANNEL_ID}``` to the channel that you would like to generate the dataset for. For example: ```CHANNEL_ID=UCJHA_jMfCvEnv-3kRjTCQXw``` corresponds to the channel [Binging with Babish](https://www.youtube.com/channel/UCJHA_jMfCvEnv-3kRjTCQXw).

Run ```main.py``` - Program will pause when it calculates that you have less than 300 units out of the daily quota of 10,000 units. Press enter when quota resets for the day to resume the program.

Dataset will be saved as ```data_file.csv``` in project folder.

## Data Collected from Youtube
| Column Name   | Definition                                                   |
|---------------|--------------------------------------------------------------|
| etag       | [HTTP ETag](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/ETag), an unique identifier for a resource.                    |
| videoid       | id of video uploaded, unique to each video                   |
| channelid     | id of channel uploader, unique to each channel               |
| publishedtime | publish time of video, in the format of YYYY-MM-DDThh:mm:ssZ |
| title         | title of the video                                           |
| desc          | description of the video                                     |
| live          | whether the video is an upcoming livestream, ongoing livestream, or neither                           |
| viewcount     | viewcount of the video at time of request                    |
| likecount     | likecount of the video at time of request, -1 indicates no data found                    |
| dislikecount  | dislikecount of the video at time of request, -1 indicates no data found                 |
| comments      | list of all main-level comments on video, saved in utf8      |
| commentcount  | count of all main-level comments                             |
| tags          | list of tags added by video uploader for video                       |

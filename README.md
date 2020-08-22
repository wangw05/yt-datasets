# Generating datasets from Youtube
## Overview
This tool was built to support a project focusing on analyzing individual youtubers over time based on their content. This project focuses on the data collection process to prepare a dataset for analysis.
## Usage
Create document named config.py within folder. Enable [Youtube Data API v3](https://console.cloud.google.com/apis/library) and place requested API within config.py using format API_KEY={YOUR_API_KEY}.

Within main.py, change CHANNEL_ID to the channel that you would like to generate the dataset for.

Run main.py - Program will stop when it detects that you are within 300 units of the daily limit (10,000 units). Press enter when quota resets for the day to resume the program.

Dataset will be saved as data_file.csv

## Data Collected from Youtube
| Column Name   | Definition                                                   |
|---------------|--------------------------------------------------------------|
| videoid       | id of video uploaded, unique to each video                   |
| channelid     | id of channel uploader, unique to each channel               |
| publishedtime | publish time of video, in the format of YYYY-MM-DDThh:mm:ssZ |
| title         | title of the video                                           |
| desc          | description of the video                                     |
| live          | whether the video was a live video                           |
| viewcount     | viewcount of the video at time of request                    |
| likecount     | likecount of the video at time of request                    |
| dislikecount  | dislikecount of the video at time of request                 |
| favoritecount | favoritecount of the video at time of request                |
| comments      | list of all main-level comments on video, saved in utf8      |
| commentcount  | count of all main-level comments                             |
| tags          | tags added by video uploader for video                       |

import json
import requests
import csv
import config
import sys

API_KEY = config.API_KEY

CHANNEL_ID = "UCJHA_jMfCvEnv-3kRjTCQXw"


def main():
    video_entries = []
    units_remain = 10000
    # get videos
    units_remain, video_entries = get_videos(units_remain, video_entries)

    # get indv details
    units_remain, video_entries = get_details(units_remain, video_entries)

    # save to csv
    save_csv(video_entries)


def get_videos(units_remain, video_entries):
    """
    Query Youtube Data API v3 to obtain search results matching in CHANNEL_ID,
    request returns only video information and excludes playlists and channels.

    Function will pause when it calculates that available quota is under 300.

    Function catches KeyError when processing request,
    will save current data before exit.

    Requires current units, data structure for storage.
    Returns remaining units, processed list of videos.
    """

    # setup env variables
    PAGE_ID = ""
    LAST_PAGE = False
    num_results = 50
    page_count = 0

    # run while last page is false
    while(LAST_PAGE is False):
        # check remaining units
        if units_remain < 300:
            input("Remaining units less than 300.\n Press Enter to continue when quota refreshes.")
            units_remain = 10000

        # setup url
        URL = (f'https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNEL_ID}&pageToken={PAGE_ID}&part=snippet,id&order=date&maxResults={num_results}&type=video')

        # get page results
        page = requests.get(URL)
        results = json.loads(page.text)
        units_remain -= 100

        # check if json is valid, causes KeyError if not caught
        try:
            videos = results['items']
        except KeyError:
            print("--Error encountered while processing search result response.\n--Printing last retrieved json...")
            print(f"URL: {URL}")
            print(results)
            print("--Exiting program...")
            sys.exit(1)

        # save videos into list
        for video in videos:
            entry = {
                'etag': video['etag'],
                'videoid': video['id']['videoId'],
                'channelid': video['snippet']['channelId'],
                'publishedtime': video['snippet']['publishTime']
            }
            video_entries.append(entry)

        # handle multipage requests
        page_count += 1

        if "nextPageToken" in results:
            print(f"Search results page {page_count} processed.")
            PAGE_ID = results['nextPageToken']
        else:
            # set last page to true
            LAST_PAGE = True
            print(f"All search results processed. {len(video_entries)} videos found.")
            print(f"Units remaining: {units_remain}")

    return units_remain, video_entries


def get_details(units_remain, video_entries):
    """
    Takes processed list of videos and queries corresponding video details.

    Function will pause when it calculates that available quota is under 300.

    Function catches KeyError when processing request,
    will save current data before exit.

    Requires current units, processed list of videos.
    Returns remaining units, processed list of videos.
    """

    video_count = 0
    total_videos = len(video_entries)

    print("Processing video details...")

    for video in video_entries:
        # check remaining units
        if units_remain < 300:
            input("--Remaining units less than 300.\n--Press Enter to continue when quota refreshes.")
            units_remain = 10000

        video_id = video['videoid']
        URL = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={API_KEY}"

        # get page results
        page = requests.get(URL)
        results = json.loads(page.text)
        units_remain -= 1

        # check if json is valid, causes KeyError if not caught
        try:
            details = results['items'][0]
        except KeyError:
            print("--Error encountered while processing video detail response.\n--Printing last retrieved json...")
            print(f"URL: {URL}")
            print(results)
            print("--Saving retrieved data to csv...")
            save_csv(video_entries)
            print("--Data save complete. Exiting program...")
            sys.exit(1)

        # process video details
        video["title"] = details['snippet']['title']
        video["desc"] = details['snippet']['description']
        video["live"] = details['snippet']['liveBroadcastContent']
        video["viewcount"] = details['statistics']['viewCount']
        # video like/dislike count may be hidden, causes KeyError if not caught
        try:
            video["likecount"] = details['statistics']['likeCount']
            video["dislikecount"] = details['statistics']['dislikeCount']
        except KeyError:
            video["likecount"] = -1
            video["dislikecount"] = -1
            print(f"{video_id} did not have any like/dislike information found.")
        units_remain, video["comments"], video["commentcount"], status =\
            get_comments(units_remain, video_id)
        # tags may be empty, causes KeyError if not caught
        try:
            video["tags"] = details['snippet']['tags']
        except KeyError:
            video["tags"] = []
            print(f"{video_id} did not have any tags.")

        # sanity check to see program is running
        print(f"{video_id} processed. {units_remain} units remaining.")
        video_count += 1
        if video_count % 20 == 0:
            print(f"Details retreived from {video_count} videos. {total_videos - video_count} remaining.")

        # comment processing errored, saving data and exiting
        if status is False:
            print("--Saving retrieved data to csv...")
            save_csv(video_entries)
            print("--Data save complete. Exiting program...")
            sys.exit(1)

    print(f"Process complete. {len(video_entries)} videos processed.")

    return units_remain, video_entries


def get_comments(units_remain, video_ID):
    """
    Based on videoID, query and save comments from a video.

    Requires current units, videoID.
    Returns remaining units, processed list of comments.
    """

    # setup env variables
    PAGE_ID = ""
    LAST_PAGE = False
    num_results = 100
    all_comments = []
    status = True

    # run while last page is false
    while(LAST_PAGE is False):
        # setup url
        URL = (f'https://www.googleapis.com/youtube/v3/commentThreads?key={API_KEY}&videoId={video_ID}&pageToken={PAGE_ID}&maxResults={num_results}&part=snippet')

        # get page results
        page = requests.get(URL)
        results = json.loads(page.text)
        units_remain -= 1

        # check if json is valid, causes KeyError if not caught
        try:
            "items" in results
        except KeyError:
            status = False
            print("--Error encountered while processing comment response.\n--Printing last retrieved json...")
            print(f"URL: {URL}")
            print(results)
            return units_remain, all_comments, len(all_comments), status

        # save comments into list
        for comment in results['items']:
            toplevel = comment['snippet']['topLevelComment']
            original = toplevel['snippet']['textOriginal']
            all_comments.append(original)

        # handle multipage requests
        if "nextPageToken" in results:
            PAGE_ID = results['nextPageToken']
        else:
            # set last page to true
            LAST_PAGE = True

    return units_remain, all_comments, len(all_comments), status


def save_csv(data_dump):
    """
    Save processed data to a csv in main directory.

    Requires processed video information.
    """

    data_file = open('data_file.csv', 'w', newline='', encoding='utf8')
    csv_writer = csv.writer(data_file)

    first = True

    for video in data_dump:
        if first is True:
            # Writing headers of CSV file
            header = video.keys()
            csv_writer.writerow(header)
            first = False

        # Writing data of CSV file
        csv_writer.writerow(video.values())

    print("Data write complete.")
    data_file.close()


if __name__ == "__main__":
    main()

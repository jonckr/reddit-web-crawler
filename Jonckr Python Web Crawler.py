import csv
import datetime
import praw
import pandas as pd
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     username='',
                     password='',
                     user_agent='Python Web Crawler')

#######################################################################################################################
#Reddit Crawler#
list_counter = 0
sr_list = ['dota2','AdmiralBulldog']
data = []
comments = []
while list_counter < len(sr_list):
    subreddit = reddit.subreddit(sr_list[list_counter]).new(limit=2) #Change limit for number of threads, .new/.hot
    for s in subreddit:  # for every submission in the subreddit
        # fetch top level comments
        for c in s.comments:
            c_time = datetime.datetime.fromtimestamp(c.created_utc) #Convert format of comment time (Y:M:D , H:M:S)
            comments.append([c.subreddit, c._submission, 'Comment', s.title, c.author, c_time, c.score, c.body])
                #May not need c._submission
        s_time = datetime.datetime.fromtimestamp(s.created_utc) #Convert format of threadRE time
        data.append([s.subreddit, s.id,'Thread', s.title, s.author, s_time, s.score, s.selftext])
    list_counter+= 1

#Export to CSV#
df = pd.DataFrame(data, columns=['Subreddit Name','Thread ID', 'Thread/Comment', 'Thread Title', 'Author',
                                 'Timestamp','Score','Content'])
df1 = pd.DataFrame(comments, columns=['Subreddit Name','Thread ID','Thread/Comment', 'Thread Title', 'Author',
                                 'Timestamp','Score','Content'])
result = pd.concat([df, df1])
result.to_csv('Raw Data.csv', index=False)

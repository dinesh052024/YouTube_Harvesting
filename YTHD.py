#pip install google-api-python-client
#pip install mysql-connector-python
# import following packages
import streamlit as st
import googleapiclient.discovery
import mysql.connector
import pandas as pd
from mysql.connector import Error
from mysql.connector import errorcode

#variable declared to get the youtube data
api_service_name = "youtube"
api_version = "v3"
API_key="AIzaSyCh0EKbFBtRzkwvfLks-h_b0AWbti-BzwM"
#channel_id="UCRTmSft-1I9f0yzTnz32oMg"
#YouTube_Harves("UCRTmSft-1I9f0yzTnz32oMg")


#DB connection
mydb = mysql.connector.connect(
  host="localhost",
  user="dinesh",
  password="dinesh@1234"
)
mycursor = mydb.cursor()

#Function to get the Channel,Video and comment details
def YouTube_Harves(channel_id):
 #Get data for channel details from youtube API
 youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=API_key)
 Channel_request = youtube.channels().list(
         part="snippet,contentDetails,statistics",
         id=channel_id
     )
 Channel_response = Channel_request.execute()
 # print(response)
 channel_name=Channel_response['items'][0]['snippet']['title']
 channel_uploads=Channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
 channel_sub_cnt=Channel_response['items'][0]['statistics']['subscriberCount'] 
 channel_view_cnt=Channel_response['items'][0]['statistics']['viewCount']
 Channel_desc=Channel_response['items'][0]['snippet']['description']
 channel_playlst_id=Channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
 #print(channel_name,channel_id,channel_sub_cnt,channel_view_cnt,Channel_desc,channel_playlst_id)

 channel_sql = "INSERT INTO dinesh.CHANNEL_DETAILS(CHNL_ID,CHNL_NAME,CHNL_DESC,CHNL_TYPE,CHNL_VW_CNT,CHNL_SUB_CNT,CHNL_PLY_ID) VALUES (%s,%s,%s,%s,%s,%s,%s)"
 channel_valu=(channel_id,channel_name,Channel_desc,None,channel_view_cnt,channel_sub_cnt,channel_playlst_id)
 try:
   mycursor.execute(channel_sql, channel_valu)
   mydb.commit()
 except  :
   #st.write('test2')
   mydb.rollback()  
 chl_id_sql="SELECT ID FROM DINESH.CHANNEL_DETAILS WHERE CHNL_ID = %s"    
 mycursor.execute(chl_id_sql,[channel_id])
 chn_id = mycursor.fetchall()
 #print(mycursor.rowcount, "record inserted.")
 pl_id=channel_id
 #Get data for Playlist details from youtube API
 playlist_request = youtube.playlistItems().list(
        part="snippet,status,contentDetails",
        playlistId=channel_uploads
    )
 playlist_response = playlist_request.execute()


 playlist_details=[]
 playlist_details = playlist_response["items"]
 video_id = []
 video_details=[]
 #print(response)
 for i in range(len(playlist_details)):
    vid_id=playlist_details[i]['snippet']['resourceId']['videoId']
    video_id.append(vid_id)
 #print(video_id)
#Get data for all video details in above channel from youtube API
 for v_id in video_id:
    video_request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=v_id
        )
    video_response = video_request.execute()
    video_details=video_response["items"]
    #print(video_details)
    #Get data for all comment details in all videos of above channel from youtube API
    comment_request= youtube.commentThreads().list(
        part="snippet",
        videoId=v_id
        )
    comment_response = comment_request.execute()
    comment_details=comment_response["items"]
    for j in video_details:
         video_id=j['id']
         video_name=j['snippet']['title']
         video_desc=j['snippet']['description']
         video_pub_dt=j['snippet']['publishedAt']
         video_view_cnt=j['statistics']['viewCount']
         video_like_cnt=j['statistics']['likeCount']
         #video_dislike_cnt=j['statistics']['dislikeCount'] 
         video_fav_cnt=j['statistics']['favoriteCount'] 
         video_cmt_cnt=j['statistics']['commentCount'] 
         video_dur=j['contentDetails']['duration'] 
         video_tmbn=j['snippet']['thumbnails']['default']['url']
         video_cap_st=j['contentDetails']['caption'] 
         video_tags=j['snippet']['tags']
         #print(chn_id)
         video_sql = "INSERT INTO dinesh.VIDEO_DETAILS(CHN_ID,VID_ID,VID_NAM,VID_DESC,TAGS,VID_PUB,VID_VW_CNT,VID_LIK_CNT,VID_DLIK_CNT,VID_FAV_CNT,VID_CMT_CNT,VID_DUT,VID_THBNAIL,VID_CAP_STS) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
         video_valu=(chn_id[0][0],video_id,video_name,video_desc,str(video_tags),pd.to_datetime(video_pub_dt),video_view_cnt,video_like_cnt,None,video_fav_cnt,video_cmt_cnt,video_dur,video_tmbn,video_cap_st)
         try:
             mycursor.execute(video_sql, video_valu)
             mydb.commit()
         except  :
             #st.write('test1')
             mydb.rollback()
            
    for k in comment_details:
         comment_id=k['id']
         comment_text=k['snippet']['topLevelComment']['snippet']['textDisplay']
         comment_aut=k['snippet']['topLevelComment']['snippet']['authorDisplayName']
         comment_pub=k['snippet']['topLevelComment']['snippet']['publishedAt']
         comment_vid_id=k['snippet']['videoId']
         vid_id_sql="SELECT ID FROM DINESH.VIDEO_DETAILS WHERE VID_ID = %s"    
         mycursor.execute(vid_id_sql,[comment_vid_id])
         vid_id = mycursor.fetchall()
         #print(comment_id,comment_text,comment_aut,comment_pub)
         video_sql = "INSERT INTO dinesh.CMT_DETAILS(CHN_ID,VID_ID,CMT_ID,CMT_TEXT,CMT_AUT,CMT_PUB) VALUES (%s,%s,%s,%s,%s,%s)"
         video_valu=(chn_id[0][0],vid_id[0][0],comment_id,comment_text,comment_aut,pd.to_datetime(comment_pub))
         try:
             mycursor.execute(video_sql, video_valu)
             mydb.commit()
         except  :
             #st.write('test')
             mydb.rollback()
#code for Frount End using streamlit
st.set_page_config(layout="wide")
#new_title = '<p style="font-family:sans-serif; color:Green; font-size: 42px;">YouTube Harvesting</p>'
#st.markdown(new_title, unsafe_allow_html=True)
#st.image("DH.PNG", channels="BGR")
st.image("DH.PNG")
st.title("YouTube Harvesting")
channel_id=[]
st.header('Available Channel List')
chnl_list_sql="SELECT CHNL_NAME FROM DINESH.CHANNEL_DETAILS"    
mycursor.execute(chnl_list_sql)
chnl_list = mycursor.fetchall()
for cl in chnl_list:
 st.write(cl[0]) 
chanel_id = st.text_input("Please Enter YouTube Channel ID")
button_res=st.button("Harvest")

channel_id=list(chanel_id.split(','))

if button_res:
 chnl_chk_sql="SELECT CASE WHEN COUNT(*) > 0 THEN 'Y' ELSE 'N' END AS CHNL_CNT FROM DINESH.CHANNEL_DETAILS WHERE CHNL_ID =%s"    
 #mycursor.execute(chnl_chk_sql,channel_id[0][0])
 #chnl_chk_id = mycursor.fetchall()
 #st.write(chnl_chk_id) 
 #for loop for comma seperated channel id's
 for l in channel_id:
    mycursor.execute(chnl_chk_sql,[l])
    chnl_chk_id = mycursor.fetchall()
    chnl_prst = chnl_chk_id[0][0]
    if chnl_prst == "Y":
      st.error('This Channel is already available', icon=None)
    YouTube_Harves(l)
    #st.write(l)
#list of questions to be displayed in drop down list   
questions={"Q1":"What are the names of all the videos and their corresponding channels?",
"Q2":"Which channels have the most number of videos, and how many videos do they have?",
"Q3":"What are the top 10 most viewed videos and their respective channels?",
"Q4":"How many comments were made on each video, and what are their corresponding video names?",
"Q5":"Which videos have the highest number of likes, and what are their corresponding channel names?",
"Q6":"What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
"Q7":"What is the total number of views for each channel, and what are their corresponding channel names?",
"Q8":"What are the names of all the channels that have published videos in the year 2022?",
"Q9":"What is the average duration of all videos in each channel, and what are their corresponding channel names?",
"Q10":"Which videos have the highest number of comments, and what are their corresponding channel names?"}  
dropdown = st.selectbox("Select the Question", options=list(questions.values())) 
#based on options selected in dropdown sql query will run and answer wil be displayed
#for m in questions:
if dropdown== "What are the names of all the videos and their corresponding channels?":
   q1_sql ="SELECT CHNL_NAME as 'Channel Name',VID_NAM as 'Video Name' FROM DINESH.channel_details C JOIN DINESH.VIDEO_DETAILS V ON C.ID = V.CHN_ID"    
   mycursor.execute(q1_sql)
   q1_ans = mycursor.fetchall()
   for q1 in q1_ans:
    st.write(q1)
if dropdown== "Which channels have the most number of videos, and how many videos do they have?":
   q2_sql ="SELECT MAX(VID_CNT) AS 'Video Count' ,CHNL_NAME as 'Channel Name' FROM ( SELECT count(vid_id) AS VID_CNT,CHNL_NAME FROM DINESH.channel_details C JOIN DINESH.VIDEO_DETAILS V ON C.ID = V.CHN_ID GROUP BY CHNL_NAME ) AS CNT GROUP BY CHNL_NAME"    
   mycursor.execute(q2_sql)
   q2_ans = mycursor.fetchall()
   for q2 in q2_ans:
    st.write(q2) 
if dropdown== "What are the top 10 most viewed videos and their respective channels?":
   q3_sql ="SELECT VID_VW_CNT AS 'Video Count',CHNL_NAME as 'Channel Name' FROM DINESH.channel_details C JOIN DINESH.VIDEO_DETAILS V ON C.ID = V.CHN_ID ORDER BY 1 DESC LIMIT  10"    
   mycursor.execute(q3_sql)
   q3_ans = mycursor.fetchall()
   for q3 in q3_ans:
    st.write(q3)
if dropdown== "How many comments were made on each video, and what are their corresponding video names?":
   q4_sql ="SELECT VID_NAM as 'Video Name',COUNT(*) AS 'Comment Count' FROM DINESH.CMT_DETAILS C JOIN DINESH.VIDEO_DETAILS V ON C.VID_ID = V.ID GROUP BY V.VID_NAM"    
   mycursor.execute(q4_sql)
   q4_ans = mycursor.fetchall()
   for q4 in q4_ans:
    st.write(q4)
if dropdown== "Which videos have the highest number of likes, and what are their corresponding channel names?":
   q5_sql ="SELECT CHNL_NAME as 'Channel Name',VID_NAM as 'Video Name',MAX(VID_LIK_CNT) as 'Like Count' FROM DINESH.channel_details C JOIN DINESH.VIDEO_DETAILS V ON C.ID = V.CHN_ID GROUP BY C.CHNL_NAME,V.VID_NAM ORDER BY 3 DESC LIMIT  1"    
   mycursor.execute(q5_sql)
   q5_ans = mycursor.fetchall()
   for q5 in q5_ans:
    st.write(q5)
if dropdown== "What is the total number of likes and dislikes for each video, and what are their corresponding video names?":
   q6_sql ="select VID_NAM as 'Video Name',VID_LIK_CNT as 'Like Count',COALESCE(VID_DLIK_CNT,0) AS 'DisLike Count'  from DINESH.VIDEO_DETAILS"    
   mycursor.execute(q6_sql)
   q6_ans = mycursor.fetchall()
   for q6 in q6_ans:
    st.write(q6)
if dropdown== "What is the total number of views for each channel, and what are their corresponding channel names?":
   q7_sql =" select CHNL_NAME as 'Channel Name',CHNL_VW_CNT as 'Total View Count' from DINESH.channel_details"    
   mycursor.execute(q7_sql)
   q7_ans = mycursor.fetchall()
   for q7 in q7_ans:
    st.write(q7)
if dropdown== "What are the names of all the channels that have published videos in the year 2022?":
   q8_sql ="SELECT distinct c.CHNL_NAME as 'Channel Name' FROM DINESH.channel_details C JOIN DINESH.VIDEO_DETAILS V ON C.ID = V.CHN_ID where year(v.VID_PUB) = '2022'"    
   mycursor.execute(q8_sql)
   q8_ans = mycursor.fetchall()
   for q8 in q8_ans:
    st.write(q8)
if dropdown== "What is the average duration of all videos in each channel, and what are their corresponding channel names?":
   q9_sql ="select c.CHNL_NAME as 'Channel Name',round(avg((substr(vid_dur,1,instr(vid_dur,':')-1) *60)+ substr(vid_dur,instr(vid_dur,':')+1,length(vid_dur)))/60,2) as 'Average Video Duration' from ( select chn_id,replace(replace(replace(VID_DUT,'M',':'),'PT',''),'S','') as vid_dur from DINESH.VIDEO_DETAILS) as v inner join dinesh.channel_details c on v.chn_id = c.id group by CHNL_NAME;"    
   mycursor.execute(q9_sql)
   q9_ans = mycursor.fetchall()
   for q9 in q9_ans:
    st.write(q9)
if dropdown== "Which videos have the highest number of comments, and what are their corresponding channel names?":
   q10_sql ="select c.CHNL_NAME as 'Channel Name',VID_NAM as 'Video Name',count(cm.id) 'Comment Count' from DINESH.VIDEO_DETAILS v join dinesh.CMT_DETAILS cm on v.id = cm.vid_id join dinesh.channel_details c on v.chn_id = c.id group by VID_NAM,CHNL_NAME order by 2 desc limit 1"    
   mycursor.execute(q10_sql)
   q10_ans = mycursor.fetchall()
   for q10 in q10_ans:
    st.write(q10)	         
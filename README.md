# YouTube_Harvesting Synopsis
This the project#1 for YouTube Harvesting.
Get the Channel Id from the User 
Get the data from the Youtube API using Python code 
Clean up the data to get only required columns 
Connect to DB
Insert the Cleaned Up data to DB
Run the Sql to get the output for the displayed questions

Description:
  This project is to get the Youtube channel id from the user and get the data from Youtube API using Python code. After getting the data from Youtube API ,we need to cleanup the data by just getting the reuired fields from the json data.From Python we need to run the Channel list API and get the required fields from channel details, from channel details we need to get the playlist id. We need to pass the playlistid to the playlistitems and get the video details. A channel can have more than one videos listed, so we need to go on a loop to get the videoId. After this we need to pass the video id to the video API to get the video details get the required fields from vedio details. Next is to get the comment id from the every video and pass the commentid to the comment API and get the comment details to get the required fields from comment details.

 Database:
    We need to create three table for the above requirements,
         CHANNEL_DETAILS
         VIDEO_DETAILS
         CMT_DETAILS
    
    After cleaning up we need to connnect the Database from python and insert the data for each table created above.
After inserting data to the tables we need to do the front end coding using Python package Streamlit to create fields, button and list.
In this front we will create a inout field to get the channel id
Button to proceed with getting the dat from youtube API and insert the data to DB
List field to show the questions mentioned in the project document
Connect the DB using Python and run the select SQL queries and populate the answers when the questions are selected from the list 

    


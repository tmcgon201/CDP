#import aws sdk
import boto3
#import time module to allow sleep to happen
import time
#import os is used to access the audio files that are stored in the directory
import os

#this is used to access the current time to print to console
from datetime import datetime

#defining the accessor
s3 = boto3.resource('s3')
sns_client = boto3.client('sns', 'us-east-1')

#initialise the array of speeches
try:
    #the array is populated with the audio files found in the directory on EC2 Instance with the directory path appended
    audioArr = []
    for file in os.listdir("/home/ec2-user/audiofiles"):
        audioArr.append("/home/ec2-user/audiofiles/"+ file)
    #index used to help upload the right speech to the bucket
    index = 1

    #to upload the contents of the audio file array to the s3 bucket
    try:
    #this indicates that function has started and files will start getting uploaded to S3 bucket
        print("Uploading files...")
    #this is to loop around all the speeches found in the audio array list
        for speech in audioArr:
            print("Uploading audio file"+str(index)+speech[-4:]+"...")
            now = datetime.now() #capture current time
    #formats the current time
            current_time = now.strftime("%H:%M:%S")
    #the upload_file function can find and access the speeches within its directory
    #This copies the file string from audio array and uploads it to S3 Bucket
            s3.meta.client.upload_file(speech, 'mybuckets1933316', ('speech'+str(index)+speech[-4:])) 
    #uploads file in 30s intervals
            time.sleep(30)
    #print message displays that the function is still running with the time the file was uploaded
            print(current_time + ": File uploaded. Uploading next file...") 
            if index == 5:
    #print message to indicate function has completed
                print("All files uploaded. Exiting...")   
    #increase the index by 1 to allow for the correct message to be printed in the next loop
            index+=1

    #For when an issue occurs in the loop, print error message to console for further debugging
    except Exception as e:
        print("An error occurred when trying to upload the files! See below for more information")
        print(e)

#For when an issue occurs initializing the audio array, print error message to console for further debugging
except Exception as e:
        print("An error occurred when trying to access the directory! See below for more information")
        print(e)

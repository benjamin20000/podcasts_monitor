# podcasts_monitor

This repository implements a pipeline for processing podcasts services,
every service get a request to do some work on specific pod via kafka, from previous service.
The services are:


### 1. pre_process
- retrieving the data as wav audio file
- creating the basic metadata
  - bytes size - the size of the audio file
  - creation time
  - last access time
  - last modification time
  - original file path - save the origen path needed for later path and naming manipulation  
  - current file path 
  - inode - a unique number across one file system - needed for latter (next service)
  - device id - uniquely identifies the device - needed for latter (next service)
- producing the metadata to next service  


### 2. processor
- consuming the metadata from previous service
- creating unique id from the device id and the inode
- renaming the file to his unique id
- saving metadata in elasticsearch
- uploading the file to mongoDB gridFS
- making request to the next service via kafka 


### 3. stt service
converting STT can take some time, so it's a good idea to make a separate service. 
That will not slow down the process service.
stt service will:
- consume a request from process service
- download the audio from mongoDB to temp folder
- implement the STT using speech_recognition lib
- removing the temp file
- updating metadata on elasticsearch with the following fields:  - the new text we just get
  - The new text we just get.
  - The number of words the text contain - needed for the next service.
- produce a request to the next service


### 4. BDS detector
this service need to find a score for how much this pod promoting BDS.
its need to this by 2 lists
- black list - contain explicit BDS-prompting words - "black words"
- grey list - contain "grey words"
the logic to determine the score is as follows:
- count the black and grey words
- when black word count as 1 and grey word count as 1/2.
- then the counter result will be divided by the amount of the podcast's words
The service also will add a is_bds field to the metadata.
in case of pod that have 2 or 3 hours of random talk,
if this pod have 1 minute of BDS comment
i will still want to determine this pod as promoting BDS
so the threshold for choosing if this pod is bds or not, going to be quite low - 4%  for now.
another thing this service do is to place the pod into 3 BDS category:
- none
- medium
- high
the logic behind this will be as follows:
- bds_percent < 3%  ==> none
- 3% < bds_percent =< 6%  ==> medium
- 6% < bds_percent  ==> high



from multiprocessing.connection import wait
from os import system
from turtle import done
import requests
from apscheduler.schedulers.background import BackgroundScheduler as scheduler
import logging
import json
import time
import csv
import configparser
from datetime import datetime, timedelta
import sys

url = "https://v5.bvg.transport.rest/radar?north=52.6&west=13.2&south=52.21942&east=13.6"
outputDirectory = "F:\\UpWork\\CSV_FILES\\"
timeIntervalInSeconds = 5
maxInstances = 10
time_till__to_keep_running_in_minutes = 30
now = datetime.now()
timeWhenToStop = now + timedelta(minutes = 30)
requiredCols = [
    'tripId',
    'productName',
    'latitude',
    'longitude',
    'timestamp'
]

logging.getLogger('apscheduler.executors.default').propagate = False


#SEND HTTP REQUEST
def send_request():
    try:
        now = datetime.now()
        timeDiffInMinutes = divmod((timeWhenToStop - now).total_seconds(), 60)[0]
        if(timeDiffInMinutes < 0):
            "Stopping Job. Time configuration limit reached."
            stopJob()
        request = requests.get(url)
        createCSV(request.content)
    except (requests.Timeout, requests.ConnectionError, requests.HTTPError) as err:
        print("Error while getting")
        print(err)
    finally:
        request.close()


def loadConfig():
    global url, outputDirectory, maxInstances,timeIntervalInSeconds, time_till__to_keep_running_in_minutes, timeWhenToStop
    config = configparser.ConfigParser()
    config.read('config.ini')
    url = config['MainConfig']['url']
    outputDirectory=config['MainConfig']['output_directory']
    timeIntervalInSeconds=config['MainConfig']['execution_time_interval_in_seconds']
    timeIntervalInSeconds = int(timeIntervalInSeconds)
    maxInstances=config['MainConfig']['max_instances']
    maxInstances=int(maxInstances)
    time_till__to_keep_running_in_minutes = config['MainConfig']['time_till__to_keep_running_in_minutes']
    time_till__to_keep_running_in_minutes = int(time_till__to_keep_running_in_minutes)
    now = datetime.now()
    timeWhenToStop =  now + timedelta(minutes = time_till__to_keep_running_in_minutes)

def addJob():
    sch.add_job(send_request, 'interval', seconds=timeIntervalInSeconds, max_instances=maxInstances)

def stopJob():
    print("Stopping Job...")
    sch.shutdown(wait=False)
    print("Job shut down successfully!")
    print("You  can exit the program window.")
    ##sys.exit()

#This method created the CSV
def createCSV(json_response):
    record_dict = json.loads(json_response)
    allRecords = []
    timestamp = str(time.time())
    filePath = outputDirectory +  '/' + timestamp + '.csv'
    for record in record_dict:
        csvRecord  = {
            'tripId' : record['tripId'], 'productName': record['line']['productName'], 'latitude' : record['location']['latitude'], 'longitude' : record['location']['latitude'],'timestamp' : timestamp 
            }
        allRecords.append(csvRecord)
    with open(filePath, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, requiredCols)
        dict_writer.writeheader()
        dict_writer.writerows(allRecords)
        output_file.close()        
                




def main():
    try:
        print("Loading configurations........")
        loadConfig()
        print("Configurations loaded")
        print("---------------------------------------") 
        print('Files will be written to ' + outputDirectory)
        print("---------------------------------------") 
        addJob()
        print("Starting to fetch URL content...")
        sch.start()
         # simulate application activity (which keeps the main
    # thread alive).
        while True:
            pass
    except KeyboardInterrupt:
        if sch.state:
                stopJob()
                

print('Starting Job, ctrl-c to exit!')
sch = scheduler(daemon=True)
main()                
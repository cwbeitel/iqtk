from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials


def run(job_name, project, bucket, template):

    credentials = GoogleCredentials.get_application_default()
    service = build('dataflow', 'v1b3', credentials=credentials)

    # Set the following variables to your values.
    JOBNAME = job_name
    PROJECT = project
    BUCKET = bucket
    TEMPLATE = template

    BODY = {
        "jobName": "{jobname}".format(jobname=JOBNAME),
        "gcsPath": "gs://{bucket}/templates/{template}".format(bucket=BUCKET, template=TEMPLATE),
        "parameters": {
            "inputFile" : "gs://{bucket}/input/my_input.txt",
            "outputFile": "gs://{bucket}/output/my_output.txt".format(bucket=BUCKET)
         },
         "environment": {
            "tempLocation": "gs://{bucket}/temp".format(bucket=BUCKET),
            "zone": "us-central1-f"
         }
    }

    request = service.projects().templates().create(projectId=PROJECT, body=BODY)
    response = request.execute()

    print(response)

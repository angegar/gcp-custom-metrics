from google.api import label_pb2 as ga_label
from google.api import metric_pb2 as ga_metric
from google.cloud import monitoring_v3
import time, random

# Authenticate with gcloud auth application-default login

class TimeSerie:
    def __init__(self):
        self.client = monitoring_v3.MetricServiceClient()
        self.projectId = "bds-rd-sf3-dev"
        self.location = "europe-west1"
        self.projectName = f"projects/{self.projectId}"
        self.type = "custom.googleapis.com/lab/vpn/bandwidth/download2"
       
    # def createDescriptor(self):
    #     # CREATE DESCRIPTOR
    #     # project_name = f"projects/{project_id}"
    #     descriptor = ga_metric.MetricDescriptor()
    #     descriptor.type = "custom.googleapis.com/lab/vpn/bandwidth/download"
    #     descriptor.metric_kind = ga_metric.MetricDescriptor.MetricKind.GAUGE
    #     descriptor.value_type = ga_metric.MetricDescriptor.ValueType.DOUBLE
    #     descriptor.description = "Download speed from the lab in byte per second"

    #     labels = ga_label.LabelDescriptor()
    #     labels.key = "from"
    #     labels.value_type = ga_label.LabelDescriptor.ValueType.STRING
    #     labels.description = "Source test server"
    #     descriptor.labels.append(labels)

    #     labels = ga_label.LabelDescriptor()
    #     labels.key = "to"
    #     labels.value_type = ga_label.LabelDescriptor.ValueType.STRING
    #     labels.description = "Destination test server"
    #     descriptor.labels.append(labels)

    #     descriptor = self.client.create_metric_descriptor(
    #         name=self.projectName, metric_descriptor=descriptor
    #     )
    #     print("Created {}.".format(descriptor.name))

    def writeTimeSerie(self, speed=random.uniform(10.5, 75.5), sourceServer="sf-centrale", destinationServer="artifactory"):
        series = monitoring_v3.TimeSeries()
        series.metric.type = self.type
        series.metric.labels["from"] = sourceServer
        series.metric.labels["to"] = destinationServer

        series.resource.type = "generic_task"
        series.resource.labels["namespace"] = "ech-monitoring"
        series.resource.labels["project_id"] = self.projectId
        series.resource.labels["location"] = self.location
        series.resource.labels["job"] = "lab-vpn"
        series.resource.labels["task_id"] = "lab-vpn"

        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10**9)
        interval = monitoring_v3.TimeInterval(
            {"end_time": {"seconds": seconds, "nanos": nanos}}
        )

        point = monitoring_v3.Point({"interval": interval, "value": {"double_value": speed}})
        series.points = [point]

        self.client.create_time_series(name=self.projectName, time_series=[series])
        print("Done writing time series.")


    def deleteTimeSerie(self):
        descriptor_name :str = "projects/bds-rd-sf3-dev/metricDescriptors/custom.googleapis.com/lab/vpn/bandwidth/download2"
        self.client.delete_metric_descriptor(name=descriptor_name)
        print("Deleted metric descriptor {}.".format(descriptor_name))

data = TimeSerie()
# data.deleteTimeSerie()
for i in range(50):
    data.writeTimeSerie()
    time.sleep(10)
    print(f"Data {i} written")
    i += 1

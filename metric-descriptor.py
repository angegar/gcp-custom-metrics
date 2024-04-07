from google.api import label_pb2 as ga_label
from google.api import metric_pb2 as ga_metric
from google.cloud import monitoring_v3
import time, random

# CREATE DESCRIPTOR
project_id="bds-rd-sf3-dev"
location="europe-west1"
client = monitoring_v3.MetricServiceClient()
project_name = f"projects/{project_id}"
descriptor = ga_metric.MetricDescriptor()
descriptor.type = "custom.googleapis.com/lab/vpn/bandwidth/download"
descriptor.metric_kind = ga_metric.MetricDescriptor.MetricKind.GAUGE
descriptor.value_type = ga_metric.MetricDescriptor.ValueType.DOUBLE
descriptor.description = "Download speed from the lab in byte per second"

labels = ga_label.LabelDescriptor()
labels.key = "from"
labels.value_type = ga_label.LabelDescriptor.ValueType.STRING
labels.description = "Source test server"
descriptor.labels.append(labels)

labels = ga_label.LabelDescriptor()
labels.key = "to"
labels.value_type = ga_label.LabelDescriptor.ValueType.STRING
labels.description = "Destination test server"
descriptor.labels.append(labels)

descriptor = client.create_metric_descriptor(
    name=project_name, metric_descriptor=descriptor
)
print("Created {}.".format(descriptor.name))


# WRITE METRICS
# from google.cloud import monitoring_v3

# client = monitoring_v3.MetricServiceClient()
# project_name = f"projects/{project_id}"

series = monitoring_v3.TimeSeries()

series.metric.type = descriptor.type
series.metric.labels["from"] = "sf-centrale"
series.metric.labels["to"] = "artifactory"

series.resource.type = "generic_task"
series.resource.labels["namespace"] = "ech-monitoring"
series.resource.labels["project_id"] = project_id
series.resource.labels["location"] = location
series.resource.labels["job"] = "lab-vpn"
series.resource.labels["task_id"] = "lab-vpn"

now = time.time()
seconds = int(now)
nanos = int((now - seconds) * 10**9)
interval = monitoring_v3.TimeInterval(
    {"end_time": {"seconds": seconds, "nanos": nanos}}
)

speed=random.uniform(10.5, 75.5)

point = monitoring_v3.Point({"interval": interval, "value": {"double_value": speed}})
# point = monitoring_v3.Point({"value": 68.5})
series.points = [point]

client.create_time_series(name=project_name, time_series=[series])
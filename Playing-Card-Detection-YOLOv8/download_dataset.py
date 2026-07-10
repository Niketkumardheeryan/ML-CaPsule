from roboflow import Roboflow

rf = Roboflow(api_key="j29PBczQJNP6Rq3uOV0V")
project = rf.workspace("0lauk0").project("playing-cards-muou8")
version = project.version(10)
dataset = version.download("yolov8")

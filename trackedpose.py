from connectmongo import returnclient,returndatabase
current_Client = returnclient()
current_DB = returndatabase()
trackedPoseCollection = current_DB["TrackedPose"]
def insert_into_trackedpose_collection(record):
    trackedPoseCollection.insert_one(record)
    
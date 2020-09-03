import os
import uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


class BlobStorageClient:

    def __init__(self, connect_str):
        self.connection_str = connect_str
        # Create the BlobServiceClient object which will be used to create a container client
        self.blob_service_client = BlobServiceClient.from_connection_string(
            self.connection_str)
        # Create a unique name for the container
        self.container_name = "rchoitestdev2"
        # Create the container
        get_match_container = next((c for c in self.blob_service_client.list_containers(
        ) if c['name'] == self.container_name), None)

        if get_match_container == None:
            self.container_client = self.blob_service_client.create_container(
                self.container_name)

        self.file_name = ""

    def upload_file(self, file):
        extension_of_image = file.filename.split(".")[1]
        fn = str(uuid.uuid4()) + "." + extension_of_image
        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name, blob=fn)

        # Upload the created file
        blob_client.upload_blob(file)
        return fn


if __name__ == "__main__":
    blobClinet = BlobStorageClient
    print(blobClinet.connection_str)

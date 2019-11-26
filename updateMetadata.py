import boto3

s3 = boto3.resource('s3')


def update_metadata(bucket_name, object_key, metadata):
    file = s3.Object(bucket_name, object_key)
    for label in metadata:
        file.metadata.update({label: metadata[label]})
    file.copy_from(CopySource={'Bucket': bucket_name, 'Key': object_key},
                   Metadata=file.metadata,
                   MetadataDirective='REPLACE')

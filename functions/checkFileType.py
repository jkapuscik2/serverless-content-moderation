from mimetypes import MimeTypes

mime = MimeTypes()


def handler(event, ctx):
    mime_type = mime.guess_type(event["objectKey"])

    return {
        "bucketName": event["bucketName"],
        "objectKey": event["objectKey"],
        "mime": mime_type[0]
    }

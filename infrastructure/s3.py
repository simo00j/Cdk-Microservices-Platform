from aws_cdk import aws_s3 as s3



def setup_s3(stack, project,role) :
    buckets = project.get('buckets',{})
    if buckets : 
        for bucket in buckets:
            bucket_name = bucket.get('name',f"{project['name']}").lower().replace(' ', '')
            bucket = s3.Bucket(
                stack,
                f"consulting-{bucket_name}-bucket",
                bucket_name=f"consulting-{bucket_name}-bucket" 
            )
            bucket.grant_read_write(role)

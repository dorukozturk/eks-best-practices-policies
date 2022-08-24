import boto3
import click
from colorama import Fore, Back, Style, init


def check_endpoint_public_access(region: str, cluster: str):
    client = boto3.client("eks", region_name=region)
    cluster_metadata = client.describe_cluster(name=cluster)
    endpoint_access = cluster_metadata["cluster"]["resourcesVpcConfig"][
        "endpointPublicAccess"
    ]
    if endpoint_access:
        print(Fore.RED + "Make the EKS Cluster Endpoint Private!")
        print(
            Style.DIM
            + "https://aws.github.io/aws-eks-best-practices/security/docs/iam/#make-the-eks-cluster-endpoint-private"
        )


def check_access_to_instance_profile(region: str, cluster: str):
    client = boto3.client("ec2", region_name=region)
    instance_metadata = client.describe_instances(
        Filters=[
            {
                "Name": "tag:aws:eks:cluster-name",
                "Values": [
                    cluster,
                ],
            },
        ]
    )
    for instance in instance_metadata["Reservations"]:
        if (
            instance["Instances"][0]["MetadataOptions"][
                "HttpPutResponseHopLimit"
            ]
            == 2
        ):
            print(
                Fore.RED
                + f"Restrict access to the instance profile assigned to the worker node {instance['Instances'][0]['InstanceId']}"
            )
            print(
                Style.DIM
                + "https://aws.github.io/aws-eks-best-practices/security/docs/iam/#make-the-eks-cluster-endpoint-private"
            )


def check_logs_are_enabled(region, cluster):
    client = boto3.client("eks", region_name=region)
    cluster_metadata = client.describe_cluster(name=cluster)
    logs = cluster_metadata["cluster"]["logging"]["clusterLogging"][0][
        "enabled"
    ]

    if not logs:
        print(Fore.RED + "Enable control plane logs for auditing")
        print(
            Style.DIM
            + "https://aws.github.io/aws-eks-best-practices/security/docs/detective/#enable-audit-logs"
        )


@click.command()
@click.argument("region")
@click.argument("cluster")
def check_eks_best_practices(region, cluster):
    init(autoreset=True)
    check_endpoint_public_access(region, cluster)
    check_access_to_instance_profile(region, cluster)
    check_logs_are_enabled(region, cluster)


if __name__ == "__main__":
    check_eks_best_practices()

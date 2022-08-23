#!/bin/bash

while [ $# -gt 0 ]; do

   if [[ $1 == *"--"* ]]; then
        v="${1/--/}"
        declare $v="$2"
   fi

  shift
done

endpointPublicAccess=$(aws eks describe-cluster \
    --name $cluster_name --region $region \
    | jq '.cluster.resourcesVpcConfig.endpointPublicAccess')

if [ "$endpointPublicAccess" = true ] ; then
    echo 'Make the EKS Cluster Endpoint Private!'
    echo 'https://aws.github.io/aws-eks-best-practices/security/docs/iam/#make-the-eks-cluster-endpoint-private'
fi

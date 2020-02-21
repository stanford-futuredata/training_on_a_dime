# Pricing logs from February and March 2020

This directory contains pricing information of instances with GPUs for three
different cloud providers (AWS, Azure, and GCP) that we collected in Februrary
and March 2020. The `aws`, `azure`, and `gcp` notebooks show how these logs can
be parsed.

Pricing information for AWS and GCP was collected using the scripts provided in
`scripts/`.

Logs under the `availability` sub-directory are collected by spinning up an
instance of the desired type and in the desired region, and then pinging the
instance every 15 minutes to see if the instance is still up. If it is not,
the instance is marked as preempted, and the process is repeated.

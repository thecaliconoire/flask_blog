## Helm Charts

Helm is used to template kubernetes manifests, in order to automate and standardize the release process.

This ensures that all clusters are similarly configured so the engineering team can inspect a realistic simulation of a production deployment. Assuming similar manifests are required for each of your environments cluster. If so, the management overhead of your kubernetes can be  greatly reduced.

These changes can be propagated through multiple environments from testing to staging all the way to production.

Helm does this through the use of charts. Charts are a collection of YAML files that describe the state of multiple Kubernetes resources.

The files and folders in this direction are as follows:

`Chart.yaml` This yaml file is used to expose the Helm charts details. These details include description version and dependencies

`templates/` folder is used to hold the template YAML  manifests for Kubernetes resources. Templates are files that are require a input file in order to generate valid kubernetes resources. This includes template files for resources such as namespaces, services and deployments.
Template files allow you to use Go templating instead of hardcoding the name of the Namespaces, it an be parameterized.

`values.yaml` This holds your default input configuration file for the chart. If no other values file is supplied these will be the default parameters.

These values are consumed by the templated YAML manifests through a `.Values` object.

This combined leads to a suite of valid Kubernetes resources that can be successfully deployed.


# Features of Helm


Single Command Install
`helm install`

Provide Insights for Releases
`helm status`

Perform Simple Updates/Upgrades
`helm upgrade`

Provide the Ability to Rollback
`helm rollback`

Simplify Deployment


Single Command Uninstall
`helm uninstall`
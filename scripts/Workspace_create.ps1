# Create the Service Principal with az after login in
$Global:servicePrincipal = "banking-auth"
$Global:clientId = (az ad sp create-for-rbac --sdk-auth --name $servicePrincipal | ConvertFrom-Json).clientId

#Capture the "objectId" using the clientID:
$Global:objectId = (az ad sp show --id $clientId | ConvertFrom-Json).objectId

$Global:workspace = "banking-ws"
$Global:resourcegroup = "alexeirg"
"CREATE RESOURCE GROUP"
az group create --name $resourcegroup --location francecentral
"CREATE WORKSPACE"
az ml workspace create -w $workspace -g $resourcegroup

"Assign the role to the new Service Principal for the given Workspace, Resource Group and User objectId"
az ml workspace share -w $workspace -g $resourcegroup --user $objectId --role owner
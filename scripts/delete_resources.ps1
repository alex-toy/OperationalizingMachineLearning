################################################################
#DELETE ALL GROUPS AND RESOURCES INSIDE :

$groups = az group list | ConvertFrom-Json
"Following resource groups will be deleted :"
$groups | Foreach-Object { $_.name }
$groups | Foreach-Object { az group delete -n $_.name --yes }
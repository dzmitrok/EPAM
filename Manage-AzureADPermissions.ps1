[CmdletBinding()]
param(
    [parameter(mandatory=$true)]
    [ValidateSet("Delegated","Application")]
    [string]$PermissionType
)
Connect-AzureAD
$AzureMgmtPrincipal = Get-AzureADServicePrincipal -All $true | Out-GridView -PassThru -Title "Select an API"
$AzureApp = Get-AzureADApplication | Out-GridView -Title "Availible Azure Apps" -PassThru
$AzureMgmtAccess = New-Object -TypeName "Microsoft.Open.AzureAD.Model.RequiredResourceAccess"
$AzureMgmtAccess.ResourceAppId = $AzureMgmtPrincipal.AppId
switch ($PermissionType){
    Application {
                $AzurePermission = $AzureMgmtPrincipal.AppRoles |
                Out-GridView -PassThru -Title "Azure $($AzureMgmtPrincipal.DisplayName) application Permissions"
                }
      Delegated {
                $AzurePermission = $AzureMgmtPrincipal.Oauth2Permissions | 
                Out-GridView -PassThru -Title "Azure $($AzureMgmtPrincipal.DisplayName) delegated (oauth2) Permissions"
    }
}
$AzureSvcMgmt = New-Object -TypeName "microsoft.open.azuread.model.resourceAccess" -ArgumentList $AzurePermission.Id, "Scope"
$AzureMgmtAccess.ResourceAccess.Add($AzureSvcMgmt)
Set-AzureADApplication -ObjectId $AzureApp.ObjectId -RequiredResourceAccess @($AzureMgmtAccess)
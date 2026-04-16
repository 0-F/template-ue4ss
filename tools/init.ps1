<#
.SYNOPSIS
    Initializes the local development environment for the repository.

.DESCRIPTION
    This script copies template items from the templates directory into the project
    root and synchronizes the generic .code-workspace file to a repository-specific
    name when needed.
#>

# Move to the parent directory (project root).
Push-Location (Split-Path -Parent $PSScriptRoot)

$codeWorkspaceTemplateName = ".code-workspace"

$templatesDir = "templates"
$excludedTemplateItems = @(
    ".code-workspace"
)

# Get the current folder name to define the workspace name.
$repoName = (Get-Item .).Name

# Copy all template items into the project root except files handled separately below.
if (Test-Path $templatesDir) {
    Get-ChildItem -Path $templatesDir -Force |
    Where-Object { $_.Name -notin $excludedTemplateItems } |
    ForEach-Object {
        Copy-Item -Path $_.FullName -Destination . -Recurse -Force
        Write-Output "Success: $($_.Name) copied from $templatesDir to project root."
    }
}
else {
    Write-Warning "Templates directory '$templatesDir' not found. Skipping template copy."
}

# Copy the generic VSCode workspace template to a repo-specific workspace file when needed.
$cwSource = Join-Path -Path $templatesDir $codeWorkspaceTemplateName
$cwDestination = "$repoName.code-workspace"
if (Test-Path $cwSource) {
    if (-not (Test-Path $cwDestination)) {
        Copy-Item -Path $cwSource -Destination $cwDestination
        Write-Output "Success: $cwSource copied to $cwDestination."
    }
    else {
        Write-Output "Skip: $cwDestination already exists. No copy performed."
    }
}
else {
    Write-Warning "Source file '$cwSource' not found. Skipping workspace sync."
}

Pop-Location

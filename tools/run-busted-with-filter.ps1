<#
.SYNOPSIS
    Cleans the filter file and executes Busted tests.
.DESCRIPTION
    This script prepares the Busted filter before execution.
    It is useful when you do not want to run the entire test suite and prefer
    targeting a specific test or group of tests.

    The filter corresponds to the Busted "--filter" option.
    Official documentation: https://lunarmodules.github.io/busted/#usage
    Option detail:
    --filter=PATTERN          only run test names matching the Lua pattern
                              (default: [])

    To add a filter, you must edit 'busted-filter.txt' by either:
    - Replacing the entire file content with your test name.
    - Adding the test name as a new line at the end of the file.

    The script automatically isolates and cleans the last line for use.

.EXAMPLE
    If the last line is: "MyTestName"
    The script extracts: MyTestName

.EXAMPLE
    If the last line is: describe("getCommandLocale()", function()
    The script extracts: getCommandLocale()

.EXAMPLE
    If the last line is: it("should return the correct options", function()
    The script extracts: should return the correct options

.EXAMPLE
    Content ending with two empty lines:
    getCommandLocale()
    [empty line]
    [empty line]
    Result: (Clears filter, executes all tests)
#>

$file = Join-Path -Path $PSScriptRoot -ChildPath 'busted-filter.txt'
$filter = ''

# Get all lines from the file.
$content = Get-Content $file

# Check if the file is not empty.
if ($content) {
    # If content is a single string, convert to array to handle indexing.
    $lines = @($content)

    # Get the last line and remove trailing/leading spaces.
    $filter = $lines[-1].Trim()

    # Matches a string strictly wrapped in double quotes.
    if ($filter -match '"(.+)"') {
        $filter = $Matches[1]
    }

    # Overwrite the file with only this cleaned line.
    $filter | Set-Content $file
}

if ($filter) {
    & busted --filter="$filter"; Write-Output "🔍 Filter in $file → $filter"
}
else {
    & busted; Write-Output "🔍 No filter in $file"
}

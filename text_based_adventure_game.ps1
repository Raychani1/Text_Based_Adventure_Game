
# Check for existence of Virtual Environment
function check_for_virtual_environment {
    $venv_directory = Join-Path -Path $pwd -ChildPath "\venv-win"

    # Check if the Virtual Environment already exists
    if (Test-Path -Path $venv_directory) {
        Write-Host -ForegroundColor 'Green' "Found existing Virtual Environment`n"
    } else {
        Write-Host -ForegroundColor 'Green' "Creating Virtual Environment`n"
        python.exe -m venv venv-win
    }
}

# Activate Virtual Environment
function activate_virtual_environment {
    Write-Host -ForegroundColor 'Green' "Activating Virtual Environment`n"
    .\venv-win\Scripts\Activate.ps1
}

# Get current Virtual Environment name
function get_virtual_environment {
    Write-Host -ForegroundColor 'Green' "Current Virtual Environment`n"
    Write-Host "$env:VIRTUAL_ENV`n"
}

# Run the setup.py script
function run_setup {
    Write-Host -ForegroundColor 'Green' "Running setup.py`n"
    python.exe ./adventure_game/utils/setup.py $pwd
}

# Run the main.py script
function run_main($mode) {
    Write-Host -ForegroundColor 'Green' "Running main.py`n"
    Start-Sleep -s 3
    Clear-Host
    python.exe ./adventure_game/main.py $mode
}

# Run the whole project
function run($arguments) {
    switch ($arguments.Count)
    {
        {($_ -eq 0) -or ($_ -eq 2)} {
            check_for_virtual_environment
            activate_virtual_environment
            get_virtual_environment
            run_setup
            run_main($arguments)
            Break
        }
        1 {
            Write-Host -ForegroundColor 'Red' "One argument is missing!`n"
            Break 
        }
        Default {
            Write-Host -ForegroundColor 'Red' "Too many arguments!`n"
        }
    }
}

run($args)

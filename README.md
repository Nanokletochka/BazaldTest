# BazaldTest
The purpose of this project is to assess the professional skills of a candidate for the position of Python developer (myself). The following tasks need to be accomplished using the REST API of the AltLinux database:
Task 1. Obtain lists of binary packages for the branches sisyphus and p10.
Task 2. Compare the obtained lists of packages and output a JSON that displays:
Task 2.1. All packages that are present in p10 but not in sisyphus.
Task 2.2. All packages that are present in sisyphus but not in p10.
Task 2.3. All packages whose version-release is greater in sisyphus than in p10.
This needs to be done for each architecture supported by the branch.

## Project Status
The project is currently under development and is not the final version.
As of now, task 1 has been implemented.

## Getting Started
- Install Python version 3+.
- Install the requests library.

## Usage
Open the file module.py, call the function, and pass it the branch name from which the list of binary packages will be retrieved.

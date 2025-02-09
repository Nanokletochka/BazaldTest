# BazaldTest
The purpose of this project is to assess the professional skills of a candidate for the position of Python developer (myself). The following tasks need to be accomplished using the REST API of the AltLinux database:
- Task 1. Obtain lists of binary packages for the branches sisyphus and p10.
- Task 2. Compare the obtained lists of packages and output a JSON that displays:
- Task 2.1. All packages that are present in p10 but not in sisyphus.
- Task 2.2. All packages that are present in sisyphus but not in p10.
- Task 2.3. All packages whose version-release is greater in sisyphus than in p10.

This needs to be done for each architecture supported by the branch.
Provide main module with CLI.

## Getting Started
- Install Python version 3+.
- Install the "requests" library.
- Install the "rpm_vercmp" library.
- Install the "click" library.

## Usage
The file module.py contains the main logic of the program, and the file cli.py contains the CLI implementation for module.py.

To run the program, use the command ```python cli.py <function_name> <first_branch_name> <second_branch_name> [--limit]```.

Available function names are: 
- 'unique' - compares packages from the first branch with packages from the second branch and returns a JSON structure containing packages from the first branch that do not exist in the second. The order of passing names for both branches is important;
- 'rpm' - finds identical packages in both branches and returns a JSON structure containing those packages from the first branch where version-release is greater.
Optional params:
- '--limit' parameter controls the number of packages in first branch to be compared will all in the second branch.

Both "unique" and "rpm" functions return JSON strings in format:
```
{
	"length": <num_of_packages>,
	"packages": {
		<architecture_type>: [
				<packages>
		],
		<another_architecture_type>: [
				<packages>
		],
		
	}
}
```
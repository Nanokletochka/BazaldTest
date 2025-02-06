import requests


# API base url
api_url = "https://rdb.altlinux.org/api/"

# API method url
export_method = "export/branch_binary_packages/"


def get_packages(branch: str):
    """
    Get binary packages from branch.


    Args:
        branch (str): branch name

    Returns:
        dict: json response object
    """

    # Getting response from API
    response = requests.get(api_url + export_method + branch)

    # Verifying status code
    if response.status_code != 200:
        raise Exception(
            f"get_packages() get {response.status_code} status code for branch '{branch}'."
            )
    
    return response.json()
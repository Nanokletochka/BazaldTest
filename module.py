import requests
from rpm_vercmp import vercmp

# API base url
api_url = "https://rdb.altlinux.org/api/"

# API method url
export_method = "export/branch_binary_packages/"


def get_packages(branch: str) -> dict:
    """
    Retrieves binary package information from a specified branch via API.


    Fetches a JSON response containing binary package data from a specific branch
    using the API endpoint defined by `api_url + export_method + branch`.

    Args:
        branch (str): The name of the branch to retrieve package information.

    Returns:
        dict: A dictionary representing the JSON response from the API.
    """

    # Getting response from API
    response = requests.get(api_url + export_method + branch)

    # Verifying status code
    if response.status_code != 200:
        raise Exception(
            f"get_packages() get {response.status_code} status code for branch '{branch}'."
        )

    return response.json()


def compare_existing(pkg_1_json: dict, pkg_2_json: dict, limit: int = None) -> dict:
    """
    Compares two lists of binary packages and identifies packages present in the first list
    but not in the second, based on key metadata fields (arch, name, epoch, version, release).

    The function extracts package lists from input JSON dictionaries, compares them,
    and returns a dictionary containing packages unique to the first list, organized by architecture.

    Example:
    >> p10 = get_packages("p10")
    >> sisyphus = get_packages("sisyphus")
    >> unique_packages = compare_existing(sisyphus, p10, limit=10000)

    Args:
        pkg_1_json (dict): A dictionary containing a list of binary packages under the key "packages".
                            Generated using a function get_packages(). Represents the 'source' list.
        pkg_2_json (dict): A dictionary containing a list of binary packages under the key "packages".
                           Represents the 'target' list against which the first list is compared.
        limit (int, optional):  Limits the number of packages to compare from each list.
                              If None, all packages from pkg_1_json will be compared. Defaults to None.

    Returns:
        dict: A dictionary where keys are architecture types and values are lists of
            package dictionaries that are unique to the first package list (pkg_1_json).
            Returns an empty dictionary if no unique packages are found.
    """

    # Extract list of packages out of json dict
    pkgs_1, pkgs_2 = pkg_1_json["packages"], pkg_2_json["packages"]

    # Set a limit
    if limit:
        pkgs_1, pkgs_2 = pkgs_1[:limit], pkgs_2[:limit]
    else:
        limit = pkg_1_json['length']

    # Fields of packages metadata to compare
    key_fields = ["arch", "name", "epoch", "version", "release"]

    # Dictionary to write results in format: {<arch type>: [<packages>]}
    unique_pkgs = {}

    # Loop thought list of packages №1
    for i, pkg_1_elem in enumerate(pkgs_1):
        # Loop thought list of packages №2
        for pkg_2_elem in pkgs_2:
            # Loop thought key fields
            for field in key_fields:
                # Check identity
                if pkg_1_elem[field] != pkg_2_elem[field]:
                    break
            else:
                # This section means that pkg_1_elem equals to pkg_2_elem
                break
        else:
            # This section means that there no pkg_1_elem in pkgs_2
            arch = pkg_1_elem["arch"]
            if arch not in unique_pkgs:
                # Create new list
                unique_pkgs[arch] = []
            unique_pkgs[arch].append(pkg_1_elem)

        # [INFO]
        if (i + 1) % 100 == 0:
            print(f"- {i + 1}/{limit} packages processed")

    return unique_pkgs


def comparator(package_1: dict, package_2: dict) -> bool:
    """
    Compare two packages using RPM comparing rules.


    Args:
        package_1 (dict): first package
        package_2 (dict): second package

    Returns:
        bool: is first package epoch:version-release newer than the second
    """

    # Compare epochs
    if package_1["epoch"] != package_2["epoch"]:
        return True if package_1["epoch"] > package_2["epoch"] else False

    # Compare version-release
    pkg_1_vr = f"{package_1['version']}-{package_1['release']}"
    pkg_2_vr = f"{package_2['version']}-{package_2['release']}"
    cmp_res = vercmp(pkg_1_vr, pkg_2_vr)

    return True if cmp_res == 1 else False


def compare_rpm(pkg_1_json: dict, pkg_2_json: dict, limit: int = None) -> dict:
    """
    Compares two lists of binary packages using RPM comparing rules.


    Finds the same packages using fields as name and arch,
    then compare epoch:version-release of these packages and finds the newest.

    Args:
        pkg_1_json (dict): A dictionary containing a list of binary packages under the key "packages".
                            Generated using a function get_packages(). Represents the 'source' list.
        pkg_2_json (dict): A dictionary containing a list of binary packages under the key "packages".
                           Represents the 'target' list against which the first list is compared.
        limit (int, optional):  Limits the number of packages to compare from each list.
                              If None, all packages from pkg_1_json will be compared. Defaults to None.

    Returns:
        dict: A dictionary where keys are architecture types and values are lists of
            package dictionaries. Returns an empty dictionary if there aren't newer versions
            in package list №1 comparing to package list №2.
    """

    # Extract list of packages out of json dict
    pkgs_1, pkgs_2 = pkg_1_json["packages"], pkg_2_json["packages"]

    # Set a limit
    if limit:
        pkgs_1, pkgs_2 = pkgs_1[:limit], pkgs_2[:limit]
    else:
        limit = pkg_1_json['length']

    # Fields of packages metadata to compare
    key_fields = ["arch", "name"]

    # Dictionary to write results in format: {<arch type>: [<packages>]}
    pkgs = {}

    # Loop thought list of packages №1
    for i, pkg_1_elem in enumerate(pkgs_1):
        # Loop thought list of packages №2
        for pkg_2_elem in pkgs_2:
            # Loop thought key fields
            for field in key_fields:
                # Check identity
                if pkg_1_elem[field] != pkg_2_elem[field]:
                    break
            else:
                # This section means that pkg_1_elem equals to pkg_2_elem
                # Compare versions using RPM comparing rules
                if comparator(pkg_1_elem, pkg_2_elem):
                    # Add package to dict
                    arch = pkg_1_elem["arch"]
                    if arch not in pkgs:
                        pkgs[arch] = []
                    pkgs[arch].append(pkg_1_elem)

                break

        # Progress information
        if (i + 1) % 100 == 0:
            print(f"- {i + 1}/{limit} packages processed")

    return pkgs

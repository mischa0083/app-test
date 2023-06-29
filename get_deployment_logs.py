# Import requests library
import requests

# Import datetime library
import datetime

# Railway GraphQL API URL
url = "https://backboard.railway.app/graphql/v2"

# Define a query
queryGetProjects = """
query getProjects{
  projects {
		edges {
          node {
            name
            id
            }
        }
    }
}
"""

# Get Railway API key from input
api_key = input("Enter a personal Railway API key: ")

# Define headers
headers = {
    "Content-Type": "application/json",

    # Railway API key
    "Authorization": "Bearer " + api_key
}

print("\nFetching Railway projects for this personal API key...")

# Make a POST request to Railway GraphQL API
response = requests.post(url, json={"query": queryGetProjects}, headers=headers)

# Parse response as JSON
response = response.json()

# print name, corresponding id, and status of each project deployment
print("\nPROJECTS:")
for project in response["data"]["projects"]["edges"]:
    print("  - " + project["node"]["name"] + " (id: " + project["node"]["id"] + ")")

# Input a project id
project_id = input("\nEnter the id of the project you want to check: ")

queryGetDeployments = """
query getDeployments{
    deployments(input: {projectId: "%s"}) {
        edges {
        node {
            staticUrl
            id
            status
            }
        }
    }
}
""" % project_id

# Make a POST request to Railway GraphQL API
response = requests.post(url, json={"query": queryGetDeployments}, headers=headers)

# Parse response as JSON
response = response.json()

# print name, corresponding id, and status of specified project deployment
print("\nDEPLOYMENTS:")
for deployment in response["data"]["deployments"]["edges"]:
    print("  - " + deployment["node"]["staticUrl"] + " (id: " + deployment["node"]["id"] + ")" + " - " + deployment["node"]["status"])

# Input a deployment id
deployment_id = input("\nEnter the id of the deployment you want to download logs: ")

# Define a query to get deployment logs using deployment id
queryGetDeploymentLogs = """
query {
  deploymentLogs(deploymentId: "%s") {
    timestamp
    severity
    message
  }
}
""" % deployment_id

# Make a POST request to Railway GraphQL API
response = requests.post(url, json={"query": queryGetDeploymentLogs}, headers=headers)

# Parse response as JSON
response = response.json()

# Pipe deployment logs to a file with deployment_id and current system time in UTC as filename
filename = deployment_id + "-" + datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S") + ".txt"

# Open file in write mode
f = open(filename, "w")

# Write deployment logs to file
for log in response["data"]["deploymentLogs"]:
    f.write(log["timestamp"] + " - " + log["severity"] + " - " + log["message"] + "\n")

# Close file
f.close()

# Print success message with filename
print("\nDeployment logs downloaded to " + filename)
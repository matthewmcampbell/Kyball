import os

def undeploy():
	os.system("terraform destroy -auto-approve")

if __name__ == "__main__":
	undeploy()
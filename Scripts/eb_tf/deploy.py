import os.path
import subprocess

def tf_output_get():
	if os.path.exists("./terraform.tfstate"):
		string = subprocess.check_output("terraform output")
		string = str(string)[2:-1]
		items_with_equals = string.split('\\n')[:-1]
		pairs = list(map(lambda x: x.split('='), items_with_equals))
		pairs = list(map(lambda x: [x[0].strip(), x[1].strip()], pairs))
		pairs_dict = dict(pairs)
		return pairs_dict

def aws_deploy_str(tf_dict, region = 'us-east-1'):
	return """aws --region {} elasticbeanstalk update-environment --environment-name {}	--version-label {}""".format(
		region, tf_dict['env_name'], tf_dict['app_version']
		)

def main():
	os.system("terraform init")
	os.system("terraform apply -auto-approve")
	tf_dict = tf_output_get()
	deploy_str = aws_deploy_str(tf_dict)
	# print(deploy_str)
	os.system(deploy_str)
	print("Django-app deploying... Please wait approx. 5-10 minutes for deployment to EC2 instance(s).")

if __name__ == '__main__':
	main()
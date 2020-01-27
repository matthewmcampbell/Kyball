Kyball Project

This project sets up a Django web application that allows users to query a database for baseball players.
The query should return nice visuals showing relevant stats of the player. The main triumph of this project,
however, is that all of the infrastructure is IaC: 'Infrastructure as Code'. 

What all happens?

Good question.

![Alt text](mysite/static/kyball/images/diagram_with_numbers.png?raw=true "Infrastructure")
1. Git pull from here.

2. Python script executes Terraform commands, e.g., "terraform init", "terraform apply", etc. This portion of the infrastructure is where the single, on-off command lies. A single shell command ("python deploy.py") will provision and connect all the necessary components henceforth. See the README in the git source if you'd like to explore doing this yourself.
        
3. Terraform config files provision an EC2 instance, RDS MySQL DB instance, Elastic Beanstalk environment/application, Route 53 records, and standard security-group/permissions fix-ins to minimize unneeded access to all resources.
        
4. EC2 instance uses bash scripts and <a href="https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html">user data</a> to write baseball data from csv files (contained in the git repo) to MySQL DB and then terminates. This is so you don't have to pay for the DB to keep it running all the time!
          
        
5. Once the Beanstalk environment and application are provisioned, a Python script communicates the CNAME of the environment (only available <i>after</i> provisioned) from Terraform to Django's settings.py file, dynamically updating the ALLOWED_HOSTS. See this <a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html#python-django-deploy">tutorial</a> to see what is being automated here.
          
        
6. The Plotly app within the Django framework establishes a connection to the RDS DB in a similar, dynamic way. A Python script communicates the address of the RDS instance to Plotly after it has been provisioned. This allows for the player querying in the app.
          
        
7. Lastly, the entire application becomes publicly accessible via Route 53 mapping the Elastic Beanstalk app to a fixed domain name via alias records. 
          

Requirements:<br />
	-AWS account with CLI setup<br />
	-Terraform properly installed<br />
	-Create a file in your Terraform dir "terraform.tfvars" with the contents:<br />
		user = "INSERT USERNAME HERE"<br />
		password = "INSERT PASSWORD HERE"<br />
	-Keep the quotes in the above.<br />


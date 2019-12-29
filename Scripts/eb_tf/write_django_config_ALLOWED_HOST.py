import sys

def write_for_django_config_ALLOWED_HOSTS(cname):
	file = open('../../mysite/mysite/django_cname.txt', 'w')
	file.write(cname)
	file.close()

def main(arg):
	write_for_django_config_ALLOWED_HOSTS(arg)	

if __name__ == '__main__':
	if len(sys.argv) < 2:
		raise ValueError("No shell arguements supplied. Cannot write to file.")
	main(sys.argv[1])
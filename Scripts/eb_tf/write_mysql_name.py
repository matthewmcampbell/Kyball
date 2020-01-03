import sys

def write_mysql_db_name(args):
	file = open('../../mysite/kyball/db_access_info.txt', 'w')
	print(args)
	for arg in args:
		file.write(str(arg)+'\n')
	file.close()

def main(args):
	write_mysql_db_name(args)
if __name__ == '__main__':
	if len(sys.argv) < 4:
		raise ValueError("No shell arguements supplied. Cannot write to file.")
	main(sys.argv[1:])
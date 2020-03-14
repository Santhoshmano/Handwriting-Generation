user = 'root' #your mysql user name
password = 'manosanthosh'  #your password
host = 'localhost'
database = 'handwriting' # give your db name

connector = 'mysql+mysqlconnector://%s:%s@%s/%s' % (user,password,host,database)
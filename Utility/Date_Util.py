from datetime import datetime

def get_date():
	return datetime.today().strftime("%Y-%m-%d %H:%M:%S")

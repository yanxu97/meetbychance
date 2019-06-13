import names
from datetime import date
from datetime import datetime
import random
import csv

 #   gender = (
 #        ('male', 'male'),
 #        ('female', 'female'),
 #    )
 #   user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
 #   org = models.CharField(
 #       'Organization', max_length=128, blank=True)
 #   telephone = models.CharField(
 #       'Telephone', max_length=50, blank=True)
 #   mod_date = models.DateTimeField('Last modified', auto_now=True)
 #   gender =  models.CharField(max_length=10,choices=gender,default='female')
 #   major = models.CharField(max_length=10)
 #   language = models.CharField(max_length=10)
 #   #photo = =
 #   email = models.EmailField(unique=True)
 #   age = models.CharField(max_length=10)
 #   interest = models.CharField(max_length=100)
 #   postion =  models.CharField(max_length=20)
 #   # newly added
 #   first_name = models.CharField(max_length=30)
 #   last_name = models.CharField(max_length=30)
 #   birthday = models._("Date"), auto_now_add = True)

today = datetime.today()
user = []
profile = []
for i in range(1, 100):
	profile = []

	user_id = i

	if i%2 == 0:
		first_name = names.get_first_name(gender='female')
		gender = 'female'
	if i%2 == 1:
		first_name = names.get_first_name(gender='male')
		gender = 'male'	
	last_name = names.get_last_name()

	a = random.randint(1990,2000)
	b = random.randint(1,12)
	if b == 2:
		c = random.randint(1,28)
	if b == 1 or b == 3 or b == 5 or b == 7 or b == 8 or b == 10 or b == 12:
		c = random.randint(1, 31)
	if b == 4 or b == 6 or b == 9 or b == 11:
		c = random.randint(1, 30)
	birthday = date(a, b, c)

	age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

	org = 'UIUC'

	profile.append(user_id)
	profile.append(first_name)
	profile.append(last_name)
	profile.append(gender)
	profile.append(birthday)
	profile.append(age)
	profile.append(org)


	user.append(profile)


# print(user)
attributes = ['user_id','first_name','last_name','gender','birthday','age','org']
with open('user.csv', mode='w') as user_file:
	writer = csv.writer(user_file)
	writer.writerow(attributes)
	for entries in user:
		writer.writerow(entries)

    

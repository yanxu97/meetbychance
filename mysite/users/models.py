from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):


   user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

   org = models.CharField(
       'Organization', max_length=128, blank=True)

   telephone = models.CharField(
       'Telephone', max_length=50, blank=True)

   mod_date = models.DateTimeField('Last modified', auto_now=True)


   class Meta:
       verbose_name = 'User Profile'

   def __str__(self):
        return "%s %s %s %s" % (self.user, self.org, self.telephone, self.mod_date)


class travel_Plan(models.Model):
    """ travel plan
    travelPlan(planID, country, city, budget, time, group size)
    """
    plan_id = models.AutoField(primary_key=True, verbose_name="plan_id")
    country=models.CharField('Country', max_length=128, blank=True)
    state=models.CharField('State', max_length=128, blank=True)
    city = models.CharField('City', max_length=128, blank=True)
    budget = models.IntegerField()
    start_time= models.DateField()
    end_time= models.DateField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='plan', null=True)
    status = models.CharField(max_length=10, default='unmatched', blank=False, null=False)


    class Meta:
        verbose_name = 'travel_Plan'
        unique_together = ('country', 'state', 'city', 'start_time', 'end_time', 'user')

    def __str__(self):
        result = []
        result.append(self.plan_id)
        result.append(self.country)
        result.append(self.state)
        result.append(self.city)
        result.append(self.budget)
        result.append(self.start_time)
        result.append(self.end_time)
        result.append(self.user)
        return str(result)

class match_list(models.Model):

   user_1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

   plan_id_1 = models.ForeignKey(travel_Plan, on_delete=models.CASCADE)

   user_2 = models.ForeignKey(UserProfile, related_name='%(class)s_requests_created', on_delete=models.CASCADE)

   plan_id_2 = models.ForeignKey(travel_Plan, related_name='%(class)s_requests_created', on_delete=models.CASCADE)

   status = models.CharField('status', max_length=10, blank=False, default='matched', null=False)

   class Meta:
       verbose_name = 'Match_List'
       abstract = False

   def __str__(self):
       result = []
       result.append(self.user_1)
       result.append(self.plan_id_1)
       result.append(self.user_2)
       result.append(self.plan_id_2)
       result.append(self.status)

       return str(result)


# class rating(match_list):
#
#     #
#     question1 = (
#         ('1', '1'),
#         ('2', '2'),
#         ('3', '3'),
#         ('4', '4'),
#         ('5', '5')
#     )
#
#     #
#     question2 = (
#         ('1', '1'),
#         ('2', '2'),
#         ('3', '3'),
#         ('4', '4'),
#         ('5', '5')
#     )
#
#     #
#     question3 = (
#         ('1', '1'),
#         ('2', '2'),
#         ('3', '3'),
#         ('4', '4'),
#         ('5', '5')
#     )
#
#     # blocked_users ?????
#
#     class Meta:
#         verbose_name = 'Rating'
#
#     def __str__(self):
#         return "%s %s %s" % (self.question1, self.question2, self.question3)

# class block_list():
#
#     # should we use foreign keys here?
#     #blocker_id =
#     #blocked_id =
#
#     class Meta:
#         verbose_name = 'Block_list'
#
#     def __str__(self):
#         return

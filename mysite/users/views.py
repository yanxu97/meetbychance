from django.shortcuts import render, get_object_or_404,render_to_response
from django.contrib.auth.models import User
from .models import UserProfile,travel_Plan, match_list
from django.contrib import auth
from .forms import RegistrationForm, LoginForm,ProfileForm,PwdChangeForm,post_plan_Form
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.http import Http404
import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Count
from django.db import connection
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.db.models import Count, Q

import json
import pandas as pd
import os





# Create your views here.

def register(request):
    if request.method == 'POST':

        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']


            user = User.objects.create_user(username=username, password=password, email=email)


            user_profile = UserProfile(user=user)
            user_profile.save()

            return HttpResponseRedirect("/accounts/login/")

    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
               auth.login(request, user)
               me=User(username=username)
               my_profile=UserProfile(user=me)
               myplan=travel_Plan(user=my_profile)
               if myplan.status=='matched':
                  pass

               return HttpResponseRedirect(reverse('users:home'))

            else:

                 return render(request, 'login.html', {'form': form,
                               'message': 'Wrong password. Please try again.'})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/login/")



@login_required
def profile(request, pk):
   user = get_object_or_404(User, pk=pk)
   return render(request, 'profile.html', {'user': user})

@login_required
def profile_update(request, pk):
   user = get_object_or_404(User, pk=pk)
   user_profile = get_object_or_404(UserProfile, user=user)

   if request.method == "POST":
       form = ProfileForm(request.POST)

       if form.is_valid():
           user.first_name = form.cleaned_data['first_name']
           user.last_name = form.cleaned_data['last_name']
           user.save()

           user_profile.org = form.cleaned_data['org']
           user_profile.telephone = form.cleaned_data['telephone']
           user_profile.save()

           return HttpResponseRedirect(reverse('users:profile', args=[user.id]))
   else:
       default_data = {'first_name': user.first_name, 'last_name': user.last_name,
                        'org': user_profile.org, 'telephone': user_profile.telephone, }
       form = ProfileForm(default_data)

   return render(request, 'profile_update.html', {'form': form, 'user': user})


@login_required
def pwd_change(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        form = PwdChangeForm(request.POST)

        if form.is_valid():

            password = form.cleaned_data['old_password']
            username = user.username

            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                new_password = form.cleaned_data['password2']
                user.set_password(new_password)
                user.save()
                return HttpResponseRedirect("/accounts/login/")

            else:
                return render(request, 'pwd_change.html', {'form': form,
                                                                 'user': user,
                                                                 'message': 'Old password is wrong. Try again'})
    else:
        form = PwdChangeForm()

    return render(request, 'pwd_change.html', {'form': form, 'user': user})


@login_required
def post_plan(request, pk):
    # user_profile = get_object_or_404(UserProfile, pk=pk)
    # user = get_object_or_404(User, pk=pk)
    # travel_plan = get_object_or_404(travel_Plan,user=user)
    if request.method == 'POST':
        form = post_plan_Form(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=pk)
            user_profile = UserProfile.objects.get(user=user)
            country = form.cleaned_data['country']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            budget = form.cleaned_data['budget']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            travel_plan = travel_Plan(user=user_profile, country=country, state=state, city=city, budget=budget,
                                      start_time=start_time, end_time=end_time)
            print(user_profile.user_id)
            try:
                print(travel_plan)
                travel_plan.save()
                # planid=travel_plan.plan_id
                # print(planid)
                myplan = travel_Plan.objects.raw(
                    '''SELECT * FROM users_travel_Plan WHERE user_id=%s ORDER BY plan_id DESC''', [user_profile.id])
                # return render(request, 'plan_list.html', {'travel_plan': travel_plan})
                # myplan = travel_Plan.objects.raw('''SELECT * FROM users_travel_Plan WHERE user_id=%s AND plan_id=%s ''', [user_profile.id,planid])
                print("test")
                print(travel_plan.plan_id)

                matched_plan = match_helper(user_profile.id, travel_plan.plan_id, -1)
                print(travel_plan.user)
                if matched_plan is not None:
                    match_list1 = match_list(user_1_id=travel_plan.user_id, plan_id_1_id=travel_plan.plan_id,
                                             user_2_id=matched_plan.user_id, plan_id_2_id=matched_plan.plan_id)
                    match_list2 = match_list(user_1_id=matched_plan.user_id, plan_id_1_id=matched_plan.plan_id,
                                             user_2_id=travel_plan.user_id, plan_id_2_id=travel_plan.plan_id)
                    match_list1.save()
                    match_list2.save()
                    plan_active = travel_Plan.objects.get(user=travel_plan.user, plan_id=travel_plan.plan_id)
                    plan_active.status = 'matched'
                    plan_active.save()
                    plan_passive = travel_Plan.objects.get(user=matched_plan.user, plan_id=matched_plan.plan_id)
                    plan_passive.status = 'matched'
                    plan_passive.save()

                # myplan = travel_Plan.objects.raw('''SELECT * FROM users_travel_Plan WHERE user_id=%s AND plan_id=%s ''', [user_profile.id,planid])
                return render(request, 'plan_list.html', {'plan_list': myplan})
                # return render(request, 'plan_detail.html', {'plan_list': myplan})
            except IntegrityError as e:
                # duplicate happens
                e = 'this data already exists in the database'
                return HttpResponse(e)
                # return render(request, 'post_plan.html', context={ 'form': form, 'e': e})
    else:
        form = post_plan_Form()
        # return render(request, 'post_plan.html', {'form':form,'travel_plan':travel_plan })
        return render(request, 'post_plan.html', {'form': form})

"""
@login_required
def plan(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = UserProfile.objects.get(user=user)

    try:
        # myplan = travel_Plan.objects.filter(user=user_profile).order_by('plan_id').last()
        myplan = travel_Plan.objects.raw('''SELECT * FROM users_travel_Plan WHERE user_id=%s''', [user_profile.id])
    except (travel_Plan.DoesNotExist):
        myplan = travel_Plan()
    return render(request, 'plan_list.html', {'travel_plan': myplan})
"""
#  -------------------------------------------------------------------------------------------------------------


@login_required
def plan_list(request,pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = UserProfile.objects.get(user=user)
    try:
        myplan = travel_Plan.objects.filter(user=user_profile)
        # myplan = travel_Plan.objects.raw('''SELECT * FROM users_travel_Plan WHERE user_id=%s ORDER BY plan_id''', [user_profile.id])
    except (travel_Plan.DoesNotExist):
        myplan = None
    print(user_profile.id)
    print(user.id)
    if str(myplan) == '<QuerySet []>':
        myplan = ''
    return render(request, 'plan_list.html', {'plan_list': myplan})

@login_required
def plan_detail(request,pk,planpk):
    user = get_object_or_404(User, pk=pk)
    user_profile = UserProfile.objects.get(user=user)
    myplan=travel_Plan.objects.get(user=user_profile,pk=planpk)
    #myplan = travel_Plan.objects.raw('''SELECT * FROM users_travel_Plan WHERE plan_id=%s AND user_id=%s''', [planpk,user_profile.id])
    print(planpk)
    print(user_profile.id)
    print(user.id)
    return render(request, 'plan_detail.html', {'myplan': myplan})

@login_required
def plan_update(request,pk,planpk):
    user = get_object_or_404(User, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=user)
    myplan = travel_Plan.objects.get(user=user_profile, pk=planpk)
    if request.method == 'POST':
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        budget = request.POST.get('budget')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        myplan.country=country
        myplan.state=state
        myplan.city=city
        myplan.budget=budget
        myplan.start_time=start_time
        myplan.end_time = end_time
        myplan.save()
        print("user_profile.id", user_profile.id)
        print("myplan.plan_id", myplan.plan_id)
        matched_plan = match_helper(user_profile.id, myplan.plan_id, -1)
        print("matched_plan", matched_plan)
        if matched_plan is not None:
            print("matched_plan is not None")
            match_list1 = match_list(user_1_id=myplan.user_id, plan_id_1_id=myplan.plan_id, user_2_id=matched_plan.user_id,
                                     plan_id_2_id=matched_plan.plan_id)
            match_list2 = match_list(user_1_id=matched_plan.user_id, plan_id_1_id=matched_plan.plan_id, user_2_id=myplan.user_id,
                                     plan_id_2_id=myplan.plan_id)
            match_list1.save()
            match_list2.save()
            plan_active = travel_Plan.objects.get(user=myplan.user, plan_id=myplan.plan_id)
            print("plan_active", plan_active)
            plan_active.status = 'matched'
            plan_active.save()
            plan_passive = travel_Plan.objects.get(user=matched_plan.user, plan_id=matched_plan.plan_id)
            plan_passive.status = 'matched'
            print("plan_passive", plan_passive)
            plan_passive.save()

        return render(request, 'plan_detail.html', {'myplan': myplan})

def match_helper(user_1,plan_1,limit):
    myplan1=travel_Plan.objects.get(user=user_1,plan_id=plan_1)
    try:
        travel_plan_1 = travel_Plan.objects.raw(
            '''SELECT * FROM users_travel_Plan WHERE country=%s AND state=%s AND city=%s AND budget>=%s AND budget<=%s AND start_time=%s AND end_time=%s AND user_id <> %s AND plan_id>%s AND status=%s ORDER BY plan_id ASC''',
            [myplan1.country, myplan1.state, myplan1.city, myplan1.budget*0.8, myplan1.budget*1.2,
             myplan1.start_time, myplan1.end_time, user_1, limit, 'unmatched'])[0]
    except IndexError:
        travel_plan_1 = None

    return travel_plan_1


@login_required
def plan_delete(request,pk,planpk):

    user = get_object_or_404(User, pk=pk)
    user_profile = UserProfile.objects.get(user=user)
    myplan = None
    try:
        delete_travel_plan = travel_Plan.objects.filter(pk=planpk)[0]
    except:
        print("first")
        myplan = travel_Plan.objects.raw('''SELECT * FROM users_travel_Plan WHERE user_id=%s''', [user_profile.id])
        return render(request, 'plan_list.html', {'plan_list': myplan})
    a = user_profile.id
    b = delete_travel_plan.plan_id
    print("a", a)
    print("b", b)
    try:
        print("did not pass the try")
        delete_match_list_plan = match_list.objects.raw('''SELECT * FROM users_match_list WHERE user_1_id=%s AND plan_id_1_id=%s''', [a, b])[0]
        print("delete_match_list_plan",delete_match_list_plan)
        delete_match_list_plan_partner = match_list.objects.raw('''SELECT * FROM users_match_list WHERE user_1_id=%s AND plan_id_1_id=%s''', [delete_match_list_plan.user_2_id, delete_match_list_plan.plan_id_2_id])[0]
        print("delete_match_list_plan_partner", delete_match_list_plan_partner)
    except:
        delete_travel_plan.delete()
        myplan = travel_Plan.objects.raw('''SELECT * FROM users_travel_Plan WHERE user_id=%s''', [user_profile.id])
        # travel_plan_partner = travel_Plan.objects.filter(plan_id=delete_match_list_plan_partner.plan_id_1_id)[0]
        # travel_plan_partner.status = 'unmatched'
        # travel_plan_partner.save()
        print("second")
        return render(request, 'plan_list.html', {'plan_list': myplan})

    delete_travel_plan.delete()

    # print("delete_match_list_plan.user_2_id", delete_match_list_plan.user_2_id)
    # print("delete_match_list_plan.plan_id_2_id", delete_match_list_plan.plan_id_2_id)
    # myplan_partner = travel_Plan.objects.raw('''SELECT * FROM users_travel_Plan WHERE user_id=%s AND plan_id=%s''', [delete_match_list_plan.user_2_id, delete_match_list_plan.plan_id_2_id])[0]
    # myplan_partner.status = 'unmatched'
    # print("myplan_partner", myplan_partner)
    # myplan_partner.save()

    delete_match_list_plan.delete()

    print("delete_match_list_plan_partner.user_1_id", delete_match_list_plan_partner.user_1_id)
    newmatch = match_helper(delete_match_list_plan_partner.user_1_id, delete_match_list_plan_partner.plan_id_1_id, -1)
    print("newmatch", newmatch)

    if newmatch is not None:
        newmatch.status = 'matched'
        newmatch.save()
        print("delete_match_list_plan_partner", delete_match_list_plan_partner)
        delete_match_list_plan_partner.status = 'matched'
        delete_match_list_plan_partner.user_2_id = newmatch.user_id
        delete_match_list_plan_partner.plan_id_2_id = newmatch.plan_id
        delete_match_list_plan_partner.save()

        new_partner = match_list(user_1_id=newmatch.user_id, plan_id_1_id=newmatch.plan_id, user_2_id=delete_match_list_plan_partner.user_1_id,
                                 plan_id_2_id=delete_match_list_plan_partner.plan_id_1_id)
        print("new partner", new_partner)
        #new_partner.save()
        new_partner.status = 'matched'
        new_partner.save()
        print("new match is not NONE")
    else:
        print("new match is none")
        delete_match_list_plan_partner.delete()
        travel_plan_partner = travel_Plan.objects.filter(plan_id=delete_match_list_plan_partner.plan_id_1_id)[0]
        print("delete", travel_plan_partner)
        travel_plan_partner.status = 'unmatched'
        travel_plan_partner.save()

    myplan=travel_Plan.objects.raw('''SELECT * FROM users_travel_Plan WHERE user_id=%s''',[ user_profile.id])
    print("third")
    return render(request, 'plan_list.html', {'plan_list': myplan})



"""
@login_required
def delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = UserProfile.objects.get(user=user)
    try:
        myplan = travel_Plan.objects.filter(user=user_profile).order_by('plan_id').last()
        myplan.delete()
    except (travel_Plan.DoesNotExist, AttributeError):
        myplan = None
        return render(request, 'delete.html', {'travel_plan': myplan})

    try:
        nextplan = travel_Plan.objects.filter(user=user_profile).order_by('plan_id').last()
    except (travel_Plan.DoesNotExist):
        nextplan = None
    return render(request, 'delete.html', {'travel_plan': nextplan})
"""

@login_required
def matched_list(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = UserProfile.objects.get(user=user)
    try:
        myplan_1 = travel_Plan.objects.filter(user=user_profile).order_by('plan_id')[0]#.last()
    except:
        myplan_1 = None

    print(myplan_1)

    try:
        myplan_2 = travel_Plan.objects.filter(user=user_profile).order_by('plan_id')[1]#.last()
    except:
        myplan_2 = None

    print(myplan_2)

    try:
        myplan_3 = travel_Plan.objects.filter(user=user_profile).order_by('plan_id')[2]#.last()
    except:
        myplan_3 = None
    if myplan_1 == None and myplan_2 == None and myplan_3 == None:
        return render(request, 'matched_list.html', {'travel_plan_1': myplan_1, 'travel_plan_2': myplan_2, 'travel_plan_3': myplan_3})

    print(myplan_3)

    '''
    country = models.CharField('Country', max_length=128, blank=True)
    state = models.CharField('State', max_length=128, blank=True)
    city = models.CharField('City', max_length=128, blank=True)
    budget = models.IntegerField()
    start_time = models.DateField()
    end_time = models.DateField()
    '''
    my_id = user_profile.id

    # myplan_1
    matched_plan_1 = None
    matched_user2_1 = None
    matched_plan2_1 = None
    partner_matchList_1 = None
    if myplan_1 != None and myplan_1.status == 'matched':
        try:
            matched_plan_1 = match_list.objects.filter(plan_id_1_id=myplan_1.plan_id).order_by('id')[0]
            print(matched_plan_1)
            matched_user2_1 = UserProfile.objects.get(id=matched_plan_1.user_2_id)
            matched_user2_1 = User.objects.get(id=matched_user2_1.user_id)
            matched_plan2_1 = travel_Plan.objects.get(plan_id=matched_plan_1.plan_id_2_id)
            partner_matchList_1 = match_list.objects.get(plan_id_1=matched_plan2_1.plan_id)

        except IndexError:
            matched_plan_1 = None
            matched_user2_1 = None
            matched_plan2_1 = None
            partner_matchList_1=None

    print("matched_user2_1", matched_user2_1)
    print("matched_plan2_1", matched_plan2_1)

    # myplan_2
    matched_plan_2 = None
    matched_user2_2 = None
    matched_plan2_2 = None
    partner_matchList_2 = None
    if myplan_2 != None and myplan_2.status == 'matched':
        try:
            matched_plan_2 = match_list.objects.filter(plan_id_1_id=myplan_2.plan_id).order_by('id')[0]
            matched_user2_2 = UserProfile.objects.get(id=matched_plan_2.user_2_id)
            matched_user2_2 = User.objects.get(id=matched_user2_2.user_id)
            matched_plan2_2 = travel_Plan.objects.get(plan_id=matched_plan_2.plan_id_2_id)
            partner_matchList_2 = match_list.objects.get(plan_id_1=matched_plan2_2.plan_id)

        except IndexError:
            matched_plan_2 = None
            matched_user2_2 = None
            matched_plan2_2 = None
            partner_matchList_2=None

    # myplan_1
    matched_plan_3 = None
    matched_user2_3 = None
    matched_plan2_3 = None
    partner_matchList_3 = None
    if myplan_3 != None and myplan_3.status == 'matched':
        try:
            matched_plan_3 = match_list.objects.filter(plan_id_1_id=myplan_3.plan_id).order_by('id')[0]
            print(matched_plan_3)
            matched_user2_3 = UserProfile.objects.get(id=matched_plan_3.user_2_id)
            matched_user2_3 = User.objects.get(id=matched_user2_3.user_id)
            matched_plan2_3 = travel_Plan.objects.get(plan_id=matched_plan_3.plan_id_2_id)
            partner_matchList_3 = match_list.objects.get(plan_id_1=matched_plan2_3.plan_id)

        except IndexError:
            matched_plan_3 = None
            matched_user2_3 = None
            matched_plan2_3 = None
            partner_matchList_3=None

    return render(request, 'matched_list.html',
                  {'matched_user2_1': matched_user2_1, 'matched_user2_2': matched_user2_2,
                   'matched_user2_3': matched_user2_3,
                   'matched_plan2_1': matched_plan2_1, 'matched_plan2_2': matched_plan2_2,
                   'matched_plan2_3': matched_plan2_3,
                   'myplan_1': myplan_1, 'myplan_2': myplan_2, 'myplan_3': myplan_3,
                   'matched_plan_1': matched_plan_1, 'matched_plan_2': matched_plan_2, 'matched_plan_3': matched_plan_3,
                   'partner_matchList_1':partner_matchList_1,'partner_matchList_2':partner_matchList_2,'partner_matchList_3':partner_matchList_3,
                   })

@login_required
def topone(request, pk):
    #top_record = travel_Plan.objects.annotate(c=Count('country')).order_by('-c')[0]
    top_city = travel_Plan.objects.values_list('city').annotate(city_count=Count('city')).order_by('-city_count')[0][0]
    print(top_city)
    try:
        top_record = travel_Plan.objects.raw('''SELECT * FROM users_travel_Plan WHERE city=%s''', [top_city])[0]
    except IndexError:
        top_record = None

    return render(request, 'whatishot.html', {'top_record': top_record})

# search_result
@login_required
def search(request):
    return render(request,'search.html')


def search_detail(request):

     if request.method == 'POST':
         country_1 = request.POST.get('country_1')
         state_1 = request.POST.get('state_1')
         city_1 = request.POST.get('city_1')
         country_2 = request.POST.get('country_2')
         state_2 = request.POST.get('state_2')
         city_2 = request.POST.get('city_2')


         search_result=travel_Plan.objects.raw('''SELECT * FROM users_travel_Plan WHERE country=%s AND state=%s AND city=%s UNION
         SELECT * FROM users_travel_Plan WHERE country=%s AND state=%s AND city=%s''',[country_1,state_1,city_1,country_2,state_2,city_2])

         #search_result=travel_Plan.objects.raw('''SELECT * FROM users_travel_Plan''')
         print(country_1, state_1)
         print(search_result)
         return render(request, 'search_detail.html', {'search_result': search_result})

@login_required
def plan_up(request,pk,planpk):
    user = get_object_or_404(User, pk=pk)
    user_profile = UserProfile.objects.get(user=user)
    myplan = travel_Plan.objects.get(user=user_profile, pk=planpk)
    return render(request,'plan_update.html',{'myplan': myplan})


# hotbytime_result
@login_required
def hotbybudget(request):
    if request.method == 'POST':
        budget_low_limit = request.POST.get('budget_low_limit')
        budget_high_limit = request.POST.get('budget_high_limit')
        # '''SELECT COUNT(plan_id), DATE_TRUNC('month',start_time) FROM users_travel_Plan GROUP BY DATE_TRUNC('month',start_time)'''
        # whatishot_result = travel_Plan.objects.raw('''SELECT plan_id, start_time FROM users_travel_Plan GROUP''')
        cursor = connection.cursor()
        cursor.execute("""select 
                                city, country, m, sum(c)/2 as s
                           from  
                           (select 
                               city, country, strftime('%%m', start_time) as m, count(*) as c, "start" as t
                           from 
                               users_travel_Plan
                           where
                               budget > %s and budget < %s
                           group by
                                m, city, country       
                           union 
                           select 
                               city, country, strftime('%%m', start_time) as m, count(*) as c, "start" as t
                           from 
                               users_travel_Plan
                           where
                               budget > %s and budget < %s
                           group by
                                m, city, country) as temp
                           group by 
                                m, city, country  
                           order by
                                s DESC
                           LIMIT 5; """, [budget_low_limit, budget_high_limit, budget_low_limit, budget_high_limit])
        whatishot_result = cursor.fetchall()
        for i in whatishot_result:
            print(i)

        return render(request, 'whatishot.html', {'whatishot_result': whatishot_result})

    '''
        cursor.execute("""select 
                              city, country, strftime('%%m', start_time), count(*), "start"
                          from 
                              users_travel_Plan
                          where
                              budget > %s and budget < %s
                          group by
                               strftime('%%m', start_time), city, country 
                          order by
                               count(*) DESC
                          LIMIT 10; """, [budget_low_limit, budget_high_limit] )

    '''

@login_required
def confirm(request,pk,myPlanPK):
    print(pk)

    user_profile=UserProfile.objects.get(user_id=pk)
    print(user_profile.id)
    try:
       myplan = match_list.objects.filter(plan_id_1_id=myPlanPK)[0]
       myplan.status='confirmed'
       print("my plan", myplan)
       myplan.save()
    except IndexError:
       pass
    return render(request, 'confirmed_text.html' )



@login_required
def reject(request,pk,myPlanPK):


    print("test1",myPlanPK)
    user_profileA=UserProfile.objects.get(user_id=pk)
    print("reject", user_profileA.id)
    try:
        planA=match_list.objects.filter(plan_id_1_id=myPlanPK)[0]
        print("plan_a",planA)

        planB=match_list.objects.filter(plan_id_2_id=myPlanPK)[0]
        print("plan_b", planB)


        print("test", planB.user_1_id)
        B_id=planA.user_2_id
        Bplan_id=planA.plan_id_2_id

        A_id=planA.user_1_id
        Aplan_id=planA.plan_id_1_id

        planA.delete()
        planB.delete()

        Bmatch=match_helper(B_id,Bplan_id,Aplan_id)
        if Bmatch is not None:
            Bmatchlist1=match_list(user_1_id=B_id,plan_id_1_id=Bplan_id,user_2_id=Bmatch.user_id,plan_id_2_id=Bmatch.plan_id)
            Bmatchlist2=match_list(user_2_id=B_id,plan_id_2_id=Bplan_id,user_1_id=Bmatch.user_id,plan_id_1_id=Bmatch.plan_id)

            Bmatchlist1.save()
            Bmatchlist2.save()
            Bmatchplan=travel_Plan.objects.get(plan_id=Bmatch.plan_id)
            Bmatchplan.status='matched'
            Bmatchplan.save()
        else:
            Bplan=travel_Plan.objects.get(plan_id=Bplan_id)
            Bplan.status='unmatched'
            Bplan.save()
        print('hahahha')
        Amatch=match_helper(A_id, Aplan_id, Bplan_id)
        if Amatch is not None:
            print("is not none")
            Amatchlist1=match_list(user_1_id=A_id,plan_id_1_id=Aplan_id,user_2_id=Amatch.user_id,plan_id_2_id=Amatch.plan_id)
            Amatchlist2=match_list(user_2_id=A_id,plan_id_2_id=Aplan_id,user_1_id=Amatch.user_id,plan_id_1_id=Amatch.plan_id)

            Amatchlist1.save()
            Amatchlist2.save()
            Amatchplan=travel_Plan.objects.get(plan_id=Amatch.plan_id)
            Amatchplan.status='matched'
            Amatchplan.save()
        else:
            print("is none")
            Aplan=travel_Plan.objects.get(plan_id=myPlanPK)
            Aplan.status='unmatched'
            Aplan.save()
    except IndexError:
        pass
    return render(request,"reject_text.html")

def confirm_1(request,pk,myPlanPK):
    print(pk)

    user_profile=UserProfile.objects.get(user_id=pk)
    print(user_profile.id)
    try:
       myplan = match_list.objects.filter(plan_id_1_id=myPlanPK)[0]
       myplan.status='confirmed'
       print("my plan", myplan)
       myplan.save()
    except IndexError:
       pass
    return render(request, 'confirmed_text.html' )



@login_required
def reject_1(request,pk,myPlanPK):


    print("test1",myPlanPK)
    user_profileA=UserProfile.objects.get(user_id=pk)
    print("reject", user_profileA.id)
    try:
        planA=match_list.objects.filter(plan_id_1_id=myPlanPK)[0]
        print("plan_a",planA)

        planB=match_list.objects.filter(plan_id_2_id=myPlanPK)[0]
        print("plan_b", planB)


        print("test", planB.user_1_id)
        B_id=planA.user_2_id
        Bplan_id=planA.plan_id_2_id

        A_id=planA.user_1_id
        Aplan_id=planA.plan_id_1_id

        planA.delete()
        planB.delete()

        Bmatch=match_helper(B_id,Bplan_id,Aplan_id)
        if Bmatch is not None:
            Bmatchlist1=match_list(user_1_id=B_id,plan_id_1_id=Bplan_id,user_2_id=Bmatch.user_id,plan_id_2_id=Bmatch.plan_id)
            Bmatchlist2=match_list(user_2_id=B_id,plan_id_2_id=Bplan_id,user_1_id=Bmatch.user_id,plan_id_1_id=Bmatch.plan_id)

            Bmatchlist1.save()
            Bmatchlist2.save()
            Bmatchplan=travel_Plan.objects.get(plan_id=Bmatch.plan_id)
            Bmatchplan.status='matched'
            Bmatchplan.save()
        else:
            Bplan=travel_Plan.objects.get(plan_id=Bplan_id)
            Bplan.status='unmatched'
            Bplan.save()
        print('hahahha')
        Amatch=match_helper(A_id, Aplan_id, Bplan_id)
        if Amatch is not None:
            print("is not none")
            Amatchlist1=match_list(user_1_id=A_id,plan_id_1_id=Aplan_id,user_2_id=Amatch.user_id,plan_id_2_id=Amatch.plan_id)
            Amatchlist2=match_list(user_2_id=A_id,plan_id_2_id=Aplan_id,user_1_id=Amatch.user_id,plan_id_1_id=Amatch.plan_id)

            Amatchlist1.save()
            Amatchlist2.save()
            Amatchplan=travel_Plan.objects.get(plan_id=Amatch.plan_id)
            Amatchplan.status='matched'
            Amatchplan.save()
        else:
            print("is none")
            Aplan=travel_Plan.objects.get(plan_id=myPlanPK)
            Aplan.status='unmatched'
            Aplan.save()
    except IndexError:
        pass
    return render(request,"reject_text.html")


@login_required
def confirm_2(request,pk,myPlanPK):
    print(pk)

    user_profile=UserProfile.objects.get(user_id=pk)
    print(user_profile.id)
    try:
       myplan=match_list.objects.filter(plan_id_1_id=myPlanPK)[0]
       myplan.status='confirmed'
       print("my plan", myplan)
       myplan.save()
    except IndexError:
       pass
    return render(request, 'confirmed_text.html' )


@login_required
def reject_2(request,pk,myPlanPK):


    print("test1",myPlanPK)
    user_profileA=UserProfile.objects.get(user_id=pk)
    print("reject", user_profileA.id)
    try:
        planA=match_list.objects.filter(plan_id_1_id=myPlanPK)[0]
        print("plan_a",planA)

        planB=match_list.objects.filter(plan_id_2_id=myPlanPK)[0]
        print("plan_b", planB)


        print("test", planB.user_1_id)
        B_id=planA.user_2_id
        Bplan_id=planA.plan_id_2_id

        A_id=planA.user_1_id
        Aplan_id=planA.plan_id_1_id

        planA.delete()
        planB.delete()

        Bmatch=match_helper(B_id,Bplan_id,Aplan_id)
        if Bmatch is not None:
            Bmatchlist1=match_list(user_1_id=B_id,plan_id_1_id=Bplan_id,user_2_id=Bmatch.user_id,plan_id_2_id=Bmatch.plan_id)
            Bmatchlist2=match_list(user_2_id=B_id,plan_id_2_id=Bplan_id,user_1_id=Bmatch.user_id,plan_id_1_id=Bmatch.plan_id)

            Bmatchlist1.save()
            Bmatchlist2.save()
            Bmatchplan=travel_Plan.objects.get(plan_id=Bmatch.plan_id)
            Bmatchplan.status='matched'
            Bmatchplan.save()
        else:
            Bplan=travel_Plan.objects.get(plan_id=Bplan_id)
            Bplan.status='unmatched'
            Bplan.save()
        print('hahahha')
        Amatch=match_helper(A_id, Aplan_id, Bplan_id)
        if Amatch is not None:
            print("is not none")
            Amatchlist1=match_list(user_1_id=A_id,plan_id_1_id=Aplan_id,user_2_id=Amatch.user_id,plan_id_2_id=Amatch.plan_id)
            Amatchlist2=match_list(user_2_id=A_id,plan_id_2_id=Aplan_id,user_1_id=Amatch.user_id,plan_id_1_id=Amatch.plan_id)

            Amatchlist1.save()
            Amatchlist2.save()
            Amatchplan=travel_Plan.objects.get(plan_id=Amatch.plan_id)
            Amatchplan.status='matched'
            Amatchplan.save()
        else:
            print("is none")
            Aplan=travel_Plan.objects.get(plan_id=myPlanPK)
            Aplan.status='unmatched'
            Aplan.save()
    except IndexError:
        pass
    return render(request,"reject_text.html")

@login_required
def notification(request,pk):

    userprofile=UserProfile.objects.get(user_id=pk)

    try:

        plans=travel_Plan.objects.filter(user_id=userprofile.id)
    except:
        plans=None

    status=0
    if plans is not None:
        for plan in plans:
            if plan.status=="matched":
               status=1
               print("tttttt")
               print(status)
               break
            else:
                status=0
    return render(request, 'base2.html', {'status': status})





def home(request):

    return render(request, 'home.html')

def homeLogin(request):

    return render(request, 'homeLogin.html')


def chart(request,pk):
    dataset = travel_Plan.objects.values('city').order_by('city').annotate(count=Count('city'))

    return render(request, 'chart.html', {'dataset': dataset})


def serve(request):
    print("t1")
    cursor = connection.cursor()
    cursor.execute("""select 
                            city, country, budget
                       from 
                           users_travel_Plan""")
    whatishot_result = cursor.fetchall()
    print("t2")
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path0 = os.path.join(BASE_DIR, 'static', 'files', 'destloc_tab.csv')
    path = os.path.join(BASE_DIR, 'static', 'files', 'planAndCoordstest.json')
    # Load in a csv file for known cities' coordinates

    destloc_tab = pd.read_csv(path0)
    print("t3")
    latCoord = list()
    lonCoord = list()

    num_sim = len(whatishot_result)
    print(num_sim)
    print("t4")
    for i in range(num_sim):

        if whatishot_result[i][0] == '?esk? Krumlov':
            latCoord.append('48.8127')
            lonCoord.append('14.3175')
        else:
            findMe = destloc_tab.loc[(destloc_tab['Country'] == whatishot_result[i][1])
                                     & (destloc_tab['City'] == whatishot_result[i][0]),]
            latCoord.append(findMe['latCoord'])
            lonCoord.append(findMe['lonCoord'])
        # print(i)

    jsonfile = open(path, 'w')
    model_name = "users.travel_plan_and_coordinates"
    jsonfile.write(
        r'{ "type": "FeatureCollection", "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } } ,"features":')
    jsonfile.write('\n')
    jsonfile.write('[ \n')
    i = 0
    for row in whatishot_result:
        # print((i, lonCoord[i], latCoord[i], whatishot_result[i][1], whatishot_result[i][0]))
        if len(lonCoord[i]) != 0:
            if i not in [0]:
                jsonfile.write(',')
            #
            todump = {"type": "Feature",
                      "properties": {"id": i, "rate": int(row[2])},
                      "geometry": {"type": "Point",
                                   "coordinates": [float(lonCoord[i]), float(latCoord[i]), 0.0]}}
            jsonfile.write('\n')
            json.dump(todump, jsonfile)
            i = i + 1
    print("t5")
    jsonfile.write('\n   ] }')
    jsonfile.write('\n')
    jsonfile.write('\n')
    jsonfile.write('\n')
    jsonfile.close()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, 'static', 'files', 'planAndCoordstest.json')
    print(path)
    with open(path, 'r', encoding='utf-8') as myfile:
        data = myfile.read()

    print(data)
    response = HttpResponse(content=data)
    response['Content-Type'] = 'application/json'
    print("t6")
    return response


def map(request):
    return render(request, 'map.html')




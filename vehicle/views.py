from django.shortcuts import render

# Create your views here.
from django.db import models

# Create your models here.
GAMES = (
    ('NOT_STARTED', 'NOT_STARTED'),
    ('QUARTER1', 'QUARTER1'),
    ('QUARTER2', 'QUARTER2'),
    ('QUARTER3', 'QUARTER3'),
    ('QUARTER4', 'QUARTER4'),
    ('SUSPENDED', 'SUSPENDED'),
    ('POINTSDISTRIBUTED', 'POINTSDISTRIBUTED'),
    ('OVERTIME', 'OVERTIME'),
    ('BREAKTIME', 'BREAKTIME'),
    ('HALFTIME', 'HALFTIME'),
    ('COMPLETED', 'COMPLETED'),
    ('AFTEROVERTIME', 'AFTEROVERTIME'),
    ('POSTPONED', 'POSTPONED'),
    ('CANCELLED', 'CANCELLED'),
)
class basketCountriesModel(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    flag = models.FileField(upload_to=None)
    date_created = models.DateTimeField(auto_now_add=True)

class basketSeasonModel(models.Model):
    date = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)

class basketLeagueSeasonModel(models.Model):
    season = models.ForeignKey(basketSeasonModel,null=True, on_delete=models.CASCADE, related_name='basketLeagueSeasonModel_season')
    start_date = models.DateField()
    end_date = models.DateField()

class basketLeagueModel(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    logo = models.FileField(upload_to=None)
    country = models.ForeignKey(basketCountriesModel,null=True, on_delete=models.CASCADE, related_name='basketLeagueModel_country')
    season = models.ManyToManyField(basketLeagueSeasonModel,related_name='basketLeagueModel_season')


class basketTeamsModel(models.Model):
    name = models.CharField(max_length=100)
    national = models.BooleanField(null=True, blank=True)
    logo = models.FileField(upload_to=None)
    country = models.ForeignKey(basketCountriesModel,null=True, on_delete=models.CASCADE, related_name='basketTeamsModel_country')


class basketGamesModel(models.Model):
    date = models.DateField()
    time = models.TimeField()
    timestamp = models.CharField(max_length=100)
    timezone = models.CharField(max_length=100)
    status =models.CharField(max_length=100, choices=GAMES)
    league = models.ForeignKey(basketLeagueModel,null=True, on_delete=models.CASCADE, related_name = 'basketGamesModel_league')
    country = models.ForeignKey(basketCountriesModel,null=True, on_delete=models.CASCADE, related_name='basketGamesModel_country')
    home_team = models.ForeignKey(basketTeamsModel, null=True,on_delete=models.CASCADE, related_name='basketGamesModel_home_team')
    away_team = models.ForeignKey(basketTeamsModel, null=True,on_delete=models.CASCADE, related_name='basketGamesModel_away_team')



class basketGameScoreModel(models.Model):
    game = models.OneToOneField(basketGamesModel,null=True, on_delete=models.CASCADE, related_name='basketGameScoreModel_game')
    home_quarter_1 = models.IntegerField()
    home_quarter_2 = models.IntegerField()
    home_quarter_3 = models.IntegerField()
    home_quarter_4 = models.IntegerField()
    overtime = models.CharField(max_length=100,null=True, blank=True)
    total = models.IntegerField()
    away_quarter_1 = models.IntegerField()
    away_quarter_2 = models.IntegerField()
    away_quarter_3 = models.IntegerField()
    away_quarter_4 = models.IntegerField()
    away_overtime = models.CharField(max_length=100,null=True, blank=True)
    away_total= models.IntegerField()
    winner = models.ForeignKey(basketTeamsModel, on_delete=models.CASCADE, related_name='basketGameScoreModel_winner')




########################33
from django.shortcuts import render
from requests import request

from basket_pro.basket_core.settings import baseurl


# Create your views here.
def hii_country(country):
    print(country)


def country_code():
    url = f"{baseurl}/countries"
    headers = {
        'x-rapidapi-host': "v1.basketball.api-sports.io",
        'x-rapidapi-key': "3d97288faa1f5f2b5de620df02e52b60"
    }
    Response = request("GET", "/countries", headers=headers)

    countries = Response.json()


    print(countries.decode("utf-8"))

    for country in countries['Response']:
        hii_country(country)
    print('countries data')

country_code()

########################
admin.site.register(basketTeamsModel)
admin.site.register(basketLeagueModel)
admin.site.register(basketCountriesModel)
admin.site.register(basketGamesModel)
admin.site.register(basketLeagueSeasonModel)
admin.site.register(basketGameScoreModel)
admin.site.register(basketSeasonModel)

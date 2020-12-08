from django.db import models

# Create your models here.
class PredictionData(models.Model):
    id = models.AutoField(primary_key=True)

    #Image String obtained via Ajax
    dataURI = models.TextField()
    userAns = models.PositiveSmallIntegerField()
    #What Model Predicted
    modelPredVal =  models.PositiveSmallIntegerField()
    #Prediction Probability of all values
    allPredProba = models.JSONField()
    #Prediction Result
    resultPred = models.BooleanField()

    dateTime = models.DateField(auto_now =True)

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from . import image_preprocessing
from . import model_prediction
from .models import PredictionData
import numpy as np
import json
import os

#Defining and initializing dictionrary to keep track of all prediction attributes
global prediction_dict_global
prediction_dict_global = {}

# Initial View when the page is loaded
def index(request):
    context = {'result':''}
    return render(request,os.path.join('canvas','index.html'),context)

#Takes in dataURI and returns predictions of the CNN model
def prediction_results(dataURI):

    #Preprocessing the data URI and checking if the canvas is empty or not
    pixel_array = image_preprocessing.convert_image_to_byte(dataURI)
    pixel_array_filtered = image_preprocessing.remove_noise(pixel_array)

    #Initializing output list
    result_list = []

    #Checking if the canvas is empty or not
    if pixel_array_filtered is not None:

        #Converting original pixel array into 28X28 pixel array
        pixel_array_resized = image_preprocessing.convert_into_required_size(pixel_array_filtered)

        #Feeding the pixel array to CNN model for prediction
        result_pytorch = model_prediction.predict_pytorch(pixel_array_resized)

        #Storing tensor into the global dictionary
        prediction_dict_global['predArray'] = result_pytorch

        #Getting the predicted number
        predicted_number = int((result_pytorch.argmax()))

        #Getting probability
        prediction_probability = int(result_pytorch.max()  * 100)

        #Assigning 0 to status_code as the canvas is not empty
        status_code = 0

        #Appending results to the output list
        result_list.append(status_code)
        result_list.append(predicted_number)
        result_list.append(prediction_probability)

    else:

        #Assigning 1 to status_code as the canvas is empty
        status_code = 1
        result_list.append(status_code)

    return result_list


#View that takes in ajax request to make the prediction
def predict_number(request):

    ############ Status_code Values and Meaning ###########
    # 0 - Success
    # 1 - Empty canvas

    #Initializing Variables
    predicted_number = 0
    prediction_probability = 0
    status_code = 0

    #Getting dataURI of the drawn image
    result = (request.GET.get('dataURI', None))
    # print(result)
    dataURI = result.split(',')[1]

    #Storing the dataURI in the global dictionary
    prediction_dict_global['dataURI'] = dataURI

    #Calling the prediction_results function to feed the value to the model and get the required prediction
    predicted_result_list = prediction_results(dataURI)

    #Getting status code value
    status_code = predicted_result_list[0]

    #Checking whether the canvas is empty or not
    if status_code == 0:
        predicted_number  = predicted_result_list[1]
        prediction_probability = predicted_result_list[2]
        prediction_dict_global['modelPredVal'] = predicted_number


    #Sending prediction results to display results to the user
    data = {'number':predicted_number,'probability':prediction_probability,'status_code' : status_code}
    print(data)
    return JsonResponse(data)


#View that gets the ajax request to store data in DB
def store_data(request):

    #Gets user response
    result = request.GET.get('values',None)
    result = json.loads(result)



    #Storing user data is the global dictionary
    prediction_dict_global['resultPred'] = result['resultPred']
    prediction_dict_global['userAns'] = result['userAns']

    #Storing probability of each digit as given by the model
    pred_array = prediction_dict_global['predArray'] * 100
    proba_dict = {'0':int(pred_array[0]),
                  '1':int(pred_array[1]),
                  '2':int(pred_array[2]),
                  '3':int(pred_array[3]),
                  '4':int(pred_array[4]),
                  '5':int(pred_array[5]),
                  '6':int(pred_array[6]),
                  '7':int(pred_array[7]),
                  '8':int(pred_array[8]),
                  '9':int(pred_array[9])}
    print(prediction_dict_global)


    #Storing Prediction attributes and user response in the databse
    pred_data = PredictionData.objects.create(dataURI = prediction_dict_global['dataURI'],
                                            userAns=prediction_dict_global['userAns'],
                                            modelPredVal=prediction_dict_global['modelPredVal'],
                                            allPredProba = proba_dict,
                                            resultPred=prediction_dict_global['resultPred'])

    pred_data.save()

    #Code to send success message
    data = {'status_code':0}
    return JsonResponse(data)

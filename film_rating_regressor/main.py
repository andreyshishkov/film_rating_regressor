from fastapi import FastAPI
import pickle
from film_rating_regressor.api_classes import RatingModel, DescrRequest

app = FastAPI(title='Film rating regressor',
              description='API predict rating of film using movie description'
              )




@app.post('/single_predict')
async def get_prediction(description: DescrRequest):
    """take description of film and return rating"""
    description = description.descr
    model = RatingModel()
    prediction = model.predict_single(description)
    return prediction


@app.get('/')
async def greet():
    return 'Hello, user'

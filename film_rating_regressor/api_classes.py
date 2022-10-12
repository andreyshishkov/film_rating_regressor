import pickle
from pydantic import BaseModel


class DescrRequest(BaseModel):
    descr: str


class RatingModel:

    def __init__(self):
        with open('model.pkl', 'rb') as file:
            self._model = pickle.load(file)

    def predict_single(self, descr: str):
        data_in = [descr]
        prediction = self._model.predict(data_in)
        return prediction


if __name__ == '__main__':
    RatingModel()

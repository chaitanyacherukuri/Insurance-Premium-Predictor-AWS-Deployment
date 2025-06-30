from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse
from model.predict import predict_output, model, MODEL_VERSION

app = FastAPI()

#human readable
@app.get('/')
def home():
    return {'message': 'Insurance Premium Predictor API'}

#machine readable
@app.get('/health')
def health_check():
    return {'status': 'ok',
            'version': MODEL_VERSION,
            'model_loaded': model is not None}

@app.post('/predict')
def predict_premium(data: UserInput, response_model=PredictionResponse):

    input_df = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    try:
        prediction = predict_output(input_df)

        return JSONResponse(status_code=200, content={'response': prediction})
    
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))






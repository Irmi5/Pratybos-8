import azure.functions as func
import logging
import os
import google.generativeai as genai

app = func.FunctionApp()

@app.route(route="Pratybos8", auth_level=func.AuthLevel.FUNCTION)
def Pratybos8(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Gauta užklausa į Google Gemini fasadą.')

    api_key = os.environ.get("GOOGLE_API_KEY")
    
    if not api_key:
        return func.HttpResponse(
            "Klaida: Serverio konfigūracijoje nerastas GOOGLE_API_KEY.",
            status_code=500
        )

    genai.configure(api_key=api_key)

    question = req.params.get('question')
    if not question:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            question = req_body.get('question')

    if not question:
        return func.HttpResponse(
            "Prašome pateikti 'question' parametrą užklausos URL arba body.",
            status_code=400
        )

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        response = model.generate_content(question)
        
        answer = response.text
        
        return func.HttpResponse(answer, status_code=200)

    except Exception as e:
        logging.error(f"Google AI klaida: {e}")
        return func.HttpResponse(
            f"Įvyko klaida: {str(e)}",
            status_code=500
        )
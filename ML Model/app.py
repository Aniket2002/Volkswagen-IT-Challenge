from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import pywhatkit as kit
import datetime

app = Flask(__name__, template_folder='templates')

# Load the serialized model
model = joblib.load('model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get user input from the form
        NO = float(request.form['NO'])
        NO2 = float(request.form['NO2'])
        NOx = float(request.form['NOx'])
        CO = float(request.form['CO'])
        SO2 = float(request.form['SO2'])
        Benzene = float(request.form['Benzene'])

        # Create a DataFrame from the user input
        user_input = pd.DataFrame({
            'NO': [NO],
            'NO2': [NO2],
            'NOx': [NOx],
            'CO': [CO],
            'SO2': [SO2],
            'Benzene': [Benzene]
        })

        # Make predictions based on the user input DataFrame
        predictions = model.predict(user_input)

        # Define messages based on the predictions
        analysis_messages = {
            0: "CO < NOx < Benzene: Lower CO and NOx with higher benzene emissions may suggest inefficient combustion and potentially higher fuel consumption.",
            1: "CO > NOx < Benzene: Elevated CO levels compared to NOx and benzene could indicate incomplete combustion, possibly leading to increased fuel consumption.",
            2: "CO < NOx > Benzene: Higher NOx levels relative to CO and benzene may indicate efficient combustion but potentially higher fuel consumption due to the formation of nitrogen oxides.",
            3: "CO > NOx > Benzene: Elevated CO and NOx levels along with benzene emissions may indicate both incomplete combustion and inefficient engine operation, likely resulting in increased fuel consumption."
        }

        analysis_message = analysis_messages.get(predictions[0], "Elevated CO and NOx levels along with benzene emissions may indicate both incomplete combustion and inefficient engine operation, likely resulting in increased fuel consumption.")

        # Send the result to WhatsApp
        phone_number = '918375057720'  # Replace with your recipient's phone number
        message = f"Analysis Result: {analysis_message}"
        send_whatsapp_message(phone_number, message)

        return jsonify({'predictions': predictions.tolist(), 'message': analysis_message})
    except Exception as e:
        return jsonify({'error': str(e)})

def send_whatsapp_message(phone_number, message):
    # Send a WhatsApp message with the result
    current_time = datetime.datetime.now()
    scheduled_time = current_time + datetime.timedelta(minutes=1)
    kit.sendwhatmsg(phone_number, message, scheduled_time.hour, scheduled_time.minute)

if __name__ == '__main__':
    app.run(debug=True)

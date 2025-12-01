from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulated database
lands = []
requests_db = []

# Auto-increment ID
land_id_counter = 1

@app.route('/')
def seller_dashboard():
    return render_template('seller.html', lands=lands, requests_db=requests_db)

@app.route('/list_land', methods=['POST'])
def list_land():
    global land_id_counter
    location = request.form['location']
    lands.append({'id': land_id_counter, 'location': location, 'owner': 'seller', 'isListed': True})
    land_id_counter += 1
    return redirect(url_for('seller_dashboard'))

@app.route('/request_buy/<int:land_id>', methods=['POST'])
def request_buy(land_id):
    buyer_name = request.form['buyerName']
    message = request.form['message']
    requests_db.append({
        'land_id': land_id,
        'buyer_name': buyer_name,
        'message': message,
        'approved': False
    })
    return redirect(url_for('seller_dashboard'))

@app.route('/approve/<int:request_index>')
def approve_request(request_index):
    req = requests_db[request_index]
    req['approved'] = True
    # Mark land as sold
    for land in lands:
        if land['id'] == req['land_id']:
            land['isListed'] = False
    return redirect(url_for('seller_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)

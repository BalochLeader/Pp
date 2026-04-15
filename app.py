    
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

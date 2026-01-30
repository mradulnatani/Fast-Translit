from app.service.translit import transliterate_text

tests = [
    "नमस्ते",
    "महाकाल मंदिर, उज्जैन",
    "शिवाजी नगर विस्तार, इंदौर",
    "एम.जी. रोड, बेंगलुरु",
    "सेक्टर 62, नोएडा",
    "",
    "   ",
]

for t in tests:
    print("\nINPUT :", repr(t))
    print("OUTPUT:", transliterate_text(t))


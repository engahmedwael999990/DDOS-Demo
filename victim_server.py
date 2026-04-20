from flask import Flask
import logging

app = Flask(__name__)

# إخفاء رسائل Flask العادية عشان شاشة الـ Terminal تفضل نظيفة
log = logging.getLogger('werkzeug')
log.disabled = True 

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Enterprise Server Dashboard</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #1e1e1e; color: white; text-align: center; padding-top: 100px;}
        .status { font-size: 40px; font-weight: bold; background: #000; padding: 20px; border-radius: 10px; display: inline-block; border: 3px solid #00ff00; color: #00ff00;}
        .loader { border: 8px solid #333; border-top: 8px solid #00ff00; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 30px auto;}
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <h1>🌐 Main Database Server</h1>
    <div class="status">✅ STATUS: ONLINE & HEALTHY</div>
    <p>Simulating Legitimate User Traffic...</p>
    <div class="loader"></div>
    <script>
        // المتصفح بيعمل Refresh كل ثانية ونص
        setTimeout(function(){ location.reload(); }, 1500);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    # هنا مفيش time.sleep لأن السيرفر ضعيف خلقة ومش محتاج تعطيل
    return HTML_PAGE

if __name__ == "__main__":
    print("[*] Basic Single-Threaded Web Server started.")
    print("[*] Server is running on hidden port 8081.")
    print("[!] Vulnerability Active: threaded=False (Can only handle 1 request at a time).")
    
    # الثغرة الأساسية هنا: السيرفر Single-Threaded
    app.run(host="127.0.0.1", port=8081, threaded=False)
import os
import ssl
from app import create_app

app = create_app()

# if __name__ == '__main__':
#    port = int(os.environ.get("PORT", 5151))
#    app.run(host='0.0.0.0', port=port, debug=True)
   

if __name__ == "__main__":
	# context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
	# context.load_cert_chain(os.path.join('ssl', 'ng2toh.crt'), os.path.join('ssl', 'ng2toh.key'))
	app.run(host='0.0.0.0', port=5252, debug=True)
	
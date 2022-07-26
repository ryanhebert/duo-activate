import jwt, os, duo_client
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from time import time
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

class Duo_enroll:

   def __init__(self, token, is_test=False):

      self.token = token
      self.is_test = is_test

      self.token_user_upn = None
      self.token_user_email = None
      self.token_expiration = 0
      self.token_user_ip = '0.0.0.0'

      self.duo_username = None
      self.duo_user_id = None
      self.duo_user_phones = []
      self.duo_user_created = 0

      self.duo_new_phone = None
      self.duo_activation_barcode = None
      self.duo_activation_url = None
      self.duo_activation_expiration = 0
      self.duo_installation_url = None

      self.config_init = self.load_config()
      self.clients_init = self.init_clients()
      self.token_init = self.init_token()
      self.user_init = self.init_user()

   def load_config(self):

      if all(x in os.environ for x in ["DUO_API_HOST","DUO_ADMIN_IKEY","DUO_ADMIN_SKEY","DUO_AUTH_IKEY","DUO_AUTH_SKEY"]):

         self.duo_api_host = os.getenv("DUO_API_HOST")
         self.duo_admin_ikey = os.getenv("DUO_ADMIN_IKEY")
         self.duo_admin_skey = os.getenv("DUO_ADMIN_SKEY")
         self.duo_auth_ikey = os.getenv("DUO_AUTH_IKEY")
         self.duo_auth_skey = os.getenv("DUO_AUTH_SKEY")

         print("Found all duo variables in environment.")

         return True

      elif all(x in os.environ for x in ["AZURE_VAULT_URI","DUO_API_HOST","DUO_ADMIN_IKEY","DUO_AUTH_IKEY"]):

         self.duo_api_host = os.getenv("DUO_API_HOST")
         self.duo_admin_ikey = os.getenv("DUO_ADMIN_IKEY")
         self.duo_auth_ikey = os.getenv("DUO_AUTH_IKEY")

         azure_vault_client = SecretClient(
            vault_url = os.getenv("AZURE_VAULT_URI"),
            credential = DefaultAzureCredential()
            )

         try:
            self.duo_admin_skey = azure_vault_client.get_secret("DUO_ADMIN_SKEY").value
            self.duo_auth_skey = azure_vault_client.get_secret("DUO_AUTH_SKEY").value

            return True

         except Exception as e:
            print(e)

      elif "AZURE_VAULT_URI" in os.environ:
         
         azure_vault_client = SecretClient(
            vault_url = os.getenv("AZURE_VAULT_URI"),
            credential = DefaultAzureCredential()
            )

         try:

            self.duo_api_host = azure_vault_client.get_secret("DUO_API_HOST").value
            self.duo_admin_ikey = azure_vault_client.get_secret("DUO_ADMIN_IKEY").value
            self.duo_admin_skey = azure_vault_client.get_secret("DUO_ADMIN_SKEY").value
            self.duo_auth_ikey = azure_vault_client.get_secret("DUO_AUTH_IKEY").value
            self.duo_auth_skey = azure_vault_client.get_secret("DUO_AUTH_SKEY").value

            return True

         except Exception as e:
            print(e)

      return False

   def init_clients(self):

      if self.config_init:

         self.duo_admin_client = duo_client.Admin(
            ikey = self.duo_admin_ikey,
            skey = self.duo_admin_skey,
            host = self.duo_api_host
         )

         self.duo_auth_client = duo_client.Auth(
            ikey = self.duo_auth_ikey,
            skey = self.duo_auth_skey,
            host = self.duo_api_host
         )
         print("Clients initialized.")
         return True
      else:
         print("Could not initialize clients.")
         return False

   def init_token(self):

      try:
         token_alg = jwt.get_unverified_header(self.token)['alg']
         decoded_token = jwt.decode(self.token, algorithms=[token_alg], options={"verify_signature": False})

         # Need to build logic to deal with case in which UPN or EMAIL are missing
         self.token_user_upn = decoded_token['upn']
         self.token_user_email = decoded_token['email']
         self.token_expiration = decoded_token['exp']
         self.token_user_ip = decoded_token['ipaddr']

         if self.is_test:
            self.token_expiration = time() + 600

         print("Token initialzed.")
         return True

      except Exception as e:
         print("Error during token initialization.")
         print(e)
         return False

   def init_user(self):

      try:
         if self.token_user_upn is not None:
            duo_user = self.duo_admin_client.get_users_by_name(self.token_user_upn)[0]
         else:
            duo_user = self.duo_admin_client.get_users_by_name(self.token_user_email)[0]

      except Exception as e:
         print("Error during user initializtion.")
         print(e)
         return False

      self.duo_username = duo_user['username']
      self.duo_user_id = duo_user['user_id']
      self.duo_user_phones = duo_user['phones']
      self.duo_user_created = duo_user['created']
      
      return True

   def create_phone(self):

      for phone in self.duo_user_phones:

         if phone['name'] == self.duo_username and phone['activated'] == False:
            print("Phone already exists.")
            self.duo_new_phone = phone

      if self.duo_new_phone is None:

         self.duo_new_phone = self.duo_admin_client.add_phone(
            name = self.duo_username,
            type = "mobile",
            platform = "generic smartphone"
            )

         self.duo_admin_client.add_user_phone(
            user_id = self.duo_user_id, 
            phone_id = self.duo_new_phone['phone_id']
            )

         self.duo_user_phones = self.duo_admin_client.get_user_phones(
            user_id = self.duo_user_id
         )

      if time() < self.duo_activation_expiration:
         print("Already have a valid barcode.")
      else:
         print("Getting new barcode.")
         activation = self.duo_admin_client.create_activation_url(
            phone_id = self.duo_new_phone['phone_id'],
            valid_secs = 600,
            install = 1
         )

         self.duo_activation_barcode = activation['activation_barcode']
         self.duo_activation_url = activation['activation_url']
         self.duo_activation_expiration = time() + int(activation['valid_secs'])
         self.duo_installation_url = activation['installation_url']

   def test_duo_auth_api(self):

      results = None

      try:
         results = self.duo_auth_client.ping()
         if results is not None:
            print("Duo Auth API test passed.")
      except Exception as e:
         print("Error testing auth api endpoint.")
         print(e)

   def test_duo_admin_api(self):

      results = None

      try:
         results = self.duo_admin_client.get_info_summary()
         if results is not None:
            print("Duo Admin API test passed.")
      except Exception as e:
         print("Error testing admin api endpoint.")
         print(e)

duo = None
app = Flask(__name__)

@app.route('/')
def index():

   token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjJaUXBKM1VwYmpBWVhZR2FYRUpsOGxWMFRPSSJ9.eyJhdWQiOiJhMTBkMDlmMy03OGVkLTQwNGItODQxNS1jMDM4OTczZjcxNzMiLCJpc3MiOiJodHRwczovL2xvZ2luLm1pY3Jvc29mdG9ubGluZS5jb20vODA3ZDMwYTUtYmJkZi00MzNjLTljZjktZjYzNjc3MWJhMGMwL3YyLjAiLCJpYXQiOjE2NTg3NTUwMDYsIm5iZiI6MTY1ODc1NTAwNiwiZXhwIjoxNjU4NzU4OTA2LCJhY2N0IjowLCJhaW8iOiJBVVFBdS84VEFBQUExZ0hzOGJ4WjF6c3NDZFRMQzQwVTByaGZxc1dUTk9aZW9ZYUY5eTNtUzJ1MXRuTWxKcTJWd0Q3VVBoVE9mUXQyV2FwTUl2NE1OenN1TW9aKzc5RDY4UT09IiwiYXV0aF90aW1lIjoxNjU4NzU1MzA2LCJlbWFpbCI6ImxpdmlAYXp1cmUuZHVvLnJ5YW4uYW0iLCJmYW1pbHlfbmFtZSI6IkhlYmVydCIsImdpdmVuX25hbWUiOiJPbGl2aWEiLCJpcGFkZHIiOiIyNC4yNDcuMjE0LjcxIiwibG9naW5faGludCI6Ik8uQ2lSaU5XVTNaVGt3TUMwMk5EYzNMVFJqTW1FdE9UazVNeTFoWldNeE56Z3lPVGxpTnpVU0pEZ3dOMlF6TUdFMUxXSmlaR1l0TkRNell5MDVZMlk1TFdZMk16WTNOekZpWVRCak1Cb1diR2wyYVVCaGVuVnlaUzVrZFc4dWNubGhiaTVoYlNEWEFRPT0iLCJuYW1lIjoiT2xpdmlhIEsuIEhlYmVydCIsIm5vbmNlIjoiNDRmZTQxMTA5NzBiNGRiMDgyNzlkMzYzYzcyOGI0MjBfMjAyMjA3MjUxMzI2MjQiLCJvaWQiOiJiNWU3ZTkwMC02NDc3LTRjMmEtOTk5My1hZWMxNzgyOTliNzUiLCJvbnByZW1fc2lkIjoiUy0xLTUtMjEtMjAzMjE5MTQxLTM3Mzc3Mjc5NjAtNDI3MDI0NzY4My0xMTM2IiwicHJlZmVycmVkX3VzZXJuYW1lIjoibGl2aUBhenVyZS5kdW8ucnlhbi5hbSIsInJoIjoiMC5BVmtBcFRCOWdOLTdQRU9jLWZZMmR4dWd3UE1KRGFIdGVFdEFoQlhBT0pjX2NYTlpBUDAuIiwic2lkIjoiYjA3MDY2ZDctYmMyOS00YWQzLTljNmQtMDZkODU4ZDI2NmE1Iiwic3ViIjoiWUtmaEdIMnROejMtWEFiSThYcHkwX21IQUZ4YWZGTmUxTDJyb0V5YjdSYyIsInRlbmFudF9jdHJ5IjoiVVMiLCJ0ZW5hbnRfcmVnaW9uX3Njb3BlIjoiTkEiLCJ0aWQiOiI4MDdkMzBhNS1iYmRmLTQzM2MtOWNmOS1mNjM2NzcxYmEwYzAiLCJ1cG4iOiJsaXZpQGF6dXJlLmR1by5yeWFuLmFtIiwidXRpIjoiTy1pTHU5WGloa0c1Uy1uTThmTmFBQSIsInZlciI6IjIuMCIsInZlcmlmaWVkX3ByaW1hcnlfZW1haWwiOlsibGl2aUBhenVyZS5kdW8ucnlhbi5hbSJdLCJ2ZXJpZmllZF9zZWNvbmRhcnlfZW1haWwiOlsibGl2aTg4ODBAcnlhbmFtLm9ubWljcm9zb2Z0LmNvbSJdLCJ4bXNfdHBsIjoiZW4ifQ.uIwVLPtxjUCypg2y88U-FrYcqvvuezYYvpdkQBDd_JpnU5-7XkQeFN7FD290VgJZ7gg97At8IjchkD8DMIdzAbt5vOWbAQ-UtAWnwD2lM776kcHIxIUXI7j56DbfRaXqxZwTsyvp9_di4ZnjIwDfWMRBow3MRpUyQaewElTENP9gu5cb2crbBk7gQ7oowpgrK8zl2nIwGIX7OcRUp6vQAUNYpoja1csUHTR_ZtRB1hyoatFvUcmUfOtCZOdfgY1DhdJ5xFDg3QjtSTO-z9FC-Zzbi9zEFYxRTqsobO_diHtG3ggsy2sr6kWHG6OB-xGg7xW75o_t1pV9RdodjoE7NA"
   
   if token is None:
      token = request.headers['X-Ms-Token-Aad-Id-Token']
      is_test = False
   else:
      is_test = True

   global duo

   if duo is None or duo.token_expiration < time():
      print("Initializing application.")
      duo = Duo_enroll(token=token, is_test = is_test)
   else:
      print("Picking up where we left off.")
   
   duo.create_phone()


   print('Request for index page received')
   return render_template(
      'index.html', 
      qr_url = duo.duo_activation_barcode,
      qr_expiration = duo.duo_activation_expiration,
      access_token = duo.token_expiration
   )

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')

@app.route('/testMfa')

def test_mfa():

   global duo

   try: 
     push_result = duo.duo_auth_client.auth(
         async_txn = True,
         user_id = duo.duo_user_id,
         ipaddr = duo.token_user_ip,
         factor = 'push', 
         device = duo.duo_new_phone['phone_id']
     )
     print(push_result)
   except Exception as e:
      print(e)

   return render_template(
      'prompt.html',
      txid = push_result['txid']
   )
@app.route('/checkPush')
def check_push():

   global duo

   txid = request.args['txid']
   status = duo.duo_auth_client.auth_status(txid)
   print(status)
   return status

@app.route('/checkActivation')
def check_activation():

   # still need to account for token?
   global duo
   phone = duo.duo_admin_client.get_phone_by_id(duo.duo_new_phone['phone_id'])

   response = '{"activated" : %s}' % str(phone['activated']).lower()
   return response

if __name__ == '__main__':
   app.run()
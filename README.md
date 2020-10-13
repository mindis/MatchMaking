MatchMaking Algorithm




# Purpose

Automates SEM Operations Tasks by creating a Self Service Tool (A web page) that empowers SEM specialist to run the SEM engines as and when needed.



# Project Installation

## Data Science Server/Locally

1. Log in to Data Science Server (54.212.242.95) command line using credentials/SSH or open a Terminal locally

2. Setup Python Virtual Envrionment by running below command:
   
```
   $ virtualenv --python=/usr/bin/python3.7 name_of_virtual_env
```

3. Activate Python Virtual Environment created in above step by running below command:
```bash

   $ source name_of_virtual_env/bin/activate
```

4. Clone the git repository by running below command:
```bash
 
   $ git clone git@github.com:Groupe-Atallah/ds-sem-service.git
```

5. Install dependent packages/libraries within virtual environment by running below command:
```bash
  
   $ python -m pip install -r ds-sem-service/requirements.txt

```

# Launching interface
Run the below command to execute the project
```bash

   $ nohup python -u ds-sem-service/web_app/run.py &

   Note, Project runs on port 3333 and can be acessed using below link:

   http://54.212.242.95:3333/

```

# Terminating Process
```bash
Run the below command to find PID

  $ ps aux | grep run.py

# Run the below command to terminate the process
  
  $ kill $PID
```

# Configurations

In order to properly run this project, the following must be setup.

1. Configure SSENSE database credentials

```bash

   ds-sem-service/resources/config/config.yml must be present and configured as per below

   athena:
       s3_staging_dir: s3://aws-athena-query-results-ssense-dataops
       aws_access_key_id: <ACCESS_KEY>
       aws_secret_access_key: <SECRET_KEY>
       region_name: us-west-2
   ssense:
       host: slave.ssense.com
       user: <USER_NAME>
       pwd: <PASSWORD>
       db: ssense
   stats:
       host: slave.ssense.com
       user: <USER_NAME>
       pwd: <PASSWORD>
       db: stats   
   ssense-recommendation-development:
      bucket: ssense-recommendation-framework-development
      id: <ID>
      secret: <KEY>
   ssense-recommendation-qa:
      bucket: ssense-recommendation-framework-qa
      id: <ID>
      secret: <KEY>
```

2. Configure BigQuery credentials
```bash

   ds-sem-service/resources/config/ssense-3c92053ad127.json must be present
```

3. Configure Google My Drive credentials


   Steps to Configure Google My Drive Account:

   1. Go to https://console.developers.google.com/ and Choose any existing project (i.e. utopian-catfish-599)

   2. Click Credentials 

   3. CREATE CREDENTIALS by choosing following

      a. OAuth  client ID
      
      b. Application type - Web Application
      
      c. Name - <give_any_name>
      
      d. Authorized JavaScript origin (+ADD URI) - http://localhost:8080
      
      e. Authorized redirect URIs  - http://localhost:8080/
      
      f Click SAVE

   4. Download JSON
   
   5. Rename the json to client_secrets.json
   
   6. Create settings.yaml file as per below
      ```
      client_config_backend: settings
      client_config:
      client_id: <CLIENT_ID FROM client_secrets.json>
      client_secret: <CLIENT_SECRET FROM client_secrets.json>

      save_credentials: True
      save_credentials_backend: file
      save_credentials_file: credentials.json

      get_refresh_token: True

      oauth_scope:
        - https://www.googleapis.com/auth/drive.file
        - https://www.googleapis.com/auth/drive.install
        - https://www.googleapis.com/auth/drive

      ```
      

   7. Copy client_secrets.json and  settings.yaml files under ds-sem-service/web_app/
   
   8. Run ds-sem-service/web_app/google_drive_connector.py manually using below command
      ```
      $ python google_drive_connector.py
      ```
   
   9. A web page will open asking you to login to google account.
   
   10. A message will appear on sucessfull login "The authentication flow has completed."
    
    Please note that client_secrets.json is used to authenticate google account so use the same account during web authentication 
    (account used to create  client_secrets.json
   
   11. credentials.json will be downloaded automatically and used for systematic authentication
   
   12. Above steps will ensure following files are available under ds-sem-service/web_app/
   
      [client_secrets.json, settings.yaml, credentials.json]
      






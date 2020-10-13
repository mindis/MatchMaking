MatchMaking Algorithm




# Purpose

Automates SEM Operations Tasks by creating a Self Service Tool (A web page) that empowers SEM specialist to run the SEM engines as and when needed.



# Project Installation

## Data Science Server/Locally

1. Log in to Data Science Server (54.212.242.95) command line using credentials/SSH or open a Terminal locally
2. Setup Python Virtual Envrionment by running below command:
   
   virtualenv --python=/usr/bin/python3.7 name_of_virtual_env


3. Activate Python Virtual Environment setup in above step:
   source name_of_virtual_env/bin/activate

4. Clone the git repository by running below command:
    
   git clone git@github.com:Groupe-Atallah/ds-sem-service.git

5. Install dependent packages/libraries within virtual environment by running below command:
   python -m pip install -r ds-sem-service/requirements.txt


# Project Execution
#Run the below command to execute the project

nohup python -u ds-sem-service/web_app/run.py &

Note, Project runs on port 3333 and can be acessed using below link:

http://54.212.242.95:3333/



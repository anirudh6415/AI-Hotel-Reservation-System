pipeline{
    agent any 

    environment{
        VENV_DIR = 'venv'
    }

    stages{
        stage('Cloning github repo to jenkins'){
            steps{
                script{
                    echo 'Cloning github repo to jenkins................'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/anirudh6415/AI-Hotel-Reservation-System.git']])
                }
            }
        }
    }

    stage('Setting Up Virtual Environment and Installing Dependancies'){
        steps{
            script{
                echo 'Setting Up Virtual Environment and Installing Dependancies............'
                sh ''' 
                python -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -e .
                '''
            }
        }
    }
}
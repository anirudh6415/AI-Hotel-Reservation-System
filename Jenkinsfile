pipeline{
    agent any 
    stages{
        stage{'Cloning github repo to jenkins'}{
            steps{
                script{
                    echo 'Cloning github repo to jenkins................'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/anirudh6415/AI-Hotel-Reservation-System.git']])
                }
            }
        }
    }
}
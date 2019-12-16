pipeline {
	agent any
	stages {
		stage('Setup') {
			steps {
				echo 'Setting up ...'
				sh 'sudo apt-get -q install -y python python-pip make'
				dir('software/sim') {
					sh 'sudo pip install -r requirements.txt'
				}
			}
		}
		stage('Test') {
			steps {
				echo 'Testing ...'
				dir('software/sim') {
					sh 'make'
				}
			}
		}
	}
	post {
		always {
			commonStepNotification()
		}
	}
}

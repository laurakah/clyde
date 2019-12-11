pipeline {
	agent any
	stages {
		stage('Setup') {
			steps {
				echo 'Setting up ...'
				sh 'sudo apt-get -q install -y python make'
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

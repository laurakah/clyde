pipeline {
	agent any
	environment {
		CLYDE_SIM_DIR = 'software/sim'
	}
	stages {
		stage('Setup') {
			steps {
				echo 'Setting up ...'
				sh 'sudo apt-get -q install -y python python-pip make'
				dir("${env.CLYDE_SIM_DIR}") {
					sh 'sudo pip install -r requirements.txt'
				}
			}
		}
		stage('Test') {
			steps {
				echo 'Testing ...'
				dir("${env.CLYDE_SIM_DIR}") {
					sh 'python -m xmlrunner discover -p"*Test.py" -v'
				}
			}
			post {
				always {
					junit "${env.CLYDE_SIM_DIR}/TEST-*.xml"
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

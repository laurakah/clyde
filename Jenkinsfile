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
					sh 'python -m xmlrunner discover -p"*Test.py" -v'
				}
			}
			post {
				always {
					junit 'software/sim/TEST-*.xml'
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

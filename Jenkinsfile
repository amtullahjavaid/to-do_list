pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'todo-app'
        DOCKER_TAG = "latest"
        APP_PORT = '3000'
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "Starting CI/CD Pipeline"
                }
                checkout scm
            }
        }
        
        stage('Code Linting') {
            steps {
                script {                 
                    sh '''
                        python3 -m pip install --user flake8 pylint
                        
                        flake8 app.py --max-line-length=120 --ignore=E501,W503 
                        
                        pylint app.py --exit-zero"
                    '''
                }
            }
        }
        
        stage('Code Build') {
            steps {
                script {                    
                    sh '''
                        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }
        
        stage('Unit Testing') {
            steps {
                script {
                    sh '''
                        python3 -m pip install --user flask pytest
                        
                        cat > test_unit.py << 'EOF'
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Todo

class TodoAppUnitTests(unittest.TestCase):
    
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DB'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_health_endpoint(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn('healthy', response.get_json()['status'])
    
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_add_todo(self):
        response = self.client.post('/add', data={'title': 'Test Todo'})
        self.assertEqual(response.status_code, 302)  

if __name__ == '__main__':
    unittest.main()
EOF
                        
                        python3 test_unit.py
                    '''
                }
            }
        }
        
        stage('Containerized Deployment') {
            steps {
                script {                    
                    sh '''
                        docker-compose -p ${PROJECT_NAME} down 
                        
                        docker-compose -p ${PROJECT_NAME} up -d

                        docker-compose -p ${PROJECT_NAME} ps
                        
                    '''
                }
            }
        }
        
        stage('Selenium Testing') {
            steps {
                script {                    
                    sh '''
                        docker build -f Dockerfile.selenium -t selenium-tests:latest .
                        
                        docker run --rm 
                    '''
                }
            }
        }
    }
    post {
        always {
            sh 'docker system prune -af'
        }
    }
    
}

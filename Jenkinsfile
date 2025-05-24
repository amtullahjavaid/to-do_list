// pipeline {
//     agent any
    
//     environment {
//         DOCKER_IMAGE = 'todo-app'
//         DOCKER_TAG = "${BUILD_NUMBER}"
//         APP_PORT = '3000'
//         COMPOSE_PROJECT_NAME = "todo-app-${BUILD_NUMBER}"
//     }
    
//     stages {
//         stage('Checkout') {
//             steps {
//                 script {
//                     echo "Starting CI/CD Pipeline for Build #${BUILD_NUMBER}"
//                 }
//                 // Clean workspace
//                 cleanWs()
//                 // Checkout code from GitHub
//                 checkout scm
//                 echo "Code checked out successfully"
//             }
//         }
        
//         stage('Code Linting') {
//             steps {
//                 script {
//                     echo "Running Code Linting..."
                    
//                     // Install Python and required tools
//                     sh '''
//                         python3 -m pip install --user flake8 pylint
//                         export PATH=$PATH:~/.local/bin
                        
//                         echo "Running flake8 linting..."
//                         flake8 app.py --max-line-length=120 --ignore=E501,W503 || echo "Linting completed with warnings"
                        
//                         echo "Running pylint..."
//                         pylint app.py --exit-zero --rcfile=/dev/null || echo "Pylint completed"
                        
//                         echo "Code linting stage completed"
//                     '''
//                 }
//             }
//         }
        
//         stage('Code Build') {
//             steps {
//                 script {
//                     echo "Building Application..."
                    
//                     // Build Docker image
//                     sh '''
//                         echo "Building Docker image..."
//                         docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
//                         docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                        
//                         echo "Docker image built successfully"
//                         docker images | grep ${DOCKER_IMAGE}
//                     '''
//                 }
//             }
//         }
        
//         stage('Unit Testing') {
//             steps {
//                 script {
//                     echo "Running Unit Tests..."
                    
//                     sh '''
//                         # Install test dependencies
//                         python3 -m pip install --user flask pytest
//                         export PATH=$PATH:~/.local/bin
                        
//                         # Create simple unit test
//                         cat > test_unit.py << 'EOF'
// import unittest
// import sys
// import os

// # Add the current directory to the path
// sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

// from app import app, db, Todo

// class TodoAppUnitTests(unittest.TestCase):
    
//     def setUp(self):
//         self.app = app
//         self.app.config['TESTING'] = True
//         self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
//         self.client = self.app.test_client()
        
//         with self.app.app_context():
//             db.create_all()
    
//     def tearDown(self):
//         with self.app.app_context():
//             db.session.remove()
//             db.drop_all()
    
//     def test_health_endpoint(self):
//         """Test the health check endpoint"""
//         response = self.client.get('/health')
//         self.assertEqual(response.status_code, 200)
//         self.assertIn('healthy', response.get_json()['status'])
    
//     def test_home_page(self):
//         """Test the home page loads"""
//         response = self.client.get('/')
//         self.assertEqual(response.status_code, 200)
    
//     def test_add_todo(self):
//         """Test adding a todo via POST"""
//         response = self.client.post('/add', data={'title': 'Test Todo'})
//         self.assertEqual(response.status_code, 302)  # Redirect after POST

// if __name__ == '__main__':
//     unittest.main()
// EOF
                        
//                         # Run unit tests
//                         python3 test_unit.py
//                         echo "Unit tests completed successfully"
//                     '''
//                 }
//             }
//         }
        
//         stage('Containerized Deployment') {
//             steps {
//                 script {
//                     echo "Deploying Application in Container..."
                    
//                     sh '''
//                         # Stop any existing containers
//                         docker-compose -p ${COMPOSE_PROJECT_NAME} down || true
                        
//                         # Start the application
//                         docker-compose -p ${COMPOSE_PROJECT_NAME} up -d
                        
//                         # Wait for application to be ready
//                         echo "Waiting for application to start..."
//                         sleep 30
                        
//                         # Check if application is running
//                         docker-compose -p ${COMPOSE_PROJECT_NAME} ps
                        
//                         # Test health endpoint
//                         for i in {1..10}; do
//                             if curl -f http://localhost:${APP_PORT}/health; then
//                                 echo "Application is healthy"
//                                 break
//                             else
//                                 echo "Attempt $i: Application not ready, waiting..."
//                                 sleep 10
//                             fi
//                         done
                        
//                         echo "Application deployed successfully"
//                     '''
//                 }
//             }
//         }
        
//         stage('Selenium Testing') {
//             steps {
//                 script {
//                     echo "Running Selenium Tests..."
                    
//                     sh '''
//                         # Build Selenium test container
//                         docker build -f Dockerfile.selenium -t selenium-tests:${BUILD_NUMBER} .
                        
//                         # Run Selenium tests
//                         docker run --rm \
//                             --network container:$(docker-compose -p ${COMPOSE_PROJECT_NAME} ps -q web) \
//                             -e APP_URL=http://localhost:3000 \
//                             -v ${WORKSPACE}/test-results:/app/test-results \
//                             selenium-tests:${BUILD_NUMBER} \
//                             python tests/test_selenium.py
                        
//                         echo "Selenium tests completed successfully"
//                     '''
//                 }
//             }
//         }
//     }
    
//     post {
//         always {
//             script {
//                 echo "Pipeline completed. Cleaning up..."
                
//                 // Clean up containers
//                 sh '''
//                     docker-compose -p ${COMPOSE_PROJECT_NAME} down || true
//                     docker rmi selenium-tests:${BUILD_NUMBER} || true
//                     docker system prune -f || true
//                 '''
//             }
//         }
        
//         success {
//             echo "✅ Pipeline completed successfully!"
//             echo "Application was built, tested, and deployed successfully."
//         }
        
//         failure {
//             echo "❌ Pipeline failed!"
//             echo "Check the logs above for error details."
//         }
//     }
// }



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
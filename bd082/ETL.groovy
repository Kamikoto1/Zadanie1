pipeline {
    agent any

    environment {
        MYSQL_HOST = 'localhost'  
        MYSQL_PORT = '3307'       
        MYSQL_USER = 'root'       
        MYSQL_PASSWORD = 'root'  
        MYSQL_DATABASE = 'mydatabase'  
        CSV_FILE_PATH = '/Users/test/Desktop/bd082/aggregated_forum_data.csv' 
    }

    stages {
        stage('Extract') {
            steps {
                script {
                    def sqlQuery = """
                    SELECT * FROM mytable;  
                    """
                    def sqlCommand = """
                    mysql -h ${MYSQL_HOST} -P ${MYSQL_PORT} -u ${MYSQL_USER} -p${MYSQL_PASSWORD} -D ${MYSQL_DATABASE} -e "${sqlQuery}" > extracted_data.txt
                    """
                    sh sqlCommand 
                }
            }
        }

        stage('Transform') {
            steps {
                script {
                   
                    def inputFile = 'extracted_data.txt'
                    def outputFile = 'transformed_data.txt'
                    
                    sh """
                    echo "Transformed Data Start" > ${outputFile}
                    cat ${inputFile} >> ${outputFile}
                    """
                }
            }
        }

        stage('Load') {
            steps {
                script {
                    def transformedFile = 'transformed_data.txt'
                    def csvOutput = "${CSV_FILE_PATH}"
                    
                    sh """
                    cat ${transformedFile} | awk '{print \$1, \$2, \$3}' > ${csvOutput}
                    """
                    echo "CSV file created at ${csvOutput}"
                }
            }
        }
    }

    post {
        always {
            cleanWs()  
        }
    }
}
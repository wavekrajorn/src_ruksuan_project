@echo off
rem Navigate to the line_api directory
cd ./line_api

rem Install npm packages
start cmd /k "npm install"

rem Start the npm application
start cmd /k "npm start"


rem Run the Python script
cd ..
start cmd /k "python ./main.py"

cd ./face_rec_v2
start cmd /k "python ./main.py"
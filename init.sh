#!/bin/bash

pip --version
npm --version

pip install requests
pip install openpyxl
pip install tqdm
pip install schedule
pip install cufflinks
pip install dataset
pip install pandas-profiling
pip install pydot
pip install chemics # https://github.com/chemics/chemics-examples
pip install gekko
pip install pony
pip install pymysql
pip install psycopg2


# Install essential library for sqltools on debian, https://github.com/mkleehammer/pyodbc/wiki/Install 
sudo apt-get update
sudo apt-get install g++ -y
sudo apt-get install unixodbc-dev -y
pip install pyodbc
## Install Linux SQL Drivers
sudo apt-get install curl -y
sudo apt-get install gnupg -y 
sudo su
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list
exit

# Adding F# and C# notebooks
# https://www.hanselman.com/blog/AnnouncingNETJupyterNotebooks.aspx

dotnet tool install --global dotnet-try
jupyter kernelspec list
dotnet try jupyter install
jupyter kernelspec list

# Added the Variable scopes  ---> https://stackoverflow.com/questions/37718907/variable-explorer-in-jupyter-notebook
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user
jupyter nbextension enable varInspector/main
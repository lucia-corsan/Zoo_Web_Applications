from website import create_app
#now we can use the website as a package

app = create_app()

#only if we run this file we are going to execute the argument
#we only will run the web server if we directly execute the file
if (__name__ == '__main__'):
   #Run will run the app and every time we make a change to the file it will rerun the server 
    app.run(debug=True)



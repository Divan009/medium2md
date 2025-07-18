# Back\-end Web Framework: Flask (Part\-3: How to make a simple Login Page using Get and Post)


2



![]()For previous posts [***Part\-1***](https://medium.com/@divadugar/web-development-back-end-with-flask-part-1-be8ecfa22abd)and [***Part\-2***](https://medium.com/@divadugar/web-development-back-end-with-flask-part-2-routing-a8ecfd828933)

HTTP protocol is the core basis of data communication in (WWW) world wide web. It is designed to communicate between clients and servers. It works as a request\-respond protocol. HTTP has different methods of data retrieval from specified URL and those methods have been defined in this protocol.

**GET:** Browser requests server to *get* data in an unencrypted form stored on that page and send it. It’s the **default** method. It can be cached and remains in browser history.

**HEAD:** It is only interested in the *headers* and not the content of the page. It is supposed to be handled as if it was a GET request but not to deliver the actual content.

**POST:** It is used to send HTML form data to be processed to a specified resource. Browser tells the server that it wants to *posts* some new data to the URL and it is only stored once. Data received by POST method is not cached by server.

**PUT:** It replaces all current representations of the target resource with the uploaded content. Similar to Post, it might trigger the store procedure multiple times by overwriting the old data. It is helpful when suppose your connection is lost during transmission. In this situation a system between the browser and the server might receive the request safely a second time without breaking things.

**DELETE:** It removes all current representations of the target resource given by a URL.

**CONNECT:** It converts the request connection to a transparent TCP/IP tunnel

By default, a route answers to `GET` requests only, but that can be changed by providing the `methods` argument to the `route()` decorator. I am just going to use here two common HTTP methods: GET and POST

For GET request `request.args.get('nm')` is used .

For POST request `request.form[‘nm’]` is used.

To collect form data we require module: **request**


```
from flask import Flask, redirect, url_for, request  
app = Flask(__name__)@app.route('/login',methods = ['POST', 'GET'])  
def login():  
   if request.method == 'POST':  
      user = request.form['nm']  
      return redirect(url_for('success',name = user))  
   else:  
      user = request.args.get('nm')  
      return redirect(url_for('success',name = user))@app.route('/success/<name>')  
def success(name):  
   return 'welcome %s' % nameif __name__ == '__main__':  
   app.run(debug = True)
```
The HTML code is


```
<html>  
<body>  
<form action = "<http://localhost:5000/login>" method="post">  
 <p> Enter Name:</p>  
 <p> <input type="text" name="nm"></p>  
 <p> <input type="submit" name="submit"></p>  
</form>  
</body>  
</html>
```
The `<http://localhost:5000/login>`is mapped to `login()` function. As the server has received the submitted data by `POST`method, value of ‘nm’ parameter obtained from the form data is by: `user = request.form[‘nm’]` . It is then passed to the `/success` URL as the variable part `/<name>` . The browser will display it on the screen.

*Thanks for reading! If you liked this article, you can* [*read my other articles here*](https://medium.com/@divadugar)*. If you like this article, please show your appreciation by* **clapping👏** *below, sharing this article and also you can also* [**follow me on Instagram**](https://www.instagram.com/diivan009/) **and** [**connect on LinkedIn**](https://www.linkedin.com/in/divajain9/)**.**

[## Diva Jain \| Coder (@diivan009\) \* Instagram photos and videos

### 204 Followers, 112 Following, 41 Posts \- See Instagram photos and videos from Diva Jain \| Coder (@diivan009\)

www.instagram.com](https://www.instagram.com/diivan009/?source=post_page-----4bacfd054fa0---------------------------------------)

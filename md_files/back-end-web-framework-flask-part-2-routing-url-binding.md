# Back\-end Web Framework: Flask (Part\-2: Routing \& URL Binding)


2



![]()Web frameworks nowadays use the routing technique to help users to navigate through a web without having to remember application URLs. It is useful to access the desired page directly without having to navigate from the home page.


```
 from flask import Flask  
 app = Flask(__name__) @app.route('/')  
     def index():  
     return 'This is homepage' @app.route('/about')  
      def about():  
      return '<h2> About page </h2>'  
   
 if __name__ == "__main__":  
     app.run(debug = True)
```
**Route()** decorator can be used to inject additional functionality to one or more functions.

`app.route(rule, option)` **Rule** represents the URL binding with the function and **option** is a list of parameters to be forwarded to the underlying **Rule** options.

`@app.route(‘/’)` This is the URL and whenever a client requests it the server will send back the return value i.e. `return ‘This is homepage’` . Now, suppose we want to go to the about page, then we write this `@app.route(‘/about’)` . This returns `return ‘<h2> About page </h2>’` . We can also put HTML codes in the return statement. `def index():` and `def about():` are functions.

`app.run(host, port, debug, option)`But we just use the debug in this example. **host** defaults to `127.0.0.1` (localhost)and Sets to ‘`0.0.0.0`’ to have server available externally

**port** defaults to 5000

**debug** defaults to false. If set to true, provides a debug information

**options** forwards to underlying Werkzeug server.

`app.run(debug = True)` when the app is under development, it should be restarted manually for each change in the code. To avoid this inconvenience, we enable the debug mode. The server then will reload itself with any changes in code. It’s also useful when there is a bug in the code and helps find errors.

There is `url_for`function which is very useful if we want a dynamically build URL.


```
from flask import Flask  
 app = Flask(__name__)@app.route('/teacher')  
     def hello_teacher():  
     return 'Hey Teacher'@app.route('/students/<student>')  
     def hello_students(student):  
     return 'Hello %s as student' %student@app.route('/user/<name>')  
     def hello_user(name):  
         if name == 'teacher':  
              return redirect(url_for('hello_teacher'))  
         else:  
              return redirect(url_for('hello_students'))if __name__ == "__main__":  
     app.run(debug = True)
```
This is a dynamic URL example

`@app.route('/user/<name>)` This here suggests the variable part `<name>` , it takes in any variable name and displays it later. If **‘teacher’** is supplied to `def hello_user(name):` function as argument. The `hello_user()` function checks if an argument received matches **‘teacher’** or not. If it matches, the application is redirected to the `hello_teacher()` function using `url_for()`, otherwise to the `hello_students()` function passing the received argument as guest parameter to it.

*Thanks for reading! If you liked this article, you can* [*read my other articles here*](https://medium.com/@divadugar)*. If you like this article, please show your appreciation by* **clapping👏** *below, sharing this article and also you can also* [**follow me on Instagram**](https://www.instagram.com/diivan009/)

[## D D (@diivan009\) \* Instagram photos and videos

### 165 Followers, 61 Following, 32 Posts \- See Instagram photos and videos from D D (@diivan009\)

www.instagram.com](https://www.instagram.com/diivan009/?source=post_page-----a8ecfd828933---------------------------------------)

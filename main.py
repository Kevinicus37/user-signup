#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import helpers

def page(username ="", mail="", name="", password="", verify="", email=""):
    head="<head><style>.error { color: red;}</style></head>"
    header = "<h1>Signup</h1>"
    username_row = """<tr>
                      <td><label for='username'>Username</label></td>
                      <td><input type='text' name='username' value='%(username)s' required>
                      <span class='error'>%(name)s</span>
                      </td>
                      </tr>"""
    password_row = """<tr><td><label for='password'>Password</label></td>
                      <td><input type='password' name='password' required>
                      <span class='error'>%(password)s<span>
                      </td>
                      </tr>"""
    verify_row = """<tr><td><label for='verify'>Verify Password</label></td>
                    <td><input type='password' name='verify_password' required>
                    <span class='error'>%(verify)s</span>
                    </td>
                    </tr>"""
    email_row = """<tr><td><label for='email'>Email (optional)</label></td>
                   <td><input type='email' name='email' value ='%(mail)s' optional>
                   <span class='error'>%(email)s</span>
                   </td>
                   </tr>"""

    form = "<body>" + head + header + "<form method='post'><table>" + username_row + password_row + verify_row + email_row + "</table><input type='submit'></form>"+ "</body>"

    return form % {'username': username, 'mail':mail, 'name': name, 'password': password, 'verify': verify, 'email': email}

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(page())

    def post(self):
        have_error = False
        username = self.request.get('username')
        password= self.request.get('password')
        verify = self.request.get('verify_password')
        email = self.request.get('email')

        params = dict(username = username, mail = email)

        if not helpers.valid_username(username):
            params['name']="That's not a valid username."
            have_error = True

        if not helpers.valid_password(password):
            params['password']="That's wasn't a valid password."
            have_error = True
        elif password != verify:
            params['verify'] = "Your passwords did not match."
            have_error = True

        if not helpers.valid_email(email):
            params['email'] = "That is not a valid email, stupid."
            have_error = True

        if have_error:
            self.response.write(page(**params))
        else:
            self.redirect('/welcome?username=' + username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        if helpers.valid_username(username):
            self.response.write('Welcome, ' + username + '!')
        else:
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/welcome', Welcome)
], debug=True)

import datetime
import logging
import os
from google.appengine.ext import db

class Session(db.Model):
  pages = db.StringListProperty(default = [ ])

def hit(client_id, referrer):
  try:
    id = int(client_id)
  except ValueError:
    return
  
  def txn():
    sess = Session.get_by_id(id)
    sess.pages.append(referrer)
    sess.put()
    return sess.pages
  
  return db.run_in_transaction(txn)

def main():
  if os.environ['PATH_INFO'].startswith('/track/'):
    print 'Status: 200 Okay'
    print 'Content-type: text/html'
    print 'Cache-Control: no-cache; must-revalidate'
    print 'Expires: Tue, 15 Nov 1994 12:45:26 GMT'
    print
    
    print repr(hit(os.environ['PATH_INFO'][7:], os.environ.get('HTTP_REFERER', '')))
  
  elif os.environ['PATH_INFO'] == '/bug':
    if 'HTTP_IF_MODIFIED_SINCE' in os.environ and false:
      print 'Status: 304 Not Modified'
      return
    
    sess = Session()
    sess.put()
    
    print 'Status: 303 Redirect'
    print 'Content-type: text/html'
    print 'Cache-Control: public, max-age=99936000'
    print 'Last-Modified: Tue, 15 Nov 1994 12:45:26 GMT'
    print 'Expires: Sun, 01 Dec 2030 16:00:00 GMT'
    print 'Location: /track/%i' % sess.key().id()
    print
  
  else:
    print 'Status: 404 File Not Found'

if __name__ == '__main__':
  main()
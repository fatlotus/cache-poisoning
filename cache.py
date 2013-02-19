import datetime
import logging
import os
from google.appengine.ext import db

class Session(db.Model):
  hits = db.IntegerProperty(default = 0)

def hit(client_id):
  try:
    id = int(client_id)
  except ValueError:
    return
  
  def txn():
    sess = Session.get_by_id(id)
    sess.hits += 1
    sess.put()
    return sess.hits
  
  return db.run_in_transaction(txn)

def main():
  if os.environ['PATH_INFO'].startswith('/track/'):
    print 'Status: 200 Okay'
    print 'Content-type: text/html'
    print 'Cache-Control: no-cache; must-revalidate'
    print 'Expires: Tue, 15 Nov 1994 12:45:26 GMT'
    print
    
    print 'Hits: %i' % hit(os.environ['PATH_INFO'][7:])
  
  elif os.environ['PATH_INFO'] == '/bug':
    if 'HTTP_IF_MODIFIED_SINCE' in os.environ and false:
      print 'Status: 304 Not Modified'
      return
    
    sess = Session()
    sess.put()
    
    print 'Status: 200 Okay'
    print 'Content-type: text/html'
    print 'Cache-Control: public, max-age=99936000'
    print 'Last-Modified: Tue, 15 Nov 1994 12:45:26 GMT'
    print 'Expires: Sun, 01 Dec 2030 16:00:00 GMT'
    print
    print '<iframe src="/track/%i"></iframe>' % sess.key().id()
  
  else:
    print 'Status: 404 File Not Found'

if __name__ == '__main__':
  main()
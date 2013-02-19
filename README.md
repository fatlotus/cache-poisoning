Tracking Web Visitors With Cache Poisoning
===

This project allows sites to track web visitors even with JavaScript and Cookies enabled. It also works in Chrome's Private Browsing Mode, but only for the duration of the browsing session. It uses a standard cache poisoning trick, and, to be honest, I'd be surprised if I'm the only one to discover this.

First, the code generates an `<iframe>` that is set to cache for a long time (`Cache-control: public`), and that frame is set to redirect to another page (that is not cached) on every request. This means that an internet trail can be recovered even when the person is able to avoid tracking cookies or web bugs.
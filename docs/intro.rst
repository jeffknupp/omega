Introduction to Whizbang
========================

Whizbang is a web application suite that gives you the tools required to build
vastly different types of modern web applications. Here are a few of the
types of applications Whizbang makes it easy to create:

* Static sites or dynamic sites that don't require storage
* NoSQL-based REST APIs
* CRUD sites using an ORM to interface with a traditional relational database
* Real-time sites using websockets

In order to allow you to build such different types of sites, whizbang offers
functionality generally found in some webframeworks plus a number of tools found
in almost none. For example, Whizbang provides:

* A pure-Python Key/Value store using ZeroMQ for transport
* A logging/statistics service that centralizes collection and display of
  metrics
* A search module that allows for efficient, indexed searching in pure Python
* A distributed task queue with *cron*-like functionality as well as the ability
  to asynchronously complete tasks launched over the network (again, using
  ZeroMQ for transport).

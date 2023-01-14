# Parcel Pickup Point Search API
Simple fastapi app to search and manage packages/mail drop points. Database agnostic, in current implementation using elasticsearch as data source.

Supports creating, updating, deleting parcel pickup points, user authorization and roles, searching near points by given location and range (in kilometers). 

Application is using async processing, custom logging implemented (currently using loguru). You can implement own data importers or use other data sources by using dedictated interfaces. If you wish it's possible to extend users management by overriding fastpi-user lib, also currently sqlite is using as data source for user management. 


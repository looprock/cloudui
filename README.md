An abstraction layer webui/API for managing 'clusters'
=======

cloudui is a django app written to be a FE/API/source of truth for development 'clusters' of virtual machines.

It's two main functionalities are to provide an interface to trigger and poll rundeck jobs that create, redeploy to, and delete sets of servers, and to provide data about cluster membership.

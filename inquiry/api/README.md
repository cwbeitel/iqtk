
# Inquiry API

**Status: Work in progress**

This section contains modules representing the various routes of the Inquiry API to be deployed on Fission. These docs assume you have deployed fission according to the [fission installation documentation](http://fission.io/docs/v0.2.1/install/) so give that a try first if you haven't already.

From there the API functions/modules can be deployed using `deploy.sh` in this directory as described below.

### Initial deployment of functions

Before a function can be exposed as a route via fission the code for that function must be registered with fission. For our routes that's done with the following:

```bash

fission function create --name run --env python --code run.py
fission function create --name list --env python --code list.py
fission function create --name describe --env python --code describe.py
fission function create --name health --env python --code health.py

```

At this point functions have just been stored by fission with an associated name.

### Initial deployment of routes

In order to run our functions we next need to create the HTTP routes that will relate URL's to each of these.

```bash

fission route create --method POST --url /run --function run
fission route create --method POST --url /list --function list
fission route create --method POST --url /describe --function describe
fission route create --method GET --url /health --function health

```

When a request comes in on a specified route the main() function of the module referenced by the function name (--function) parameter will run.

### Updating functions (and therefore routes)

In the process of development we'll probably need to update the code stored for a certain function. This can be done as follows:

```bash

fission function update --name run --env python --code run.py
fission function update --name list --env python --code list.py
fission function update --name describe --env python --code describe.py
fission function update --name health --env python --code health.py

```

Routes stay the same and it's just the function code that changes.

### Testing the routes

Next we want to test our routes. We can start by streaming logs from a particular function before we send a request to it which can be done as follows

```bash

fission function logs --name [function name] --follow

```

*Get the health/status of the api system (?):*

```bash

curl -X GET -H "Content-Type: application/json" http://$FISSION_ROUTER/health
function 'health' updated
{"hp": 100}%

```

*List past and current workflow runs given some query (illustrative):*

```bash

curl -X POST -d "{'started_after': 'yesterday'}" -H "Content-Type: application/json" http://$FISSION_ROUTER/list
[{"body": "something", "created": "long time ago"}, {"body": "lots of things", "created": "recently"}]%

```

*Describe an individual workflow (illustrative):*

```bash

curl -X POST -d "@example.json" -H "Content-Type: application/json" http://$FISSION_ROUTER/describe
{"created": "long time ago", "body": "something"}%

```

*Submit a workflow:*

```bash

curl -X POST -d "@example.json" -H "Content-Type: application/json" http://$FISSION_ROUTER/run

```

“IBM” Photos
============

This project is *not* owned by IBM.

An online photo gallery that allows you to search photos by boolean
expressions on existence of objects on them.

Example query: `person & ~horse`.

Syntax: `&`, `|`, `~` (not), `(`, `)`, `<object>`.

[Supported objects](https://gist.github.com/AruniRC/7b3dadd004da04c80198557db5da4bda)
– sans those that have space inside the name (e.g. "baseball bat").

Only processed photos are shown in the gallery, so they might 
not appear immediately after uploading.

Architecture
------------
k8s pods:
* `ibm-photos-front`: nginx with compiled static files, also serves
  media (via a shared PVC mount) & passes API requests to backend.
* `ibm-photos-back`: uwsgi that hosts django. Media files saved
  ot shared PVC mount. Can be scaled horizontally.
* `ibm-photos-celery-beat`: collects unfinished tasks from the db
  and schedules them to be run by workers.
* `ibm-photos-celery-worker`: does the work. Could be scaled
  horizontally after adjusting job scheduling.
* `redis`: ephermal celery work queue
* `ibm-postgres-dev`: ephermal ( :( ) db
* `ibm-object-storage-plugin`: what the name says.

A [public demo deployment](http://max-object-detector.max.us-south.containers.appdomain.cloud)
of [MAX Object Detector](https://developer.ibm.com/exchanges/models/all/max-object-detector/)
is used.

I did not use [IBM Cloud Visual Recognition](https://cloud.ibm.com/catalog/services/visual-recognition)
as I needed to find multiple objects per photo, not classify
photos.

Deployment
----------
1. Create k8s service in IBM Cloud, build, tag, and upload `back`
   & `front` docker images. [Some help](https://github.com/phthom/ContainerOrchestration/blob/master/3-KubernetesLab.md).
2. [Setup object storage tier for photos storage](https://cloud.ibm.com/docs/containers?topic=containers-object_storage)
3. `cd k8photos`
4. [Install Tiler, add some repos](https://github.com/phthom/ContainerOrchestration/blob/master/4-HelmLab.md)
  (look at `dependencies.yaml` to see which repos to add)
5. `kubectl create namespace photos-test`
6. `kubectl apply -n photos-test -f manual-media-volume-claim.yaml`
7. `helm install --name=photos --namespace photos-test .`
8. Get the public IP from k8s IBM dashboard (ignore the one
   shown by k8s cli) & port from `photos-ibm-photos-front`.
9. Profit.

Uploading photos via API
------------------------
1. Log in via `/admin`.
2. Create an API token in django admin.
3. `/api/photo`.

Possible improvements
---------------------
* Make the database persistent. I don't have access to block
  storage nor managed postgresql on the lite tier. Object
  storage would have too big latency for a db.
* Make the query language more lax, support spaces inside object
  class names.
* Improve query performance by using [native bitmaps](https://github.com/Ezibenroc/PyRoaringBitMap)
  for boolean set operations. The bitmaps could be cached in RAM
  and invalidated on new image arrival/image removal.
* Remove the random unused nginx container from deployment.
* Deploy the ML model instead of using a public demo.
* Use a better ML model. Some options listed in `res.txt`.
* Don't have the admin password cleartext in the repo.
* Travis for auto deployments.
* Publish images to a public registry.
* Create [ingress](https://cloud.ibm.com/docs/containers?topic=containers-ingress)
  for SSL & domain support. Would do it now, but can't due
  to lite.
* CDN for photos.
* Display objects for each image in the gallery.

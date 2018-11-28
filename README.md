Script to teach classificationbox image classes as described in
https://blog.machinebox.io/how-anyone-can-build-a-machine-learning-image-classifier-from-photos-on-your-hard-drive-very-5c20c6f2764f

This script is therefore a python implementation of
https://github.com/machinebox/toys/blob/master/imgclass/main.go

First create a model using CURL:
```CURL
$ curl -XPOST --header "Content-Type: application/json" --header "Accept: application/json"  http://localhost:8080/classificationbox/models --data '{
    "id": "sentiment1",
    "name": "sentimentModel",
    "options": {
        "ngrams": 1,
        "skipgrams": 1
    },
    "classes": [
        "class1",
        "class2",
        "class3"
    ]
}
```
You can check what models you have available:
```CURL
curl -XPOST --header "Content-Type: application/json" --header "Accept: application/json"  http://localhost:8080/classificationbox/models
```

Then run the script `teach_classificationbox.py` from within the root folder containing the folders of images.

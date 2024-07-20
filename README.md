# Pixar_flask

# run
```sh
cd Pixar_flask

source env/venv/bin/activate

gunicorn --timeout 300 -w 4 -b 0.0.0.0:8000 app:app
```

# test(postman)
```sh
http://213.173.110.211:16307/post_endpoint

{
   "image_base":"",
    "num_avatars":1,
    "crop":"center",
    "generate_prompt_from_image":"False",
    "device":"cuda"
}
```

# Recipes API exercise

## How to use it

Clone the repository:

```sh
$ git clone https://github.com/angel-tk/tk-recipe-backend.git
$ cd tk-recipe-backend
```

Build the docker image:

```sh
$ docker-compose build
```

Then run the server:

```sh
$ docker-compose up
```

Test the API sending your requests to the root URL `http://127.0.0.1:8000/`.
The following availabe endpoints are available:

- Get all the recipes
  - **GET** /recipes/
- Filter recipes by name
  - **GET** /recipes/?name=`name of the recipe`/
- Get recipe by key
  - **GET** /recipes/`id number`/
- Create new recipe
  - **POST** /recipes/
- Edit a recipe
  - **PATCH** /recipes/`id number`/
- Partially edit a recipe
  - **PUT** /recipes/`id number`/
- Delete a recipe
  - **DELETE** /recipes/`id number`/

## Example recipe list

GET /recipes/

    [
      {
        "id": 1,
        "name": "Mac and cheese"
        "description": "Cook macaroni pasta and add cheddar. Put it in the oven. Springle some black pepper. Alternatively, you can watch episode 5 of season 11 of It's Always Sunny in Philadelphia to learn how to prepare the variant Mac's Famous Mac and Cheese.",
        "ingredients": [{"name": "macaroni"}, {"name": "cheddar"}, {"name": "black pepper"}]
        }
    ]

## Testing

Run the following command to check the tests:

```sh
docker-compose run --rm app sh -c "python manage.py test"
```

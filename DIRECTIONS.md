# Assignment

In this assignment you are going to build an API that communicates with a database. We will be using Python & FastAPI to write the API. You will then need to build a simple frontend application using Next.js to communicate with the API.

## API

We have provided you some boilerplate code for the API and it is located in `server/main.py`. This is the only file for the API. You will need to add code here for implementing each API route. The API connects to a database that is setup through Docker and docker compose. It has been configured to automatically load in the data so that the database is pre-filled with 1000 rows of data. The boilerplate code of the assignment has also been setup to connect to the database for you so that you do not need to do that.

The boilerplate code also only setups up a connection to the postgres database, it does not use an ORM so you will have to write raw SQL statements to accomplish the desired functionality.

### Running the API

The API is setup to run on port `3000` but you should change this to use another port, like 5001 so requests should be made to `localhost:5001` (or whatever port you use) when running the API.

1. Ensure you have `pipenv` installed https://pipenv.pypa.io/en/latest/installation.html. Note: this requires PIP to install Pipenv, they are different tools however.
2. Run `docker compose up` and wait for the container to start. This is your database
3. Navigate to the `server` folder and run `pipenv install` followed by `pipenv run python main.py`
4. Open another terminal and run `npm run dev` and read the output to make sure that the API started without any errors. 
   1. This command will start the server and watch the files. This means that it will re-load and re-start the server each time you edit a file(Similar to what happens in Next.js)
5. You're ready to start working. Keep in mind that you both your docker container running and the server running to have the API function. If you close the terminal, the processes will stop.

### Learning

- https://www.youtube.com/watch?v=0RS9W8MtZe4

If you prefer reading:
 - https://fastapi.tiangolo.com/learn/

## Database

We have setup the database for you. When you start the docker container, it auto-fills the database with the data stored in the `products_data.csv` file. There is only one table called `products` in the `product_db` database(one database server can host more than one database).

### Detailed Description[LLM Supported]

1. **Table Name**:
   - The table is named `products`.

2. **Columns**:
   - `id`: This is the primary key for the table, which will uniquely identify each record. The `SERIAL` data type is used, which is an auto-incrementing integer, ensuring that each new record will have a unique `id`.
   - `name`: This column stores the name of the product, with a maximum character limit of 255.
   - `description`: This column is designated for storing textual descriptions of the products. The `TEXT` data type allows for storing longer strings.
   - `price`: This column holds the price of the products. It's defined as a decimal number with up to 10 digits, 2 of which can be after the decimal point, allowing for precise pricing information.
   - `created_at`: This column records the timestamp when a product record is created. By default, it is set to the current timestamp at the time of record creation (`NOW()` function is used for this).

3. **Primary Key**:
   - The `id` column is set as the primary key of the table, ensuring data integrity and uniqueness of records.

4. **Defaults**:
   - The `created_at` column has a default value set to the current timestamp at the time of record creation, using the `NOW()` function.

## Frontend

You will need to build a basic frontend that allows the user to input an ID of a product in the database and it will retrieve it. The design of this page is not important. You need to use components from the Antd library to build this feature though.

### Running the frontend

This is a standard Next.js application. `npm install` and `npm run dev` will get things started, you should be presented with some "Hello World" text.

## Tasks

1. After starting the API, make a  request to `localhost:5000/` [or whatever port is specified in `main.py`] to make sure the API is working. You should get "Hello World! Database connection is successful." as a response. You can find the definition of this route in the top of the `main.py` file
2. Write an API route get the total number of items in the database table called `products`. This route should be a GET request and only return the count of items in the table.
   1. The route path should be `/products/count`
3. Write a route to get a specific item from the `products` table based on the ID of the items.
   1. The API route should correctly handle errors such as, product not found(read the HTTP status code doc to see which code is appropriate for this) and internal server errors(some other error occurred while performing the query)
   2. The product ID that is being selected should be passed as part of the URL. For example `/products/55`, specifically it will be part of the URL parameters. See the fastapi docs here: https://fastapi.tiangolo.com/tutorial/first-steps/ and https://fastapi.tiangolo.com/tutorial/query-params/
4. Write an API route that returns all items in the database in a paginated form using `page` and `limit`(similar to API in previous assignment). It should have a default `page` of 1 and a `limit` of 10.
   1. Hint: Start with a simple SQL query that returns everything and then add on the pagination support
   2. Hint: You'll need to use the SQL keywords `limit` and `offset` to accomplish this in your query.
   3. Required: Handle a server error and return a `500` code if anything goes wrong
   4. Required: The `page` and `limit` properties of the request should be passed as query parameters.
5. Build a simple frontend that allows users to retrieve a product by the ID. 
   1. There should be a text field that accepts an input(it does not need to be validated) and a button to "search" upon which you can query the API for the data and display the results.
   2. Required: Handle the response from the API, both success(display the product) and error(not found, server error etc)
   3. Note: The design is not important, you must use Antd components but colors, spacing etc is not important.

### Bonus [5% Each]

1. Write a route that allows the user to search the products based on keywords. It should search the title field of products and return 0-n results depending on if anything matched. Also, implement this feature in the frontend, allowing the user to input their query in a text box and then show the result(s) on the screen after querying the API.
2. Implement an API route that allows the user to create a new product. It should accept, title and description. The rest should be generated by the database. This must be a POST/PUT request. In addition, you must implement this feature in the frontend.

# BigAuction
BigAuction is an ecommerce website built with mongoDB and Flask. Users can sign in and purchase items or sell items. Users will also see notifications for when another user buys one of their items. The rendering is done with Jinja which is built into Flask. 

# User Authentication
User authentication is done with bcrypt which generates a hashed password which is then stored in the database and used as a reference when users try logging in. If a user does not exist or the password is incorrect, a flash() is called which renders new html onto the page to tell the user that message. 

# Store
Random image urls, names and descriptions were generated and automated into the database, thereby creating a virtual store. The store is split into many sections meaning that a user can naviagate through different categories to search for a specific product. It is also possible to sort products by the amount or price. The sorting is done based on information from a query string that execeutes a sorting algorithm on the backend if conditions are correct. 

# Search Engine
The search engine aspect was accomplished with a database query and then a simple filtering system. For example, if a user searched "ring", the algorithm would query through all products and check if the word "ring" was in the name, category or description of that product. After the filtering is complete, the products that meet the requirements of the search will be rendered with the Jinja rendering template. 

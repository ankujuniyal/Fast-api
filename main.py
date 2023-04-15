#IMPORTING LIBRARIES
from typing import Optional
from fastapi import FastAPI, Response , status, HTTPException
# from fastapi.params import Body 
from pydantic import BaseModel
from random import randrange
import uvicorn
#creating classs
app = FastAPI()

#creating a class to define schema for post
#this will do all the validation
class Post(BaseModel):
     Title: str
     content: str
     published: bool=True
     rating: Optional[int]=True #give optional rating but has to be integer
     
#creating an array to store posts in memory
my_posts=[{"Title:":"First post", "content:":"content of post 1", "id":1},{"Title:":"Favorite food", "content:":"Pizza", "id":2}]

#Path operation, instance of class FastAPI.
@app.get("/") 
async def root():
    return {"message": "Hello World"}

#------------old-----------------
#creating function to retrieve data
#@app.get("/posts")
#def get_posts():
#    return{"Data": "This is your post"}

#------------new----------------

#Creating function to retrieve data
@app.get("/posts")
def get_posts():
    new_var = "This is your post"
    return{"Data": my_posts}

#to ectract the particular post by id from list of posts
def find_post(id):
     for p in my_posts:
          if p['id']==id:
               return p
          

#creating function to send data to api server


#-----------old method------------
#@app.post("/createposts")
#def create_post(payload: dict= Body(...)):
        #print(payload)
        #return {"newpost": f"Title: {payload['Title']} content:{payload['content']}"} 

#-----------new method with schema-----------
@app.post("/posts",status_code=status.HTTP_201_CREATED)#status code for creating post
def create_post(new_post: Post): #creating a variable to reference class(Post) we created before
        #print(new_post)
        new_post_dict = new_post.dict() 
        new_post_dict['id']= randrange(0,1000000) #calling id and storing a random number onto it
        print(new_post.dict()) #converitng to a python dictionary
        my_posts.append(new_post_dict)
        return {"data": new_post_dict} 

#path parameter to fetch detial for a particular id input
@app.get("/posts/{id}")
def get_post(id:int, response:Response): #Converting id to integer, response variable for http 404 exc
     post=find_post(id)
     if not post: #incase user inputs an invalid number as id
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
     print(post)
     return{"post detail:": post}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)

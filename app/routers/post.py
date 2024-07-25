from .. import models, schemas, utils
from ..database import engine, get_db
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import oauth2
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Post']
)

@router.get("/", response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(get_db),limit: int = 10, skip: int = 0, search: Optional[str]=""):
    # cur.execute(""" SELECT * FROM posts """)
    # posts = cur.fetchall()
    #post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = (
    db.query(models.Post, func.count(models.Votes.post_id).label("votes"))
    .outerjoin(models.Votes, models.Votes.post_id == models.Post.id)
    .group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
     .all()
)
    return results

    

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), get_current_user: int =Depends(oauth2.get_current_user)):
#     cur.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
#                 (post.title, post.content,post.published))
#     new_post = cur.fetchone()
#     conn.commit()
#     return(new_post)
    print(get_current_user.email)
    new_post = models.Post(owner_id = get_current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return(new_post)


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cur.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cur.fetchone()
    # print (post)
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
           detail=f"Post with id: {id} was not found, therefore not found.")

    
    return(post)



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), get_current_user: int =Depends(oauth2.get_current_user)):    
    # cur.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # conn.commit()
    # deleted_post = cur.fetchone()

    post=db.query(models.Post).filter(models.Post.id==id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"Post with id: {id} was not found, therefore not updated.") 
    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized")  
    db.delete(post) 
    db.commit()
    return(post)

@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), get_current_user: int =Depends(oauth2.get_current_user)):
    # cur.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *  """, 
    #             (post.title, post.content, post.published, str(id)))
    # conn.commit()
    # updated_post = cur.fetchone()
    existing_post=db.query(models.Post).filter(models.Post.id==id).first()
    if existing_post== None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"Post with id: {id} was not found, therefore not updated.")
    if existing_post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized")  

    existing_post.title = post.title
    existing_post.content = post.content
    db.commit()
    return(existing_post) 
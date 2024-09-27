from fastapi import APIRouter, HTTPException, status, Depends
from app.models.models import User
from app.core.security import get_current_user
from app.db.mongodb import find_object, get_object
from app.db.minio import get_url_from_minio

router = APIRouter()

@router.get("/all", response_model=dict, description="Get all subjects with their details")
async def get_subjects(
    current_user: User = Depends(get_current_user)
):
    print(current_user)
    class_name = current_user["class_name"]
    className = await find_object("className", {"name": class_name})
    data = className
    if not className:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")

    for ind, subject in enumerate(className["subjects"]):

        data['subjects'][ind]= await get_object("subject", subject)

        for ind2, book in enumerate(className["subjects"][ind]["books"]):

            data['subjects'][ind]['books'][ind2] = await get_object("book", book)

            for ind3, topic in enumerate(className["subjects"][ind]["books"][ind2]["topics"]):

                data['subjects'][ind]['books'][ind2]['topics'][ind3] = await get_object("topic", topic)
                data['subjects'][ind]['books'][ind2]['topics'][ind3].pop('book_location')
    return data

@router.get("/topics/pdf/{id}", description="Get a pdf file")
async def get_pdf(
    id=id,
    current_user: User = Depends(get_current_user)
):
    data = await get_object("topic", id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    url = await get_url_from_minio(data["book_location"])
    print(url)
    return {"url": url}
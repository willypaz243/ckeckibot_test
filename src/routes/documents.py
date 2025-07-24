from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile

from src.routes.deps import VectorStoreManagerDep

docs_router = APIRouter(prefix="/documents", tags=["Documents"])


@docs_router.post("/upload")
async def upload_document(
    file: UploadFile,
    vectorestore_manager: VectorStoreManagerDep = Depends(),
):
    filename, ext = file.filename.split(".")
    if file.content_type not in ["text/csv", "application/json"]:
        raise HTTPException(status_code=400, detail="File must be a csv or json")
    now = datetime.now(UTC)
    now.strftime("%Y-%m-%d_%H_%M_%S")
    filename = f"{filename}_{now.strftime('%Y-%m-%d_%H_%M_%S')}.{ext}"
    _bytes = await file.read()
    await vectorestore_manager.add_document(filename, _bytes)
    return {"success": True, "filename": filename}


@docs_router.get("/list")
async def list_documents(
    vectorstore_manager: VectorStoreManagerDep = Depends(),
):
    documents = vectorstore_manager.list_documents()
    return {"documents": documents}


@docs_router.delete("/{filename}")
async def delete_document(
    filename: str,
    vectorstore_manager: VectorStoreManagerDep = Depends(),
):
    success = await vectorstore_manager.delete_document(filename)
    if success:
        return {"success": True}
    else:
        raise HTTPException(status_code=404, detail="Document not found")

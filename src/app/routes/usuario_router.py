from fastapi import APIRouter

from src.app.models.usuario import Usuario
from src.app.repositories.usuario_repository import UsuarioRepository

usuario_router = APIRouter()
usuario_router.prefix = "/api/usuarios"
usuario_router.tags = ["Usuários"]

usuario_repository = UsuarioRepository()

@usuario_router.post("/")
def create_usuario(usuario: Usuario):
    return usuario_repository.create(usuario)

@usuario_router.get("/")
def get_usuarios():
    return usuario_repository.get_all()

@usuario_router.get("/{usuario_id}")
def get_usuario_by_id(usuario_id: int):
    return usuario_repository.get_by_id(usuario_id)

@usuario_router.put("/{usuario_id}")
def update_usuario(usuario_id: int, usuario_data: dict):
    return usuario_repository.update(usuario_id, usuario_data)

@usuario_router.delete("/{usuario_id}")
def delete_usuario(usuario_id: int):
    return usuario_repository.delete(usuario_id)
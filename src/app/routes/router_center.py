from fastapi.routing import APIRouter

from src.app.routes.usuario_router import usuario_router
from src.app.routes.contrato_router import contrato_router
from src.app.routes.veiculo_router import veiculo_router
from src.app.routes.veiculo_manutencao_router import veiculo_manutencao_router
from src.app.routes.manutencao_router import manutencao_router
from src.app.routes.pagamento_router import pagamento_router

router = APIRouter()

router.include_router(usuario_router)
router.include_router(contrato_router)
router.include_router(veiculo_router)
router.include_router(veiculo_manutencao_router)
router.include_router(manutencao_router)
router.include_router(pagamento_router)

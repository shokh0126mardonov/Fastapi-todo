from fastapi.routing import APIRouter

router = APIRouter()


@router.get('/')
def home():
    return {'message': 'hello world'}
    
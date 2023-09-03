from flask import Blueprint

 
home_bp = Blueprint('home', __name__)
from . import home  
auth_bp = Blueprint('auth', __name__)
from . import auth 
publicar_duda_bp = Blueprint('publicar_duda', __name__)
from . import publicar_duda  
explorar_bp = Blueprint('explorar', __name__)
from . import explorar  
perfil_bp = Blueprint('perfil', __name__)
from . import perfil  
detalle_duda_bp = Blueprint('detalle_duda', __name__)
from . import detalle_duda 
 

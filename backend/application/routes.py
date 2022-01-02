from application import app
from .services import *

tv_bedroom = Tv('192.168.0.133', 'bedroom')


@app.route('/tv', methods=['POST'])
def control_tv():
    getattr(tv_bedroom,'connect_to')()
    return 'oks'

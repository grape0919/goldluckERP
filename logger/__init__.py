import logging
from logging import handlers
import json
from logging import Logger, INFO, ERROR, WARNING, DEBUG, getLevelName
from db.models import KpmgUser
from inspect import currentframe
from datetime import datetime
from fastapi import Request, Response
class KpmgLogger(Logger):
    
    def kpmgLog(self, level:int, msg, request:Request=None, response:Response=None, kpmgUser:KpmgUser=None):
        levelName = getLevelName(level)
        if levelName == INFO:
            log_method = self.info
        elif levelName == WARNING:
            log_method = self.warning
        elif levelName == ERROR:
            log_method = self.error
        elif levelName == DEBUG:
            log_method = self.debug
        else:
            log_method = self.info
        
        callMethodName = currentframe().f_back.f_code.co_name
        extra={"call_method":callMethodName}
        
        if kpmgUser:
            uesrInfo = {c.name: getattr(kpmgUser, c.name) for c in kpmgUser.__table__.columns}
            del uesrInfo["thumbnail"]
            del uesrInfo["last_login_date"]
            del uesrInfo["is_activate"]
            extra.update({
                "user": json.dumps(uesrInfo)
            })
        else:
            extra.update({
                "user":"null"})
            
            
        temp_msg = {
            "message":f"{msg}"
        }
        extra['host'] = "unknown"
        extra['agent'] = "unknown"
        extra['endpoint'] = "null"
        extra['method'] = "null"
        extra['token'] = "null"
        if request:
            if request.client:
                extra['host'] = request.client.host
                
            if request.headers:
                extra['agent'] = request.headers.get("User-Agent")
                
            if request.scope:
                extra['endpoint'] = request.scope['path']
                extra['method'] = request.scope['method']
            
            if request.cookies:
                extra['token'] = request.cookies.get('token')    
            
            temp_msg.update({"request":{}})
            if request.query_params:
                temp_msg['request']["query_param"] = dict(request.query_params)
                
            if hasattr(request, "_form") and request._form:
                input_param = dict(request._form)
                if 'file' in input_param:
                    input_param['file'] = input_param['file'].filename
                temp_msg['request']["input_param"] = input_param
                
                
        if response:
            response_temp = response
            if isinstance(response_temp, Response):
                response_temp = response_temp.body.decode(response_temp.charset)
            temp_msg.update({"response":response_temp})
        
        msg_json = json.dumps(temp_msg, ensure_ascii=False)
        log_method(msg_json, extra=extra)    
    

logging.setLoggerClass(KpmgLogger)

logger = logging.getLogger("KPMGSftLogger")
formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(host)s | %(user)s | %(agent)s | %(token)s | %(method)s %(endpoint)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
fileHandler = handlers.TimedRotatingFileHandler(filename='logs/sft_app.log', interval=1, when='D', encoding='utf-8')
fileHandler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(fileHandler)

def getLogger(loggerName) -> KpmgLogger:
    
    return logger

# logging.basicConfig()
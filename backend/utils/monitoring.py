import logging
import time
import psutil
from prometheus_client import Counter, Gauge, Histogram, start_http_server
from functools import wraps

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 定义Prometheus指标
REQUEST_COUNT = Counter('app_requests_total', 'Total number of requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('app_request_duration_seconds', 'Request latency', ['method', 'endpoint'])
ACTIVE_REQUESTS = Gauge('app_active_requests', 'Number of active requests')
MEMORY_USAGE = Gauge('app_memory_usage_bytes', 'Memory usage in bytes')
CPU_USAGE = Gauge('app_cpu_usage_percent', 'CPU usage percentage')
DB_CONNECTIONS = Gauge('app_db_connections', 'Number of database connections')

# 监控装饰器
def monitor_request(f):
    """监控请求装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request = args[0]
        method = request.method
        endpoint = request.path
        
        # 增加活跃请求计数
        ACTIVE_REQUESTS.inc()
        
        # 记录开始时间
        start_time = time.time()
        
        try:
            # 执行请求
            response = f(*args, **kwargs)
            status_code = response[1] if isinstance(response, tuple) else 200
        except Exception as e:
            # 记录异常
            logger.error(f"Error processing request {method} {endpoint}: {str(e)}")
            status_code = 500
            raise
        finally:
            # 计算延迟
            latency = time.time() - start_time
            
            # 记录指标
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status_code).inc()
            REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(latency)
            
            # 减少活跃请求计数
            ACTIVE_REQUESTS.dec()
            
            # 记录日志
            logger.info(f"{method} {endpoint} - {status_code} - {latency:.4f}s")
        
        return response
    return decorated_function

# 系统指标收集器
def collect_system_metrics():
    """收集系统指标"""
    # 收集内存使用情况
    memory = psutil.virtual_memory()
    MEMORY_USAGE.set(memory.used)
    
    # 收集CPU使用情况
    cpu = psutil.cpu_percent(interval=1)
    CPU_USAGE.set(cpu)

# 启动Prometheus服务器
def start_monitoring_server(port=8000):
    """启动监控服务器"""
    start_http_server(port)
    logger.info(f"Prometheus metrics server started on port {port}")

# 健康检查
def health_check():
    """健康检查"""
    # 收集系统指标
    collect_system_metrics()
    
    # 检查应用状态
    status = {
        'status': 'healthy',
        'timestamp': time.time(),
        'system': {
            'memory_usage': MEMORY_USAGE._value.get(),
            'cpu_usage': CPU_USAGE._value.get(),
            'active_requests': ACTIVE_REQUESTS._value.get()
        }
    }
    
    return status

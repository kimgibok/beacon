from deco import time_logger
import time

@time_logger('funtime')
def pay():
    time.sleep(5)
    print("결제되었습니다.")
    
pay()
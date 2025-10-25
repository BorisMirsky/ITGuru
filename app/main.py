from models import *
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from fastapi import Depends, FastAPI, Body, Request, Query
from fastapi.responses import JSONResponse, FileResponse
from pydantic import create_model
import asyncio



"""
Метод должен принимать ID заказа, ID номенклатуры и количество. Если товар уже
есть в заказе, его количество должно увеличиваться, а не создаваться новая позиция.
Если товара нет в наличии то должна возвращаться соответствующая ошибка
"""

app = FastAPI()

# сессия подключения к бд
SessionLocal = sessionmaker(autoflush=False, bind=engine)

# определяем зависимость
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





@app.put("/add_product_to_order")
async def edit_order(data = Body(), db: Session = Depends(get_db)):
    order_id = data["order_id"]
    product_id = data["product_id"]
    required_product_count = data["product_count"]
    order = db.query(Order).filter(Order.Id == order_id).first()
    product = db.query(Product).filter(Product.Id == product_id).first()
    orderProducts = db.query(OrderProducts).filter(OrderProducts.Order_id == order_id).first() # все строки одного заказа
    product_in_order = False      # флаг 'есть ли в заказе добавляемый товар'
    
    # ошибка с id заказа или товара
    if order == None:
        return JSONResponse(status_code=404, content={ "message": f"Заказа с id {order_id} не существует"})
    if product == None:
        return JSONResponse(status_code=404, content={ "message": f"Товара c id {product_id} не существует"})
    
    # товара нет на складе
    if product.Count == 0:
        return JSONResponse(status_code=404, content={ "message": "Товар закончился, заказ невозможен"})
    
    # требуется больше товара, чем есть на складе
    if product.Count < required_product_count:
        required_product_count = product.Count
        return JSONResponse(status_code=404, content={ "message": f"В заказ добавлено {product.Count} штук из требуемых {required_product_count}. Товар закончился."})

    # Проверка: есть ли в заказе добавляемый товар 
    for row in db.query(OrderProducts).filter(OrderProducts.Order_id == order_id):
        # товар есть в заказе => его количество обновляется 
        if row.Product_id == product_id:
            product_in_order = True       # флаг
            orderProducts.Product_count += required_product_count
            order.Order_sum += product.Price * required_product_count
            product.Count = (product.Count - required_product_count)
            break

    # товара нет в заказе => создаётся новая строка  
    if not product_in_order:
        del orderProducts
        orderProducts = OrderProducts()
        orderProducts.Order_id = order_id
        orderProducts.Product_id = product_id
        orderProducts.Product_count = required_product_count
        order.Order_sum += product.Price * required_product_count
        product.Count = (product.Count - required_product_count)
            
    # внесение изменений в бд
    db.add(order)
    db.add(product)
    db.add(orderProducts)
    db.commit()
    db.refresh(order)
    db.refresh(product)
    db.refresh(orderProducts)
    result = {"status":"OK", "code":200, "content":orderProducts}
    return result 




from models import *
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from fastapi import Depends, FastAPI, Body, Request, Query
from fastapi.responses import JSONResponse, FileResponse
#from datetime import datetime
from pydantic import create_model




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

# Преобразование запроса в словарь
def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d



@app.get("/")
def root():
    return "Корень проекта, но фронтенда тут нет" 


@app.get("/orders")
def get_all_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@app.get("/order/{id_}")
def get_one_order(id_, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.Id == id_).first()
    if order==None:  
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})
    result = {"status":"OK", "code":200, "content": order}
    return result




@app.put("/add_product_to_order")
def edit_order(data = Body(), db: Session = Depends(get_db)):
    order_id = data["order_id"]
    product_id = data["product_id"]
    required_product_count = data["product_count"]
    order = db.query(Order).filter(Order.Id == order_id).first()
    orderProducts = db.query(OrderProducts).filter(OrderProducts.Product_id == order_id).first()
    product = db.query(Product).filter(Product.Id == product_id).first()
    
    # ошибка с id товара
    if order == None:
        return JSONResponse(status_code=404, content={ "message": f"Заказа {order_id} не существует"})
    
    # товара нет на складе
    if product.Count == 0:
        return JSONResponse(status_code=404, content={ "message": "Товар закончился"})
    
    # требуется больше товара, чем есть на складе
    if product.Count < required_product_count:
        return JSONResponse(status_code=404, content={ "message": f"В заказ добавлено {product.Count} штук из требуемых {required_product_count}. Товар закончился."})
      
    for row in db.query(OrderProducts).filter(OrderProducts.Order_id == order_id):
        # товар есть в заказе и его количество обновляется 
        if row.Product_id == product_id:
            print('___666___', row.Product_id, product_id, sep=', ')
        # товара нет в заказе и сооздаётся новая строка  
        else:
            print('___444___', row.Product_id, product_id, sep=', ')
        

    # товара нет в заказе, т.е. создаётся новая позиция


    
    # внесение изменений в бд
    #db.add(transaction)
    #db.commit()
    #db.refresh(transaction)
    #db.refresh(client)
    #content = "Клиент: {0}, Баланс в рублях: {1}, Комментарий: {2}".format(client_parsed['name'],
    #                                                                       client.balance, comments_)
    result = {"status":"OK", "code":200, "content": orderProducts}
    #print('type(orderProducts) ', type(orderProducts))
    return product #orderProducts.Product_count












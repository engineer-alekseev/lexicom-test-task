from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.contacts import DataIn, AddressOut, ApiResponse, validate_phone
from app.db.redis import get_redis


router = APIRouter()


@router.post("/write_data", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def write_data(
    data: DataIn,
    redis = Depends(get_redis)
):
    """
    Записывает или обновляет данные адреса в Redis по номеру телефона.

    Params:
    - data: DataIn - объект, содержащий номер телефона и адрес.

    Returns:
    - JSON-объект

    HTTP statuses:
    - 201 Created: Если данные успешно записаны
    - 400 Bad request: если такая запись уже существует
    - 422 Unprocessable Entity: Если входные данные не прошли валидацию
    - 500 Internal Server Error: Если произошла ошибка при записи данных.
    """
    try:
        existing_address = await redis.get(data.phone)
        if existing_address:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Телефонный номер уже существует"
            )
        await redis.set(data.phone, data.address)
        return ApiResponse(
            status="created",
            code=status.HTTP_201_CREATED,
            entity=data
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Не удалось записать данные"
        )

@router.get("/check_data", response_model=AddressOut, status_code=status.HTTP_200_OK)
async def check_data(
    phone: str,
    redis = Depends(get_redis)
):
    """
    Получает адрес из Redis по номеру телефона.

    Params:
    - phone: str - номер телефона, по которому нужно получить адрес.

    Returns:
    - AddressOut: Объект с полем `address`, содержащим адрес.

    HTTP statuses:
    - 200 OK: Если адрес успешно найден и возвращен.
    - 400 Bad request: Если переданный номер не прошел валидацию.
    - 404 Not Found: Если номер телефона не найден.
    - 500 Internal Server Error: Если произошла ошибка при получении данных
    """
    try:
        validate_phone(phone)
        address = await redis.get(phone)
        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Адрес не найден")
        return AddressOut(address=address)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to retrieve data"
        )


@router.put("/update_data", response_model=ApiResponse, status_code=status.HTTP_200_OK)
async def update_data(
    data: DataIn,
    redis = Depends(get_redis)
):
    """
    Обновляет данные адреса в Redis по номеру телефона.

    Params:
    - data: DataIn - объект, содержащий номер телефона и новый адрес.

    Returns:
    - JSON-объект

    HTTP statuses:
    - 200 OK: Если данные успешно обновлены
    - 404 Not Found: Если номер телефона не найден
    - 422 Unprocessable Entity: Если входные данные не прошли валидацию
    - 500 Internal Server Error: Если произошла ошибка при обновлении данных.
    """
    try:
        validate_phone(data.phone)
        existing_address = await redis.get(data.phone)
        if not existing_address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Телефонный номер не найден"
            )
        await redis.set(data.phone, data.address)
        return ApiResponse(
            status="updated",
            code=status.HTTP_200_OK,
            entity=data
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Не удалось обновить данные"
        )


@router.delete("/delete_data", status_code=status.HTTP_204_NO_CONTENT)
async def delete_data(
    phone: str,
    redis = Depends(get_redis)
):
    """
    Удаляет запись адреса из Redis по номеру телефона.

    Params:
    - phone: str - номер телефона, по которому нужно удалить адрес.

    Returns:
    - Нет тела ответа

    HTTP statuses:
    - 204 No Content: Если данные успешно удалены
    - 404 Not Found: Если номер телефона не найден
    - 422 Unprocessable Entity: Если номер телефона не прошел валидацию
    - 500 Internal Server Error: Если произошла ошибка при удалении данных.
    """
    try:
        validate_phone(phone)
        existing_address = await redis.get(phone)
        if not existing_address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Телефонный номер не найден"
            )
        await redis.delete(phone)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Не удалось удалить данные"
        )

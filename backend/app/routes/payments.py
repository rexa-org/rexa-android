from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/webhook")
async def razorpay_webhook(request: Request):
    # TODO: verify signature, update payment status
    data = await request.json()
    return {"ok": True, "data": data}

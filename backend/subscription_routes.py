
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import get_db
from models import User, Subscription, SubscriptionPlanType, SubscriptionStatus
from auth import get_current_user
from schemas import SubscriptionResponse, SubscriptionCreate, UpgradeRequest

router = APIRouter(
    prefix="/subscription",
    tags=["subscription"]
)

@router.get("/status", response_model=SubscriptionResponse)
async def get_subscription_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's subscription status.
    If no subscription exists, create a default (inactive/new) record.
    """
    sub = db.query(Subscription).filter(Subscription.user_id == current_user.id).first()
    
    if not sub:
        # Auto-create a subscription record for new users (or existing ones accessing this feature)
        # Default to TRIAL but maybe check if they registered long ago? 
        # For simplicity, let's say they haven't started trial yet until they hit "Activate"
        # OR we can auto-start trial on registration. User request says "free trial... after that subscribe".
        # Let's create a placeholder record that allows them to ACTIVATE trial.
        
        # Actually, let's make it simpler: Auto-start trial on first access if not exists
        # Or let them click "Start Free Trial". Let's stick to auto-start for smooth UX or manual?
        # Let's go with: No sub = Check registration date. 
        # Actually, let's create a "pending" or "trial" state. 
        # Let's just create a new TRIAL subscription starting NOW if one doesn't exist.
        
        new_sub = Subscription(
            user_id=current_user.id,
            plan_type=SubscriptionPlanType.TRIAL,
            status=SubscriptionStatus.ACTIVE,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=7), # 1 Week Free Trial
            free_consultation_used=False
        )
        db.add(new_sub)
        db.commit()
        db.refresh(new_sub)
        return new_sub

    # Check for expiry
    if sub.plan_type == SubscriptionPlanType.TRIAL and sub.status == SubscriptionStatus.ACTIVE:
        if sub.end_date and datetime.utcnow() > sub.end_date:
            sub.status = SubscriptionStatus.EXPIRED
            db.commit()
            db.refresh(sub)
    
    return sub

@router.post("/activate-trial", response_model=SubscriptionResponse)
async def activate_trial(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sub = db.query(Subscription).filter(Subscription.user_id == current_user.id).first()
    if sub:
        if sub.plan_type == SubscriptionPlanType.PREMIUM:
             raise HTTPException(status_code=400, detail="Already a premium member")
        if sub.status == SubscriptionStatus.EXPIRED:
             raise HTTPException(status_code=400, detail="Trial already expired")
        return sub # Already active

    new_sub = Subscription(
        user_id=current_user.id,
        plan_type=SubscriptionPlanType.TRIAL,
        status=SubscriptionStatus.ACTIVE,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=7),
        free_consultation_used=False
    )
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)
    return new_sub

@router.post("/upgrade", response_model=SubscriptionResponse)
async def upgrade_subscription(
    request: UpgradeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mock endpoint to upgrade to Premium.
    In real world, this would verify payment.
    """
    sub = db.query(Subscription).filter(Subscription.user_id == current_user.id).first()
    
    if not sub:
        sub = Subscription(user_id=current_user.id)
        db.add(sub)
    
    sub.plan_type = SubscriptionPlanType.PREMIUM
    sub.status = SubscriptionStatus.ACTIVE
    sub.end_date = None # Lifetime or manage recurring
    
    db.commit()
    db.refresh(sub)
    return sub

@router.post("/use-consultation", response_model=SubscriptionResponse)
async def use_free_consultation(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark the one-time free consultation as used.
    """
    sub = db.query(Subscription).filter(Subscription.user_id == current_user.id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
        
    if sub.plan_type == SubscriptionPlanType.PREMIUM:
        return sub # Premium has unlimited? or this flag is only for trial tracking.
        
    if sub.free_consultation_used:
        raise HTTPException(status_code=400, detail="Free consultation already used")
        
    sub.free_consultation_used = True
    db.commit()
    db.refresh(sub)
    return sub

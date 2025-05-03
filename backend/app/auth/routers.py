from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.users.models import UserCreate, UserPublic, UserInDB
from app.users.crud import get_user
from app.database import users_collection
from app.auth.auth import hash_password, verify_password, create_access_token
from datetime import timedelta
from jose import JWTError, jwt
from bson import ObjectId
import os
from app.auth.auth import generate_email_token, verify_email_token
from app.utils.email_utils import send_verification_email
from pydantic import BaseModel

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# /auth/register
@router.post("/register", status_code=201)
async def register(user: UserCreate):
    existing_user = get_user(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé")

    hashed = hash_password(user.password)
    user_data = user.dict()
    user_data["hashed_password"] = hashed
    user_data["is_verified"] = False

    result = users_collection.insert_one(user_data)

    # Générer un token de validation
    token = generate_email_token(user.email)
    await send_verification_email(user.email, token)

    return {"message": "Utilisateur créé. Vérifiez votre email."}

@router.get("/verify-email")
def verify_email(token: str):
    try:
        email = verify_email_token(token)
        user = get_user(email)
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

        users_collection.update_one(
            {"email": email},
            {"$set": {"is_verified": True}}
        )
        return {"message": "Email vérifié avec succès ✅"}
    except Exception:
        raise HTTPException(status_code=400, detail="Lien de vérification invalide ou expiré")


# /auth/login
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authentifie un utilisateur via email (utiliser le champ `username`) et mot de passe.
    """
    user = get_user(form_data.username)  # ici, username = email
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Adresse email non vérifiée")

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Helper pour extraire user depuis JWT
async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(email)
    if user is None:
        raise credentials_exception
    return user

# /auth/me
@router.get("/me", response_model=UserPublic)
def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return UserPublic(id=str(current_user.id), email=current_user.email, full_name=current_user.full_name)

# /auth/forgot-password (mock pour l'instant)
@router.post("/forgot-password")
async def forgot_password(email: str):
    user = get_user(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # En vrai : générer un token unique et envoyer un mail
    token = generate_email_token(email)
    await send_verification_email(email, token)
    return {"message": f"Un lien de réinitialisation a été envoyé à {email}."}

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest):
    try:
        email = verify_email_token(data.token)
        user = get_user(email)
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur introuvable")

        hashed = hash_password(data.new_password)
        users_collection.update_one(
            {"email": email},
            {"$set": {"hashed_password": hashed}}
        )
        return {"message": "Mot de passe réinitialisé avec succès"}
    except Exception:
        raise HTTPException(status_code=400, detail="Lien invalide ou expiré")

@router.put("/update-name")
def update_name(new_name: str, current_user: UserInDB = Depends(get_current_user)):
    users_collection.update_one({"email": current_user.email}, {"$set": {"full_name": new_name}})
    return {"message": "Nom mis à jour"}

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

@router.post("/change-password")
def change_password(data: ChangePasswordRequest, current_user: UserInDB = Depends(get_current_user)):
    if not verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Mot de passe actuel incorrect")

    new_hashed = hash_password(data.new_password)
    users_collection.update_one({"email": current_user.email}, {"$set": {"hashed_password": new_hashed}})
    return {"message": "Mot de passe mis à jour"}

@router.delete("/delete-account")
def delete_account(current_user: UserInDB = Depends(get_current_user)):
    result = users_collection.delete_one({"email": current_user.email})
    if result.deleted_count == 1:
        return {"message": "Compte supprimé avec succès"}
    raise HTTPException(status_code=404, detail="Utilisateur introuvable")

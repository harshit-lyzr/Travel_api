from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal, List
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase1: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Define the FastAPI app
app = FastAPI()

# Define the schema
class Location(BaseModel):
    name: str = Field(..., example="Eiffel Tower")
    latitude: float = Field(..., example=48.8588443)
    longitude: float = Field(..., example=2.2943506)
    time_to_enjoy: float = Field(..., gt=0, example=2.5)
    category: str = Field(..., example="Historical")

class LocationResponse(Location):
    id: int

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    try:
        response = supabase1.table("company_tickets").select("*").limit(1).execute()
        if response:
            return {"status": "healthy"}
        else:
            raise Exception("its not giving Response")

    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

# CRUD Endpoints
@app.post("/locations/", response_model=LocationResponse)
async def create_location(location: Location):
    """
    Create a new location.
    """
    response = supabase1.table("company_tickets").insert(location.dict()).execute()
    if response:
        return response.data[0]
    else:
        raise print("You got error")

@app.get("/locations/", response_model=List[LocationResponse])
async def list_locations():
    """
    Retrieve all locations.
    """
    response = supabase1.table("company_tickets").select("*").execute()
    if response.data:
        return response.data
    else:
        raise print("You got error")

@app.get("/locations/{location_id}", response_model=LocationResponse)
async def get_location(location_id: int):
    """
    Retrieve a location by ID.
    """
    response = supabase1.table("company_tickets").select("*").eq("id", location_id).execute()
    if response.data:
        return response.data[0]
    else:
        raise print("You got error")


@app.put("/locations/{location_id}", response_model=LocationResponse)
async def update_location(location_id: int, location: Location):
    """
    Update a location by ID.
    """
    response = supabase1.table("company_tickets").update(location.dict()).eq("id", location_id).execute()
    if response.data:
        return response.data[0]
    else:
        raise print("You got error")

@app.delete("/locations/{location_id}")
async def delete_location(location_id: int):
    """
    Delete a location by ID.
    """
    response = supabase1.table("company_tickets").delete().eq("id", location_id).execute()
    if response.data:
        return response.data[0]
    return {"message": "Location deleted successfully"}

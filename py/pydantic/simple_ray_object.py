from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from random import randint

def get_node_list() -> List[int]: 
    return [randint(1, 5) for _ in range(5)]

class RayUser(BaseModel):
    id: int = Field(description="Unique identifier for the person")   
    username : str = Field(description="Name of the person")
    password : str = Field(description="Password of the person")
    alias :str = Field(description="Alias of the person")
    timestamp: Optional[datetime] = Field(description="Signup timestamp")
    node_types: List[int] = Field(description="List of node types")
if __name__ == "__main__":
    id = randint(1, 100)
    ray_user_data = {'id':id,
                    'username': f"user-{id}",
                    'password': f"pass-{id}-{id}2U",
                    'alias': 'anonymous',
                    'timestamp': datetime.now(),
                    'node_types': get_node_list()
                
    }
    ray_user = RayUser(**ray_user_data)
    print(ray_user)

    ray_user_data_2 = {'id':  123,
                    'username': f"user-{id}",
                    'password': f"pass-{id}-{id}2U",
                    'alias': 'anonymous',
                    'timestamp': datetime.now(),
                    'node_types': get_node_list()
    }

    # pydantic error validation
    try:
        ray_user_2 = RayUser(**ray_user_data_2)
    except ValueError as e:
        print(e.json())

from datetime import datetime
from operator import ge
from typing import List, Optional
from pydantic import BaseModel
from random import randint

def get_node_list() -> List[int]: 
    return [randint(1, 5) for _ in range(5)]

class RayUser(BaseModel):
    id: int    
    username : str
    password : str
    alias = 'anonymous'
    timestamp: Optional[datetime] = None
    nodes_types: List[int] = []

if __name__ == "__main__":
    ray_user_data = {'id': randint(1, 100),
                    'username': f"user-{id}",
                    'password': f"pass-{randint(1,100)}",
                    'alias': 'anonymous',
                    'timestamp': datetime.now(),
                    'node_types': get_node_list()
    }
    ray_user = RayUser(**ray_user_data)
    print(ray_user)

    ray_user_data_2 = {'id': "random-number: 123",
                    'username': f"user-{id}",
                    'password': f"pass-{randint(1,100)}",
                    'alias': 'anonymous',
                    'timestamp': datetime.now(),
                    'node_types': get_node_list()
    }

    # pydantic error validation
    try:
        ray_user_2 = RayUser(**ray_user_data_2)
    except ValueError as e:
        print(e.json())

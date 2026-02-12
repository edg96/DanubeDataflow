from .models.Senators import save_senators_to_postgres
from .models.Deputy import save_deputies_to_postgres

if __name__ == "__main__":
    save_senators_to_postgres()
    save_deputies_to_postgres()
